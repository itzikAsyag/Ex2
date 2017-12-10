import psycopg2
from configparser import ConfigParser

class DB:

    def __init__(self):
        self._conn = None
        self._cur = None

    def config(self,filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self._conn = psycopg2.connect(**params)

            # create a cursor
            self._cur =  self._conn.cursor()

            """# execute a statement
            print('PostgreSQL database version:')
            self._cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self._cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            #"""
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def execute(self, statment, args=None):
        if args is None:
            self._cur.execute(statment)
            # row = self._cur.fetchone()
            # while row is not None:
            #     row = self._cur.fetchone()
            rows = self._cur.fetchall()
            print(rows)
            return rows
        else:
            self._cur.execute(statment, args)
            self._conn.commit()
            if statment[:6] != "UPDATE":
                res = self._cur.fetchone()
                return res[0]

    def disconnect(self):
        if self._conn is not None:
            self._cur.close()
            self._conn.close()
            print('Database connection closed.')



