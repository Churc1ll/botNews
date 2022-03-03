import requests
from bs4 import BeautifulSoup
import re
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

now = datetime.datetime.now()


def date():
    return '*' + ('0' + str(now.day) if len(str(now.day)) < 2 else str(now.day)) + '. ' + ('0' + str(now.month) if len(str(now.month)) < 2 else str(now.month)) + '*'


def parse(url, tag, details):
    response = requests.get(url, headers=headers)
    answer = BeautifulSoup(response.text, 'lxml')
    return answer.find_all(tag, details)


def corona():
    quote = parse(
        'https://coronavirus-monitorus.ru/moskva/',
        'sup',
        'new-cases'
    )[0]
    answ = re.findall(r'\d+', str(quote))
    return ' '.join(answ)


def dollar():
    quotes = parse(
        'https://cbr.ru/',
        'div',
        'col-md-2 col-xs-9 _right mono-num'
    )
    # quote = quotes[0]
    quote = quotes[1]
    # quote = quotes[0] if now.day % 2 != 0 or now.hour > 12 else quotes[1]
    sum = ''.join(re.findall(r'\d+', str(quote)[33:]))
    return '*' + sum[0:2] + ',' + sum[2:4] + '*'


def bitcoin():
    quote = parse(
        'https://www.rbc.ru/crypto/currency/btcusd',
        'span',
        'currencies__td__inner'
    )[1]
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ' ' + sum[2:5] + ',' + (sum[5:] if len(sum) > 6 else '00')


def weather():
    quote = parse(
        'https://www.gismeteo.ru/weather-moscow-4368/2-weeks/',
        'div',
        'widget-row-chart widget-row-chart-temperature-avg'
    )
    sum = ''.join(re.findall(
        r'(?<=unit unit_temperature_c).*', str(quote)))[2:4]
    return sum


def message():
    return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ: ' + dollar() + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()
