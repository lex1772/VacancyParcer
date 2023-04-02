import requests
import json
import os
from dotenv import load_dotenv


def configure():
    load_dotenv()


def hh_responce(text, num_of_results, experience):
    hh_url = 'https://api.hh.ru/vacancies'
    hh_params = {
        "text": text,
        "per_page": num_of_results,
        "experience": experience
    }
    return requests.get(hh_url, hh_params)


def sj_responce(keyword, num_of_results, experience):
    sj_url = "https://api.superjob.ru/2.0/vacancies/"
    sj_params = {
        "keyword": keyword,
        "experience": experience,
        "count": num_of_results,
    }
    configure()
    key = os.getenv('sj_api_key')
    sj_headers = {"X-Api-App-Id": key}
    return requests.get(sj_url, sj_params, headers=sj_headers)
