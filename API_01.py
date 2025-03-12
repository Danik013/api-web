import requests


def main():
    locations = ["Лондон", "svo", "Череповец"]
    params = {"TnqmM": "", "lang": "ru"}
    url_template = "https://wttr.in/{}"
    
    for location in locations:
        url = url_template.format(location)
        response = requests.get(url, params)
        response.raise_for_status()
        decoder_response = response.text
        try:
            if not "error" in decoder_response:
                print(response.text)
        except:
            raise requests.exceptions.HTTPError(decoded_response['error'])


if __name__ == '__main__':
    main()
        
