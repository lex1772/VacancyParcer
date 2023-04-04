import requests
import json
import os
from dotenv import load_dotenv


def configure():
    load_dotenv()


def __hh_responce(search_query, top_n, experience):
    if experience == 1:
        experience = "noExperience"
    elif experience == 2:
        experience = "between1And3"
    elif experience == 3:
        experience = "between3And6"
    else:
        experience = "moreThan6"
    hh_url = 'https://api.hh.ru/vacancies'
    hh_params = {
        "text": search_query,
        "per_page": top_n,
        "experience": experience
    }
    return requests.get(hh_url, hh_params)


def __sj_responce(search_query, top_n, experience):
    sj_url = "https://api.superjob.ru/2.0/vacancies/"
    sj_params = {
        "keyword": search_query,
        "experience": experience,
        "count": top_n,
    }
    configure()
    key = os.getenv('sj_api_key')
    sj_headers = {"X-Api-App-Id": key}
    return requests.get(sj_url, sj_params, headers=sj_headers)


def user_interaction():
    platforms = ["1) HeadHunter", "2) SuperJob", "3) Обе платформы"]
    exp_list = ["1) Без опыта", "2) От 1 года", "3) От 3 лет", "4) От 6 лет"]
    flag = True
    while flag:
        try:
            platform_to_search = int(input(
                f"Введите цифрой номер платформы из списка: {', '.join(platforms)} "))
        except ValueError:
            print("Принимаются только целые числа")
            continue
        else:
            while 0 < platform_to_search > 4:
                experience = int(input(
                    f"Введите цифру порядкового номера списка, который отражает ваш опыт работы: {', '.join(platforms)} "))
            flag = False
    search_query = input("Введите поисковый запрос: ")
    flag = True
    while flag:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        except ValueError:
            print("Принимаются только целые числа")
            continue
        else:
            flag = False
    filter_words = input("Введите ключевые слова для фильтрации вакансий через запятую: ").split(",")
    flag = True
    while flag:
        try:
            experience = int(input(
                f"Введите цифру порядкового номера списка, который отражает ваш опыт работы: {', '.join(exp_list)} "))
            while 0 < experience < 5:
                experience = int(input(
                    f"Введите цифру порядкового номера списка, который отражает ваш опыт работы: {', '.join(exp_list)} "))
        except ValueError:
            print("Принимаются только целые числа от 1 до 3")
            continue
        else:
            while 0 < experience > 4:
                experience = int(input(
                    f"Введите цифру порядкового номера списка, который отражает ваш опыт работы: {', '.join(exp_list)} "))
            flag = False
    if platform_to_search == 1:
        __hh_responce(search_query, top_n, experience)
    elif platform_to_search == 2:
        __sj_responce(search_query, top_n, experience)
    else:
        __hh_responce(search_query, top_n, experience)
        __sj_responce(search_query, top_n, experience)
