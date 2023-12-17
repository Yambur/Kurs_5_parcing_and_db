import requests
import json


class HH_vacancy():
    HH_URL = "https://api.hh.ru/vacancies"
    HH_COMPANY = "https://api.hh.ru/employers"
    HH_AREAS = "https://api.hh.ru/suggests/areas"
    company_id = 'id_companies.json'

    def get_company_id(self):
        company_id_list = []
        with open(self.company_id) as file:
            company_json = json.load(file)
            for company in company_json:
                company_id_list.append(company['id'])
        return company_id_list

    def get_company_name(self):
        company_name_list = []
        with open(self.company_id) as file:
            company_json = json.load(file)
            for company in company_json:
                company_name_list.append(company['name'])
        return company_name_list

    def get_vacancy(self):
        vacancy_list = []
        params = {
            'employer_id': 1740,
            'per_page': 10,
            'only_with_salary': True,
        }
        response = requests.get(self.HH_URL, params)
        if response.status_code == 200:
            vacancies = response.json()
            for item in vacancies['items']:
                if item['salary']['from']:
                    vacancy_list.append(item)
        for vacancy in vacancy_list:
            print(vacancy)


hh = HH_vacancy()
hh.get_vacancy()