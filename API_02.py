import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(user_input, token):
    url_elements = urlparse(user_input)
    domaine_name = url_elements.path
    vk_stats = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": 5.199,
        "key": domaine_name.replace("/", "", 1)
    }
    response = requests.get(vk_stats, params=params)
    response.raise_for_status()
    keys_response = response.json()
    return "response" in keys_response


def shorten_link(token, base_url):
    base_url_response = requests.get(base_url)
    vk_url = "https://api.vk.ru/method/utils.getShortLink"
    params = {
        "access_token": token,
        "v": 5.199,
        "url": base_url
    }
    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    keys_response = response.json()
    short_link = keys_response["response"]["short_url"]
    return short_link
    

def count_clicks(token, shorten_url):    
    shorten_url_response = requests.get(shorten_url)
    shorten_url_response.raise_for_status()
    url_elements = urlparse(shorten_url)
    domaine_name = url_elements.path
    vk_stats = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": 5.199,
        "key": domaine_name.replace("/", "", 1)
    }
    response = requests.get(vk_stats, params=params)
    response.raise_for_status()
    keys_response = response.json()
    clicks_count = keys_response["response"]["stats"][0]["views"]
    return clicks_count


def main():
    load_dotenv()
    token = os.environ.get("VK_SERVICE_KEY", "KeyError: 'SOME_KEY'")
    user_input = input("Введите ссылку: ")
    if is_shorten_link(user_input, token):
        try:
            clicks_count = count_clicks(token, user_input)
            print( "Количество переходов:", clicks_count)
        except IndexError:
            print("Возможно ссылкой еще не пользовались!")
    else:
        try:
            shorten_url = shorten_link(token, user_input)
            print("Сокращенная ссылка: ", shorten_url)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или параметры!")
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения при попытке получить данные.")
        except requests.exceptions.Timeout:
            print("Время ожидания истекло.")
        except requests.exceptions.MissingSchema:
            print(f"Недопустимый URL-адрес. Возможно вы имели ввиду: https://{user_input}")
    

if __name__ == '__main__':
    main()