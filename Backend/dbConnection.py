import psycopg2
connection=None

def setConnection( dbname, dbuser, dbpass, dbhost):
    global connection
    connection=DBConnection(dbname, dbuser, dbpass, dbhost)
    setup_preparedStatements()

class DBConnection():

    def __init__(self, dbname, dbuser, dbpass, dbhost):
        try:
            self.conn = psycopg2.connect(
                "dbname='{}' user='{}' host='{}' password='{}'".format(dbname, dbuser, dbhost, dbpass))
        except:
            print('ERROR: Unable to connect to database')
            raise Exception('Unable to connect to database')

    def close(self):
        self.conn.close()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def get_error(self):
        return psycopg2.Error

def setup_preparedStatements():
    try:
        cursor=connection.get_cursor()
        cursor.execute('prepare insertClick as insert into sessionProjectClick values($1,$2)')
        cursor.execute('prepare insertSessionProjectClick as insert into sessionProjectClick values($1,$2)')
    except Exception as e:
        print('error while making prepared statements ' + str(e))
        connection.rollback()