import requests
from bs4 import BeautifulSoup
import re
import datetime

now = datetime.datetime.now()
def date():
    return '*' + ('0' + str(now.day) if len(str(now.day)) < 2 else str(now.day)) + '. ' + ('0' + str(now.month) if len(str(now.month)) < 2 else str(now.month)) + '*'


def parse(url, tag, details):
    response = requests.get(url)
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
    return quote


def dollar():
    quotes = parse(
        'https://cbr.ru/',
        'div',
        'col-md-2 col-xs-9 _right mono-num'
    )

    quote = quotes[0] if now.day%2 != 0 or now.hour > 12 else quotes[1]
    sum = ''.join(re.findall(r'\d+', str(quote)[33:]))
    # return quotes
    return '*' + sum[0:2] + ',' + sum[2:4] + '*'


def bitcoin():
    quote = parse(
        'https://www.rbc.ru/crypto/currency/btcusd',
        'span',
        'currencies__td__inner'
    )[1]
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ' ' + sum[2:5] + ',' + (sum[5:] if len(sum) > 6 else '00')


def message():
    return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\n\nКурс доллара: ' + dollar() + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

print(dollar())
print(message())
message = message()