import os
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

    @classmethod
    def json_saver(cls, element):
        with open("vacancies.json", "a", encoding="utf-8") as file:
            json.dump(element, file)


class HH(Engine):
    def get_request(self):
        resp = hh_responce
        if resp.status_code == 200:
            vacancies = resp.json()["items"]
            for vacancy in vacancies:
                url_response = requests.get(vacancy["url"])
                details = url_response.json()
                element = {"name": details.get("name"), "salary": details.get("salary"),
                           "experience": details["experience"]["name"],
                           "description": details["description"].replace('<ul> <li>', '\n').replace('<p>', ''),
                           "url": details["alternate_url"]}
                try:
                    details["address"]["metro"]["station_name"]
                except TypeError:
                    element["metro"] = "Не указано"
                else:
                    element["metro"] = details["address"]["metro"]["station_name"]
                try:
                    details["address"]["raw"]
                except TypeError:
                    element["address"] = "Не указано"
                else:
                    element["address"] = details["address"]["raw"]
                self.json_saver(element)
        else:
            print("Error:", resp.status_code)


class Superjob(Engine):
    def get_request(self):
        resp = sj_responce
        if resp.status_code == 200:
            vacancies = resp.json()['objects']
            for vacancy in vacancies:
                element = {"name": vacancy.get('profession'),
                           "salary": {"from": vacancy.get('payment_from'), "to": vacancy.get('payment_to')},
                           "experience": vacancy['experience']['title'], "description": vacancy.get("candidat"),
                           "url": vacancy.get('link'), "metro": vacancy.get('metro'), "address": vacancy.get('address')}
                self.json_saver(element)
        else:
            print("Error:", resp.status_code)
