import csv

from section import Section
from util import abbreviate, tokenize, extract_number, fuzzy_section_chooser

SECTION_ID = 'section_id'
SECTION_NAME = 'section_name'
ROW_ID = 'row_id'
ROW_NAME = 'row_name'


class Normalizer(object):

    def __init__(self):
        """
        Establish dictionary structures for various ways to represent section names:
        exact matches, semi-unique labels (numbers), and abbreviations
        """
        self.sections_full = {}
        self.sections_broad = {}
        self.sections_abbrev = {}

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
        with open(manifest, 'r') as manifest_file:
            manifest_reader = csv.DictReader(manifest_file)

            for line in manifest_reader:
                section_name = line[SECTION_NAME].lower()
                section_name_cleaned = extract_number(section_name)
                section_id = int(line[SECTION_ID]) if line[SECTION_ID] else None
                row_name = line[ROW_NAME].lower()
                row_id = int(line[ROW_ID]) if line[ROW_ID] else None
                if section_name in self.sections_full and row_name:
                    section = self.sections_full[section_name]
                    section.add_row(row_name, row_id)
                else:
                    section = Section(section_name, section_id, extract_number)
                    if row_name:
                        section.add_row(row_name, row_id)
                    self.sections_full[section_name] = section
                    if section_name_cleaned in self.sections_broad:
                        self.sections_broad[section_name_cleaned].append(section)
                    else:
                        self.sections_broad[section_name_cleaned] = [section]
                    self.sections_abbrev[(section.name_abbrev, section_name_cleaned)] = section


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
        section_name = section_name.lower().strip() if section_name else None
        row_name = row_name.lower().lstrip("0").strip() if row_name else None
        section = None
        #Starting with most precise (exact match) and moving to least precise, attempt to match
        #input section name with a section name from the manifest
        if section_name in self.sections_full:
            section = self.sections_full[section_name]

        #Check if number from input name matches a section number from manifest,
        #then if that number is not unique, attempt to make best guess based on words/letters
        #in input name
        if not section:
            clean_name = extract_number(section_name)
            sections = self.sections_broad[clean_name]
            if len(sections) == 1:
                section = sections[0]
            else:
                input_tokens = tokenize(section_name)
                if input_tokens:
                    section = fuzzy_section_chooser(input_tokens, sections)

        #Now check based on abbreviations - once by abbreviating words in input,
        #next by assuming input is itself an abbreviation
        if not section:
            abbrev_name = abbreviate(tokenize(section_name))
            if abbrev_name and (abbrev_name, clean_name) in self.sections_abbrev:
                section = self.sections_abbrev[(abbrev_name, clean_name)]

        if not section:
            abbrev_name = abbreviate(tokenize(section_name))
            if abbrev_name and (abbrev_name, clean_name) in self.sections_abbrev:
                section = self.sections_abbrev[(abbrev_name, clean_name)]
            elif tokenize(section_name) and (tokenize(section_name)[0], clean_name) in self.sections_abbrev:
                section = self.sections_abbrev[(tokenize(section_name)[0], clean_name)]

        if not section:
            return None, None, False
        elif not section.has_rows and not row_name:
            return section.id, None, True
        elif row_name not in section.rows:
            return section.id, None, False

        row_id = section.rows[row_name]
        return section.id, row_id, True


