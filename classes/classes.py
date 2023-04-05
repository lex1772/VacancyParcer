# делаем необходимые импорты для работы
import os
from abc import ABC, abstractmethod
import json
import requests
from dotenv import load_dotenv


class Engine(ABC):
    '''Создаем абстрактный класс для работы с платформами'''
    elements_list = list()

    @abstractmethod
    def get_request(self):
        """Абстрактный метод для отправки запроса на сайт"""
        pass

    def to_list(self, element):
        """Функция для добавления элементов в общий список"""
        self.elements_list.append(element)

    def check_to_list(self, element):
        """Функция для проверки элементов в списке"""
        if element in self.elements_list:
            pass
        else:
            self.to_list(element)

    @staticmethod
    def configure():
        """Функция для загрузки API ключа"""
        load_dotenv()


class HH(Engine):
    """Класс для работы с платформой HeadHunter"""

    def __init__(self, search_query, experience, count):
        """Инициализация, которая принимает поисковый запрос и опыт работы"""
        self.search_query = search_query
        self.experience = experience
        self.count = count

    def hh_responce(self):
        """Функция для отправки запроса на платформу HeadHunter"""
        if self.experience == 1:
            experience = "noExperience"
        elif self.experience == 2:
            experience = "between1And3"
        elif self.experience == 3:
            experience = "between3And6"
        else:
            experience = "moreThan6"

        hh_url = 'https://api.hh.ru/vacancies'
        hh_params = {
            "text": self.search_query,
            "per_page": self.count,
            "experience": experience
        }

        return requests.get(hh_url, hh_params)

    def get_request(self):
        """Функция для получения данных с платформы HeadHunter. Получаем название, зарплату, ссылку, адрес и метро, либо выдаем ошибку, если нет подключения"""
        resp = self.hh_responce()

        if resp.status_code == 200:
            vacancies = resp.json()["items"]

            for vacancy in vacancies:
                element = {"name": vacancy.get("name"), "salary": {"from": 0, "to": 0},
                           "url": vacancy["alternate_url"], "salary_to_sort": 0}

                try:
                    vacancy["address"]["metro"]["station_name"]
                except TypeError:
                    element["metro"] = "Не указано"
                else:
                    element["metro"] = vacancy["address"]["metro"]["station_name"]

                try:
                    vacancy["address"]["raw"]
                except TypeError:
                    element["address"] = "Не указано"
                else:
                    element["address"] = vacancy["address"]["raw"]

                try:
                    element["salary_to_sort"] = vacancy["salary"]["from"]
                except TypeError:
                    element["salary"]["from"] = 0
                else:
                    element["salary"]["from"] = vacancy["salary"]["from"]
                    try:
                        vacancy["salary"]["to"]
                    except TypeError:
                        element["salary"]["to"] = "Не указано"
                    else:
                        if element["salary"]["to"] is not None:
                            if element["salary"]["to"] > 0:
                                element["salary_to_sort"] = vacancy["salary"]["to"]
                if element["salary_to_sort"] is None:
                    element["salary_to_sort"] = 0

                try:
                    description = f'{vacancy["snippet"]["requirement"]}. {vacancy["snippet"]["responsibility"]}'
                    element["description"] = description
                except TypeError:
                    try:
                        element["description"] = vacancy["snippet"]["responsibility"]
                    except TypeError:
                        element["description"] = "Не указано"
                    else:
                        description = f'{vacancy["snippet"]["requirement"].replace("<highlighttext>", "").replace("</highlighttext>", "")}. {vacancy["snippet"]["responsibility"]}'
                        element["description"] = description

                if self.experience == 1:
                    element["experience"] = "Без опыта"
                elif self.experience == 2:
                    element["experience"] = "От 1 года"
                elif self.experience == 3:
                    element["experience"] = "От 3 лет"
                else:
                    element["experience"] = "От 6 лет"

                self.check_to_list(element)

        else:
            print("HH Error:", resp.status_code)


