
class Section(object):

    def __init__(self, section_name, section_id, name_normalize_func=None):
        self.exact_name = section_name
        self.clean_name = name_normalize_func(section_name) if name_normalize_func else section_name
        self.id = int(section_id) if section_id else None
        self.has_rows = False
        self.rows = {}

    def add_row(self, row_name, row_id):
        if not row_name or not row_id:
            return

        self.has_rows = True
        if row_name not in self.rows:
            self.rows[row_name] = int(row_id)
