from util import abbreviate, tokenize


class Section(object):

    def __init__(self, section_name, section_id, name_normalize_func=None):
        self.exact_name = section_name
        self.num_name = name_normalize_func(section_name) if name_normalize_func else section_name
        self.name_alpha_tokens = tokenize(section_name)
        self.name_abbrev = abbreviate(self.name_alpha_tokens) if self.name_alpha_tokens else None
        self.id = int(section_id) if section_id else None
        self.has_rows = False
        self.rows = {}

    def add_row(self, row_name, row_id):
        if row_name is None or row_id is None:
            return

        self.has_rows = True
        if row_name not in self.rows:
            self.rows[row_name] = int(row_id)
