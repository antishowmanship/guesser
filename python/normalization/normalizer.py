import re
import csv
from string import digits
from section import Section


NUMBERS_RE = re.compile("\d+")
SECTION_ID = 'section_id'
SECTION_NAME = 'section_name'
ROW_ID = 'row_id'
ROW_NAME = 'row_name'

def tokenize(section_name):
    if not section_name:
        return None
    token_list = [word.translate(None, digits) for word in section_name.split() if word.translate(None, digits)]
    if len(token_list) > 0:
        return token_list
    return None


def arena_section_name_stripper(canonical_section_name):
    numbers = NUMBERS_RE.findall(canonical_section_name)
    if len(numbers) <> 1:
        return None
    else:
        return numbers[0]


def fuzzy_section_chooser(tokens, sections):
    scored_sections = []
    for section in sections:
        score = 0
        for token in tokens:
            if token in section.name_alpha_tokens:
                score += 1
        if score > 0:
            scored_sections.add((section, score))
    sorted(scored_sections, key=lambda x: x[1])
    if len(scored_sections) > 0:
        return scored_sections[0]
    return None



class Normalizer(object):

    def __init__(self):
        self.sections_full = {}
        self.section_broad = {}

    def read_manifest(self, manifest):
        """reads a manifest file

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """

        ## your code goes here
        with open(manifest, 'r') as manifest_file:
            manifest_reader = csv.DictReader(manifest_file)

            for line in manifest_reader:
                section_name = line[SECTION_NAME].lower()
                section_name_cleaned = arena_section_name_stripper(section_name)
                section_id = int(line[SECTION_ID]) if line[SECTION_ID] else None
                row_name = line[ROW_NAME].lower()
                row_id = int(line[ROW_ID]) if line[ROW_ID] else None
                if section_name in self.sections_full and row_name:
                    section = self.sections_full[section_name]
                    section.add_row(row_name, row_id)
                else:
                    section = Section(section_name, section_id, arena_section_name_stripper)
                    if row_name:
                        section.add_row(row_name, row_id)
                    self.sections_full[section_name] = section
                    if section_name_cleaned in self.sections_broad:
                        self.section_broad[section_name_cleaned].add(section)
                    else:
                        self.section_broad[section_name_cleaned] = [section]


    def normalize(self, section_name, row_name=''):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """

        ## your code goes here
        section_name = section_name.lower().strip() if section_name else None
        row_name = row_name.lower().strip() if row_name else None
        print "section_name: " + section_name
        print "row_name: " + row_name
        section = None
        if section_name in self.sections_full:
            section = self.sections_full[section_name]
        else:
            clean_name = arena_section_name_stripper(section_name)
            print "clean_name: " + clean_name
            sections = self.sections_cleaned[clean_name]
            if len(sections) == 1:
                section = sections[0]
            else:
                section = fuzzy_section_chooser(tokenize(section_name), sections)
            #section = next((potential_section for potential_section in self.sections.values() if potential_section.clean_name == clean_name), None)

        if not section:
            return None, None, False
        elif not section.has_rows and not row_name:
            return section.id, None, True
        elif row_name not in section.rows:
            return section.id, None, False

        row_id = section.rows[row_name]
        return section.id, row_id, True


