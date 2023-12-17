import psycopg2


class DBManager:



    def __init__(self, db_name, user, password, host, port):
        self.conn = psycopg2.connect(db_name=db_name,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)

    def create_db(self) -> None:
        """Создание базы данных"""
        connector = psycopg2.connect(dbname='postgres', db_name=self.db_name,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port)
        connector.autocommit = True
        cursor = connector.cursor()

        try:
            cursor.execute(f'DROP DATABASE {self.db_name}')
            print('Удаляем старую базу данных')
        except psycopg2.errors.InvalidCatalogName:
            print('Создаём новую базу данных')
        finally:
            cursor.execute(f'CREATE DATABASE {self.db_name}')
            cursor.close()
            connector.close()

    def get_companies_and_vacancies_count(self):
        cur = self.conn.cursor()
        cur.execute('''"SELECT employer, COUNT(*) AS vacancies_count FROM vacancies GROUP BY employer''')
        cur.close()
        return cur.fetchall

    def get_all_vacancies(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM vacancies''')
        return cur.fetchall

    def get_avg_salary(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT AVG(salary) AS avg_salary FROM vacancies WHERE salary IS NOT NULL''')
        return cur.fetchall

    def get_vacancies_with_higher_salary(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM vacancies WHERE salary > %s''')
        return cur.fetchall

    def get_vacancies_with_keyword(self, keyword, cur):
        cur.execute(f'''SELECT * FROM vacancies WHERE vacancy_name LIKE "%{keyword}%"''')
        result = cur.fetchall()
        return result