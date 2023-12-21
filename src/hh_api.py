import requests
import json


class HH_vacancy():
    HH_COMPANY = "https://api.hh.ru/employers"
    """Получает данные о работодателях и вакансиях с помощью API HeadHunter."""

    def get_companies(self):
        info_companies = []
        company_id_list = [
            78191,
            1122462,
            906391,
            4934,
            1740,
            3529,
            5060211,
            5928535,
            1711204,
            1776381]
        for company in company_id_list:
            responce = requests.get(self.HH_COMPANY + f'/{company}')
            data = responce.json()
            info_companies.append(
                {
                    'company': data['name'],
                    'url_vacancies': data['vacancies_url']
                }
            )
        return info_companies

    def get_vacancies(self):
        companies = self.get_companies()
        for company in companies:
            url = company['url_vacancies']
            responce = requests.get(url)
            data = responce.json()
            vacancies = data.get('items')
            company['vacancies'] = []
            if vacancies:
                for vacancy in vacancies:
                    company['vacancies'].append(
                        {
                            'vacancy': vacancy['name'],
                            'url': vacancy['alternate_url'],
                            'salary': vacancy['salary']['from'] if vacancy.get('salary') else 0
                        }
                    )
        return companies
