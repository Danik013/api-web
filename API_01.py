import requests


url_template = 'https://wttr.in/{}?TnqmM&lang=ru'
url_london = url_template.format("Лондон")
url_sheremetyevo_airport = url_template.format("svo")
url_cherepovets = url_template.format("Череповец")
response_london = requests.get(url_london)
response_sheremetyevo_airport = requests.get(url_sheremetyevo_airport)
response_cherepovets = requests.get(url_cherepovets)

print(response_london.text)
print(response_sheremetyevo_airport.text)
print(response_cherepovets.text)