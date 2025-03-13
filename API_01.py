import requests


def main():
    locations = ["Лондон", "svo", "Череповец"]
    params = {"TnqmM": "", "lang": "ru"}
    url_template = "https://wttr.in/{}"
    
    for location in locations:
        url = url_template.format(location)
        response = requests.get(url, params)
        try:
            response.raise_for_status()
            if not "error" in response.text:
                print(response.text)
            else:
                raise requests.exceptions.HTTPError(response.text['error'])
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или параметры!")

if __name__ == '__main__':
    main()
        
