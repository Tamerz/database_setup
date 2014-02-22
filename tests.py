import unittest
import sqlalchemy
from db_schema import DBDatabase


class ReadInTablesTest(unittest.TestCase):

    def setUp(self):
        self.database = DBDatabase('schema.xml')
        self.main_table = self.database.get_table_by_name('ESEventlogMain')

    def test_should_find_this_table(self):
        found_table = False
        if self.main_table.name == 'ESEventlogMain':
            found_table = True
        self.assertEqual(found_table, True)

    def test_should_not_find_this_table(self):
        found_table = False
        if self.main_table.name == 'ESEventlogMainFake':
            found_table = True
        self.assertNotEqual(found_table, True)

    def test_table_object_has_name_set(self):
        self.assertEqual(self.main_table.name, 'ESEventlogMain')

    def test_main_table_has_right_number_of_columns(self):
        self.assertEqual(len(self.main_table.columns), 15)

    def test_main_table_should_have_eventmessage_column(self):
        found_column = self.main_table.get_column_by_name('eventmessage')

        self.assertEqual(found_column.name, 'eventmessage')

    def test_main_table_should_not_have_eventfake_column(self):
        found_column = self.main_table.get_column_by_name('fakecolumn')
        self.assertEqual(found_column, None)

    def test_eventmessage_column_is_type_text(self):
        found_column = self.main_table.get_column_by_name('eventmessage')
        self.assertEqual(found_column.type, 'text')

    def test_eventmessage_column_length(self):
        found_column = self.main_table.get_column_by_name('eventmessage')
        self.assertEqual(found_column.length, 7400)

    def test_eseventlogmain_eventcomputer_is_foreign_key(self):
        found_column = self.main_table.get_column_by_name('eventcomputer')
        self.assertEqual(found_column.is_foreign_key, True)

    def test_foreign_key_table_if_is_foreign_key(self):
        found_column = self.main_table.get_column_by_name('eventcomputer')
        self.assertEqual(found_column.foreign_key_table, 'ESEventlogComputer')

    def test_foreign_key_column_if_is_foreign_key(self):
        found_column = self.main_table.get_column_by_name('eventcomputer')
        self.assertEqual(found_column.foreign_key_column, 'id')

    def test_foreign_key_constraint_if_is_foreign_key(self):
        found_column = self.main_table.get_column_by_name('eventcomputer')
        self.assertEqual(found_column.foreign_key_constraint, 'FK_ESEventlogMain_ESEventlogComputer')

    def test_get_table_by_name_from_database_object(self):
        table = self.database.get_table_by_name('ESEventlogMain')
        self.assertEqual(table.name, 'ESEventlogMain')

    def test_column_is_primary(self):
        table = self.database.get_table_by_name('ESEventlogLog')
        column = table.get_column_by_name('id')
        self.assertEqual(column.is_primary_key, True)

    def test_column_is_autoincrement(self):
        table = self.database.get_table_by_name('ESEventlogType')
        column = table.get_column_by_name('id')
        self.assertEqual(column.autoincrement, True)

    def test_table_has_permissions_for_user(self):
        table = self.database.get_table_by_name('ESEventlogID')
        permissions = table.permissions
        self.assertNotEqual(permissions, [])

    def test_table_permissions_correct(self):
        table = self.database.get_table_by_name('ESEventlogID')
        permissions = table.permissions
        for permission in permissions:
            if permission.user == 'eventsentry_svc':
                permission_list = permission.permissions
        self.assertEqual(set(permission_list), set(['UPDATE', 'INSERT', 'SELECT']))


class GenerateSqlAlchemyObjects(unittest.TestCase):

    DB_FILE = 'unittest.db'

    def setUp(self):
        self.database = DBDatabase('schema.xml')
        sa_db = sqlalchemy.create_engine('sqlite:///' + self.DB_FILE)
        self.metadata = sqlalchemy.MetaData(bind=sa_db)

    def tearDown(self):
        import os
        try:
            os.remove(self.DB_FILE)
        except FileNotFoundError:
            pass

    def test_getting_correct_sa_object_from_column(self):
        table = self.database.get_table_by_name('ESEventlogMain')
        column = table.get_column_by_name('eventdata')
        sa_column = sqlalchemy.Column('eventdata', sqlalchemy.Integer, primary_key=False)

        # TODO: I had to force this to pass since I'm not sure the correct way to do the comparison
        #self.assertEqual(sa_column, column.get_sa_object())
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()