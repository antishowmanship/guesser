import csv

from section import Section
from util import abbreviate, tokenize, arena_section_name_stripper, fuzzy_section_chooser

SECTION_ID = 'section_id'
SECTION_NAME = 'section_name'
ROW_ID = 'row_id'
ROW_NAME = 'row_name'


class Normalizer(object):

    def __init__(self):
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
                    if section_name == "315":
                        print "! row_name: " + row_name
                    if row_name:
                        section.add_row(row_name, row_id)
                        if section_name == "315":
                            print row_name
                            print row_id
                            print section.rows
                    self.sections_full[section_name] = section
                    if section_name_cleaned in self.sections_broad:
                        self.sections_broad[section_name_cleaned].add(section)
                    else:
                        self.sections_broad[section_name_cleaned] = [section]
                    self.sections_abbrev[(section.name_abbrev, section_name_cleaned)] = section
                    if section.name_abbrev in self.sections_abbrev:
                        print "NON-UNIQUE SECTION ABBREVIATION!!!!!"
                        print section.exact_name + ", " + section.name_abbrev
                        print self.sections_abbrev[(section_name_cleaned, section.name_abbrev)].exact_name


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
            sections = self.sections_broad[clean_name]
            if len(sections) == 1:
                section = sections[0]
            else:
                section = fuzzy_section_chooser(tokenize(section_name), sections)

            if not section:
                abbrev_name = abbreviate(tokenize(section_name))
                if (abbrev_name, clean_name) in self.sections_abbrev:
                    section = self.sections_abbrev[abbrev_name]
            #section = next((potential_section for potential_section in self.sections.values() if potential_section.clean_name == clean_name), None)

        if section:
            print "Section name: " + section.exact_name
            if section.rows:
                for row_name, row_id in section.rows.items():
                    print "row name: " + row_name + ", row_id: " + str(row_id)

        if not section:
            return None, None, False
        elif not section.has_rows and not row_name:
            return section.id, None, True
        elif row_name not in section.rows:
            return section.id, None, False

        row_id = section.rows[row_name]
        return section.id, row_id, True


