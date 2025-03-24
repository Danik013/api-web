import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(user_input, token):
    url_elements = urlparse(user_input)
    path_url = url_elements.path
    vk_stats = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": 5.199,
        "key": path_url.replace("/", "", 1)
    }
    response = requests.get(vk_stats, params=params)
    response.raise_for_status()
    link_info = response.json()
    return "response" in link_info


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
    link_info = response.json()
    short_link = link_info["response"]["short_url"]
    return short_link
    

def count_clicks(token, shorten_url):    
    url_elements = urlparse(shorten_url)
    path_url = url_elements.path
    vk_stats = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": 5.199,
        "key": path_url.replace("/", "", 1)
    }
    response = requests.get(vk_stats, params=params)
    response.raise_for_status()
    link_info = response.json()
    clicks_count = link_info["response"]["stats"][0]["views"]
    return clicks_count


def main():
    load_dotenv()
    token = os.environ["VK_SERVICE_KEY"]
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
        except requests.exceptions.HTTPError as http_err:
            print(f"Вы ввели неправильную ссылку или параметры. Ошибка: {http_err}")
        except requests.exceptions.ConnectionError as err:
            print(f"Ошибка соединения: {err}")
        except requests.exceptions.Timeout as time_err:
            print(f"Время ожидания истекло: {time_err}")
        except requests.exceptions.MissingSchema:
            print(f"Недопустимый URL-адрес. Возможно вы имели ввиду: https://{user_input}")
    

if __name__ == '__main__':
    main()