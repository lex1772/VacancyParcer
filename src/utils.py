import requests
import json

hh_url = 'https://api.hh.ru/vacancies'
hh_params = {
    "text": "Россия, Python",
    "per_page": 30,
    "experience": "noExperience"
}
hh_responce = requests.get(hh_url, hh_params)


sj_api_key = "v3.r.125158146.40ad8f59cf58107a6d7707908769627d3a0ff52d.671b9890809fb96e83bc555f9370614a6547ff33"
sj_url = "https://api.superjob.ru/2.0/vacancies/"
sj_params = {
    "keyword": "Python",
    "c": [1],
    "experience": 1,
    "count": 100,
    }
sj_headers = {"X-Api-App-Id": sj_api_key}
sj_responce = requests.get(sj_url, sj_params, headers=sj_headers)