class Superjob(Engine):
    """Класс для работы с платформой HeadHunter"""

    def __init__(self, search_query, experience, count):
        """Инициализация, которая принимает поисковый запрос и опыт работы"""
        self.search_query = search_query
        self.experience = experience
        self.count = count

    def sj_responce(self):
        """Функция для отправки запроса на платформу HeadHunter"""
        sj_url = "https://api.superjob.ru/2.0/vacancies/"
        sj_params = {
            "keyword": self.search_query,
            "experience": self.experience,
            "count": int(self.count),
        }

        self.configure()

        key = os.getenv('sj_api_key')
        sj_headers = {"X-Api-App-Id": key}

        return requests.get(sj_url, sj_params, headers=sj_headers)

    def get_request(self):
        """Функция для получения данных с платформы HeadHunter. Получаем название, зарплату, ссылку, адрес и метро, либо выдаем ошибку, если нет подключения"""
        resp = self.sj_responce()
        if resp.status_code == 200:
            vacancies = resp.json()['objects']
            for vacancy in vacancies:
                element = {"name": vacancy.get('profession'),
                           "salary": {"from": vacancy.get('payment_from'), "to": vacancy.get('payment_to')},
                           "experience": vacancy['experience']['title'],
                           "description": vacancy.get("candidat"),
                           "url": vacancy.get('link'), "metro": vacancy.get('metro', "Не указано"),
                           "address": vacancy.get('address',
                                                  "Не указан")}
                try:
                    element["salary_to_sort"] = vacancy["payment_from"]
                except TypeError:
                    element["salary"]["from"] = 0
                else:
                    element["salary"]["from"] = vacancy["payment_from"]
                    try:
                        vacancy["payment_to"]
                    except TypeError:
                        element["salary"]["payment_to"] = "Не указано"
                    else:
                        if element["salary"]["to"] is not None:
                            if element["salary"]["to"] > 0:
                                element["salary_to_sort"] = vacancy["payment_to"]
                    if element["salary_to_sort"] is None:
                        element["salary_to_sort"] = 0
                try:
                    element["metro"] = vacancy["metro"][0]["title"]
                except TypeError:
                    element["metro"] = "Не указано"
                except IndexError:
                    try:
                        element["metro"] = vacancy["metro"]["title"]
                    except TypeError:
                        element["metro"] = "Не указано"
                self.to_list(element)

        else:
            print("Superjob Error:", resp.status_code)


class Vacancy:
    """Класс для обработки вакансий в Json формате"""

    def __init__(self, filter_words, top_n):
        """Инициализация, которая принимает слова для фильтра и список отображаемых вакансий"""
        self.filter_words = filter_words
        self.top_n = top_n

    def vacancies_to_json(self, element_list, element_list2=None):
        """Функция для создания Json файла из двух списков"""
        list_for_vacancy = []

        if element_list2 is None:
            for i in element_list:
                if i not in list_for_vacancy:
                    list_for_vacancy.append(i)
                else:
                    pass

        else:
            for i in element_list:
                if i not in list_for_vacancy:
                    list_for_vacancy.append(i)
                else:
                    pass

            for j in element_list2:
                if j not in list_for_vacancy:
                    list_for_vacancy.append(j)
                else:
                    pass

        with open("vacancies.json", "a") as file:
            json.dump(list_for_vacancy, file)

    def get_vacancies(self):
        """Функция для получения вакансий из файла Json и отображения на экран данных по запросу"""
        with open("vacancies.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            vacancy_list = []
            sorted_data = sorted(data, key=lambda x: x['salary_to_sort'], reverse=True)

            for i in range(len(sorted_data)):
                counter = 0
                vacancy_count = 0
                for j in self.filter_words:
                    if j.lower() in sorted_data[i]["description"].lower():
                        counter += 1
                        if counter == len(self.filter_words):
                            vacancy_list.append(sorted_data[i])

            if len(vacancy_list) == 0:
                print("Нет вакансий, соответствующих заданным критериям.")

            elif len(vacancy_list) <= self.top_n:
                for vacancy in vacancy_list:
                    vacancy_count += 1
                    print(
                        f"{vacancy_count}) Вакансия: {vacancy['name']}\nЗарплата: от {vacancy['salary']['from']} до {vacancy['salary']['to']}\nОпыт: {vacancy['experience']}\nОписание: {vacancy['description']}\nМетро: {vacancy['metro']}\nАдрес: {vacancy['address']}\nСсылка: {vacancy['url']}\n")

            else:
                for i in range(self.top_n):
                    print(
                        f"{i + 1}) Вакансия: {vacancy_list[i]['name']}\nЗарплата: от {vacancy_list[i]['salary']['from']} до {vacancy_list[i]['salary']['to']}\nОпыт: {vacancy_list[i]['experience']}\nОписание: {vacancy_list[i]['description']}\nМетро: {vacancy_list[i]['metro']}\nАдрес: {vacancy_list[i]['address']}\nСсылка: {vacancy_list[i]['url']}\n")

    def clear_vacancies(self):
        """Функция для очистки файла"""
        with open("vacancies.json", "w", encoding="utf-8") as file:
            pass
