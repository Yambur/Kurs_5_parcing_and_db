# Курсовая № 5. Парсинг сайта HH и добавление в базу данных

## Что делает программа:
- Парсит нужные нам компании и вакансии в них
- Добавляет их данные в DB
- Делает выборку из базы данных

## Для работы вам потребуется:
- Убедится в установленной библиотеке psycopg2
- Убедится в установленной библиотеке requests

## Для работы вам необходимо подключиться к вашей базе данных
Для это в файле `database.ini` нужно ввести свои данные, где:
- `host` - хост вашей базы данных
- `user` - пользователь вашей базы данных
- `password` - пароль базы данных
- `port` - порт базы данных

## Как работает программа:

1. В файле `hh_api` парсим нам необходимое с помощью класса HH_vacancy, где в методе `get_companies` написаны id интересующих нас компаний и в методе `get_vacancies` вакансии к ним
2. В файле `dbmanager` создаем базу данных с помощью метода `create_tables` и далее есть методы для выборочной работы по базе данных, а именно
> get_companies_and_vacancies_count

Список компаний и количество вакансий у каждой компании
>get_all_vacancies

Возвращает все вакансии из базы данных
>get_avg_salary

Возвращает среднюю зарплату всех вакансий, где зарплата указана
>get_vacancies_with_higher_salary

Возвращает все вакансии, у которых зарплата выше средней зарплаты


 


