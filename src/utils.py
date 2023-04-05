# Импортируем необходимые классы
from classes.classes import HH, Superjob, Vacancy


def user_interaction():
    """Функция для взаимодействия с пользователем, которая задает вопросы и на основании ответов пользователя выводит на экран вакансии, если они найдены, либо же отвечает, что по фильтрам вакансий нет"""
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
                    f"Введите цифру порядкового платформы: {', '.join(platforms)} "))
            flag = False

    flag = True
    while flag:
        try:
            count = int(input(f"Введите число для выгрузки массива вакансий: "))
        except ValueError:
            print("Принимаются только целые числа")
            continue
        else:
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
        except ValueError:
            print("Принимаются только целые числа от 1 до 3")
            continue
        else:
            while 0 < experience > 5:
                experience = int(input(
                    f"Введите цифру порядкового номера списка, который отражает ваш опыт работы: {', '.join(exp_list)} "))
            flag = False

    if platform_to_search == 1:
        hh = HH(search_query, experience, count)
        hh.get_request()
        vac = Vacancy(filter_words, top_n)
        vac.clear_vacancies()
        vac.vacancies_to_json(hh.elements_list)
        vac.get_vacancies()
    elif platform_to_search == 2:
        sj = Superjob(search_query, experience, count)
        sj.get_request()
        vac = Vacancy(filter_words, top_n)
        vac.clear_vacancies()
        vac.vacancies_to_json(sj.elements_list)
        vac.get_vacancies()
    else:
        hh = HH(search_query, experience, count)
        hh.get_request()
        sj = Superjob(search_query, experience, count)
        sj.get_request()
        vac = Vacancy(filter_words, top_n)
        vac.clear_vacancies()
        vac.vacancies_to_json(hh.elements_list, sj.elements_list)
        vac.get_vacancies()

    vac.clear_vacancies()
