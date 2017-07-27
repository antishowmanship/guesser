
class Section(object):

    def __init__(self, section_name, section_id, name_normalize_func=None):
        self.exact_name = section_name
        self.match_name = name_normalize_func(section_name) if name_normalize_func else section_name
        self.id = section_id
        self.has_rows = False
        self.rows = {}

    def add_row(self, row_name, row_id):
        if not row_name or not row_id:
            return

        self.has_rows = True
        if row_name not in self.rows:
            self.rows[row_name] = row_id
