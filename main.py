import os
from src.config import config
from src.dbmanager import DBManager
from src.hh_api import HH_vacancy

params = config(filename=os.path.abspath('database.ini'))
db = DBManager(params)
db.create_db()
db.create_tables()
hh = HH_vacancy()
company_vacancies = hh.get_vacancies()

for company in company_vacancies:
    db.insert_data(company)
print(db.get_companies_and_vacancies_count())
print(db.get_all_vacancies())
print(db.get_avg_salary())
print(db.get_vacancies_with_higher_salary())
keyword = input('Введите ключевое слово ')
print(db.get_vacancies_with_keyword(keyword))