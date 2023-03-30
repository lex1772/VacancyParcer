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
        if hh_responce.status_code == 200:
            vacancies = hh_responce.json()["items"]
            for vacancy in vacancies:
                print(vacancy["name"], vacancy["url"], vacancy["salary"])
        else:
            print("Error:", hh_responce.status_code)


class Superjob(Engine):
    def get_request(self):
        if sj_responce.status_code == 200:
            vacancies = sj_responce.json()["items"]
            for vacancy in vacancies:
                #print(vacancy["name"], vacancy["url"], vacancy["salary"])
                print(vacancy)
        else:
            print("Error:", sj_responce.status_code)
