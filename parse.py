import requests
from bs4 import BeautifulSoup
import re
import datetime


def date():
    now = datetime.datetime.now()
    return '0' + str(now.day) if len(str(now.day)) < 2 else str(now.day) + '. ' + '0' + str(now.month) if len(str(now.month)) < 2 else str(now.month) + ' ' + now.hour


def parse(url, tag, details):
    response = requests.get(url)
    answer = BeautifulSoup(response.text, 'lxml')
    return answer.find_all(tag, details)


def corona():
    quote = parse(
        'https://coronavirus-monitorus.ru/moskva/',
        'sup',
        ''
    )[0]
    answ = re.findall(r'\d+', str(quote))
    return ' '.join(answ)


def bitcoin():
    quote = parse(
        'https://www.rbc.ru/crypto/currency/btcusd',
        'span',
        'currencies__td__inner'
    )[1]
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ' ' + sum[2:5] + ',' + (sum[5:] if len(sum) > 6 else '00')


def dollar():
    quote = parse(
        'https://quote.rbc.ru/ticker/72413',
        'span',
        'chart__info__sum'
    )
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ',' + sum[2:]


def message():
    return 'За *' + date() + '* количество зараженных по Москве:  *' + corona() + '*' + ' человек\n\nКурс доллара: ' + '*' + dollar() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()
