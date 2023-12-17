"""В данном модуле будут располагаться функции по
созданию и наполнению базы данных"""
import requests


def get_data():
    """
    Получает данные о работодателях и вакансиях с помощью API HeadHunter.

    Returns:
        employers_data_clean (list): Список списков, содержащих id и название работодателей.
        vacancies_data_clean (list): Список списков, содержащих название вакансии,
                                     название работодателя, минимальную зарплату,
                                     id работодателя и ссылку на вакансию.
    """
    employers_id = [
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
    all_employers = [
        requests.get(
            f"https://api.hh.ru/employers/{id}",
            params={
                'page': 0,
                'per_page': 10},
            timeout=5).json() for id in employers_id]

    employers_data_clean = [
        [i['id'], i['name']]
        for i in all_employers
    ]

    vacancies_url = "https://api.hh.ru/vacancies"
    params = {
        "employer_id": employers_id,
        "page": 0,
        "per_page": 100
    }
    vacancies_data = requests.get(vacancies_url, params=params, timeout=5).json()

    vacancies_data_clean = [
        [
            vacancy['name'],
            vacancy['employer']['name'],
            vacancy.get(
                'salary',
                {}).get('from'),
            vacancy['employer']['id'],
            vacancy['url']] for vacancy in vacancies_data.get(
            'items',
            []) if vacancy.get('salary') and vacancy.get('salary') != '']

    return employers_data_clean, vacancies_data_clean