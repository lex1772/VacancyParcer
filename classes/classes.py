from abc import ABC, abstractmethod
import json
import requests
from src.utils import hh_responce, sj_responce


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def get_request(self):
        resp = hh_responce("Россия, Python", 30, "noExperience")
        if resp.status_code == 200:
            vacancies = resp.json()["items"]
            for vacancy in vacancies:
                url_response = requests.get(vacancy["url"])
                details = url_response.json()
                print(details["name"], details["salary"], details["experience"]["name"], details["alternate_url"])
        else:
            print("Error:", resp.status_code)


class Superjob(Engine):
    def get_request(self):
        resp = sj_responce("Python", 30, 1)
        if resp.status_code == 200:
            vacancies = resp.json()['objects']
            for vacancy in vacancies:
                print(vacancy['profession'], vacancy['payment_from'], vacancy['payment_to'],
                      vacancy['experience']['title'], vacancy['link'])
        else:
            print("Error:", resp.status_code)
