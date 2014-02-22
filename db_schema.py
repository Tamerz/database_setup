import xml.etree.ElementTree as ET
import sqlalchemy


class DBDatabase(object):
    def __init__(self, database_xml_file):
        self.database_info = self.get_info_from_xml(database_xml_file)
        self.tables = []
        self.populate()

    def get_info_from_xml(self, database_xml_file):
        tree = ET.ElementTree(file=database_xml_file)
        return tree.getroot()

    def populate(self):
        for child in self.database_info:
            if child.tag == 'table':
                new_table = DBTable(child)
                self.tables.append(new_table)

    def get_table_by_name(self, name):
        wanted_table = None
        for table in self.tables:
            if table.name == name:
                wanted_table = table
        return wanted_table


class DBTable(object):
    def __init__(self, table_info):
        self.table_info = table_info
        self.name = None
        self.columns = []
        self.permissions = []
        self.populate()

    def populate(self):
        self.name = self.table_info.attrib['name']
        self.add_columns()
        self.add_permissions()

    def add_columns(self):
        for child_of_tables in self.table_info:
            if child_of_tables.tag == 'column':
                new_column = DBColumn(child_of_tables)
                self.columns.append(new_column)

    def add_permissions(self):
        for child_of_tables in self.table_info:
            if child_of_tables.tag == 'permissions':
                self.permissions.append(DBPermission(child_of_tables))

    def get_column_by_name(self, name):
        wanted_column = None
        for column in self.columns:
            if column.name == name:
                wanted_column = column
        return wanted_column


class DBColumn(object):
    def __init__(self, column_info):
        self.column_info = column_info
        self.name = None
        self.type = None
        self.length = 0
        self.can_be_null = False
        self.is_primary_key = False
        self.is_foreign_key = False
        self.autoincrement = False
        self.foreign_key_table = None
        self.foreign_key_column = None
        self.foreign_key_constraint = None
        self.populate()

    def populate(self):
        self.name = self.column_info.attrib['name']
        self.type = self.column_info.attrib['type']
        try:
            self.length = int(self.column_info.attrib['length'])
        except KeyError:
            pass

        try:
            if self.column_info.attrib['key'] == 'primary':
                self.is_primary_key = True
            elif self.column_info.attrib['key'] == 'foreign':
                self.is_foreign_key = True
                self.set_foreign_key_info()
            if self.column_info.attrib['autoincrement'] == 'true':
                self.autoincrement = True
        except KeyError:
            pass

    def set_foreign_key_info(self):
        for child in self.column_info:
            if child.tag == 'fkey_table':
                self.foreign_key_table = child.text
            elif child.tag == 'fkey_column':
                self.foreign_key_column = child.text
            elif child.tag == 'fkey_constraint':
                self.foreign_key_constraint = child.text

    def get_sa_object(self):
        if self.type == 'int':
            sa_type = sqlalchemy.Integer
        elif self.type == 'varchar':
            sa_type = sqlalchemy.String(self.length)

        return sqlalchemy.Column(self.name, sa_type, primary_key=self.is_primary_key)


class DBPermission(object):
    def __init__(self, permissions_info):
        self.permissions_info = permissions_info
        self.user = self.permissions_info.attrib['user']
        self.permissions = []
        self.parse_permissions()

    def parse_permissions(self):
        for permission in self.permissions_info:
            if permission.tag == 'permission':
                self.permissions.append(permission.text)


if __name__ == '__main__':

    pass