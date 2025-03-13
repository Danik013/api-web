import requests


def main():
    locations = ["Лондон", "svo", "Череповец"]
    params = {"TnqmM": "", "lang": "ru"}
    url_template = "https://wttr.in/{}"
    
    for location in locations:
        url = url_template.format(location)
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или параметры!")
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения при попытке получить данные.")
        except requests.exceptions.Timeout:
            print("Время ожидания истекло.")

if __name__ == '__main__':
    main()
        
