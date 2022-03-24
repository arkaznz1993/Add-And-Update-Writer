import os
import mysql.connector
from mysql.connector.constants import ClientFlag

# Instance name - flash-hour-338103:asia-south1:test-sql-server

config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': '35.200.140.194',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': os.environ.get('SSL_CA'),
    'ssl_cert': os.environ.get('SSL_CERT'),
    'ssl_key': os.environ.get('SSL_KEY'),
    'database': os.environ.get('DB_NAME'),
}

GET_WRITERS = 'SELECT TrelloId, Team FROM Writers'

GET_CUSTOM_FIELDS = 'SELECT * FROM CustomFields;'

GET_CUSTOM_FIELD_OPTIONS = 'SELECT CustomFieldOptions.* FROM CustomFieldOptions ' \
                           'JOIN CustomFields ON CustomFieldOptions.IdCustomField = CustomFields.Id;'

INSERT_WRITER = 'INSERT INTO Writers (' \
                'TrelloId, Name, Team, Role, DailyWordCount, Overtime, DOJ, EmpCode, Leaves)' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
                'ON DUPLICATE KEY UPDATE ' \
                'Name = VALUES(Name),' \
                'Team = VALUES(Team),' \
                'Role = VALUES(Role),' \
                'DailyWordCount = VALUES(DailyWordCount),' \
                'Overtime = VALUES(Overtime),' \
                'DOJ = VALUES(DOJ),' \
                'EmpCode = VALUES(EmpCode),' \
                'Leaves = VALUES(Leaves);'

UPDATE_WRITER = 'UPDATE Writers ' \
                'SET ' \
                'Team = %s,' \
                'Role = %s,' \
                'DailyWordCount = %s,' \
                'Overtime = %s,' \
                'EmpCode = %s ' \
                'WHERE ' \
                'TrelloId = %s;'


class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def get_custom_fields(self):
        self.cursor.execute(GET_CUSTOM_FIELDS)
        return self.cursor.fetchall()

    def get_custom_field_options(self):
        self.cursor.execute(GET_CUSTOM_FIELD_OPTIONS)
        return self.cursor.fetchall()

    def get_writers(self):
        self.cursor.execute(GET_WRITERS)
        return self.cursor.fetchall()

    def insert_writer_details(self, values):
        self.cursor.executemany(INSERT_WRITER, values)
        self.connection.commit()

    def update_writer_details(self, values):
        self.cursor.executemany(UPDATE_WRITER, values)
        self.connection.commit()


database_connection = DatabaseConnector()
