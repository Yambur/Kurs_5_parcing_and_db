import psycopg2


class DBManager:

    def __init__(self, params):
        self.params = params
        self.conn = psycopg2.connect(db_name='postgres', **self.params)

    def create_db(self) -> None:
        """Создание базы данных"""
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        cursor.execute('DROP DATABASE IF EXISTS hh')
        print('Удаляем старую базу данных')
        cursor.execute('CREATE DATABASE hh')
        print("Создали базу данных")
        cursor.close()
        self.conn.close()

    def create_tables(self):
        """Создание таблиц"""
        self.conn = psycopg2.connect(db_name='hh', **self.params)
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLES companies (
        id INTEGER PRIMARY KEY,
        company text,
        url_vacancies text)
        ''')
        cursor.execute('''
        CREATE TABLES vacancies (
        id INTEGER PRIMARY KEY,
        vacancy text,
        salary integer,
        url text,
        id_company int REFERENCES companies(id))
        ''')
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def connection_db(self):
        """Метод для подключения к БД"""
        return psycopg2.connect(db_name='hh', **self.params)

    def close_connection_db(self):
        """Метод для закрытия БД"""
        connection = self.connection_db()
        connection.close()

    def get_companies_and_vacancies_count(self):
        """Список компаний и количество вакансий у каждой компании."""
        cur = self.connection_db().cursor()
        cur.execute('''"SELECT employer, COUNT(*) AS vacancies_count FROM vacancies GROUP BY employer''')
        cur.close()
        return cur.fetchall

    def get_all_vacancies(self):
        """Возвращает все вакансии из базы данных."""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT * FROM vacancies''')
        return cur.fetchall

    def get_avg_salary(self):
        """Возвращает среднюю зарплату всех вакансий, где зарплата указана."""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT AVG(salary) AS avg_salary FROM vacancies WHERE salary IS NOT NULL''')
        return cur.fetchall

    def get_vacancies_with_higher_salary(self):
        """Возвращает все вакансии, у которых зарплата выше средней зарплаты."""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT * FROM vacancies WHERE salary > %s''')
        return cur.fetchall

    def get_vacancies_with_keyword(self, keyword):
        cur = self.connection_db().cursor()
        cur.execute(f'''SELECT * FROM vacancies WHERE vacancy_name LIKE "%{keyword}%"''')
        result = cur.fetchall()
        return result

    def insert_data(self, company):
        conn = self.connection_db()
        cur = conn.cursor()
        cur.execute(f'INSERT INTO companies (company, url_vacancies) VALUES ({company["company"]},{company["url_vacancies"]}) RETURNING id')
        data = cur.fetchone()
        for vacancy in company["vacancies"]:
            cur.execute(f'INSERT INTO vacancies (vacancy, salary, url, id_company) VALUES ({vacancy["vacancy"]},{vacancy["salary"]},{vacancy["url"]},{data[0]})')
        conn.commit()
        cur.close()
