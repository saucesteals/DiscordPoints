import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb as m

class MySQLUtil():
    def __init__(self):
        self.db = None

    def connect_db(self):
        self.db = pymysql.connect(host='na05-sql.pebblehost.com', user='customer_197460_starbase',
                                  password='$$f9S#1kAgi1fQJcf47b', db='customer_197460_starbase', port=3306)

    def close_db(self):
        self.db.close()

    def exec_query(self, sql):
        try:
            # execute sql statement
            cursor = self.db.cursor()
            cursor.execute(sql)
            # get all rows in mysql
            results = cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")
            return None

    def exec_sql(self, sql):
        # sql is insert, delete or update statement
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            # commit sql to mysql
            self.db.commit()
            cursor.close()
            return True
        except:
            self.db.rollback()
        return False