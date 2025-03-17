import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(user_input, token):
    parsed = urlparse(user_input)
    pars_url = parsed.netloc
    if "vk.cc" in pars_url:
        shorten_url = user_input
        cliks_url = count_clicks(token, shorten_url)
        if cliks_url is not None:
            print("Количество переходов:", cliks_url)
    else:
        base_url = user_input
        shorten_url = shorten_link(token, base_url)
        if shorten_url is not None:
            print("Сокращенная ссылка: ", shorten_url)
 

def shorten_link(token, base_url):
    try:
        base_url_response = requests.get(base_url)
        base_url_response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Вы ввели неправильную ссылку или параметры!")
        return None
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения при попытке получить данные.")
        return None
    except requests.exceptions.Timeout:
        print("Время ожидания истекло.")
        return None
    except requests.exceptions.MissingSchema:
        print(f"Недопустимый URL-адрес. Возможно вы имели ввиду: https://{base_url}")
        return None
    vk_url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": token,
        "v": 5.199,
        "url": base_url
    }
    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    dict_response = response.json()
    short_link = dict_response["response"]["short_url"]
    return short_link
    

def count_clicks(token, shorten_url):    
    shorten_url_response = requests.get(shorten_url)
    shorten_url_response.raise_for_status()
    parsed = urlparse(shorten_url)
    pars_url = parsed.path
    key = pars_url.replace("/", "", 1)
    vk_stats = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": 5.199,
        "key": key
    }
    try:
        response_stats = requests.get(vk_stats, params=params)
        response_stats.raise_for_status()
        dict_stats = response_stats.json()
        clicks_count = dict_stats["response"]["stats"][0]["views"]
    except IndexError:
        print("Возможно ссылкой еще не пользовались!")
        return None
    return clicks_count


def main():
    load_dotenv()
    token = os.getenv("SERVICE_KEY")
    user_input = input("Введите ссылку: ")
    is_shorten_link(user_input, token)


if __name__ == '__main__':
    main()

