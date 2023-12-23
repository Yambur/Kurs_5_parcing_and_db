import psycopg2


class DBManager:

    def __init__(self, params):
        self.params = params
        self.conn = psycopg2.connect(dbname='postgres', **self.params)

    def create_db(self) -> None:
        """Создание базы данных"""
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        cursor.execute('DROP DATABASE IF EXISTS hh')
        print('Удаляем старую базу данных')
        cursor.execute('CREATE DATABASE hh')
        print("Создали базу данных")
        self.conn.close()

    def create_tables(self):
        """Создание таблиц"""
        self.conn = psycopg2.connect(dbname='hh', **self.params)
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE companies (
        id SERIAL PRIMARY KEY,
        company text,
        url_vacancies text)
        ''')
        cursor.execute('''
        CREATE TABLE vacancies (
        id SERIAL PRIMARY KEY,
        vacancy text,
        salary integer,
        url text,
        id_company int REFERENCES companies(id))
        ''')
        self.conn.commit()
        self.conn.close()

    def connection_db(self):
        """Метод для подключения к БД"""
        return psycopg2.connect(dbname='hh', **self.params)

    def close_connection_db(self):
        """Метод для закрытия БД"""
        connection = self.connection_db()
        connection.close()

    def get_companies_and_vacancies_count(self):
        """Список компаний и количество вакансий у каждой компании"""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT c.id, c.company, c.url_vacancies, COUNT(v.id) AS vacancy_count
        FROM companies c
        LEFT JOIN vacancies v ON c.id = v.id_company
        GROUP BY c.id, c.company, c.url_vacancies;''')
        return cur.fetchall()

    def get_all_vacancies(self):
        """Возвращает все вакансии из базы данных"""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT * FROM vacancies''')
        return cur.fetchall()

    def get_avg_salary(self):
        """Возвращает среднюю зарплату всех вакансий, где зарплата указана"""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL''')
        return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Возвращает все вакансии, у которых зарплата выше средней зарплаты"""
        cur = self.connection_db().cursor()
        cur.execute('''SELECT * 
        FROM vacancies 
        WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL)''')
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        cur = self.connection_db().cursor()
        cur.execute(f'''SELECT * FROM vacancies WHERE vacancy LIKE \'%{keyword}%\'''')
        result = cur.fetchall()
        return result

    def insert_data(self, company):
        conn = self.connection_db()
        cur = conn.cursor()
        query = "INSERT INTO companies (company, url_vacancies) VALUES (%s, %s) RETURNING id"
        cur.execute(query, (company["company"], company["url_vacancies"]))
        data = cur.fetchone()
        for vacancy in company["vacancies"]:
            query = "INSERT INTO vacancies (vacancy, salary, url, id_company) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (vacancy["vacancy"], vacancy["salary"], vacancy["url"], data))
        conn.commit()
        cur.close()
