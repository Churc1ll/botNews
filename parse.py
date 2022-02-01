import requests
from bs4 import BeautifulSoup
import re
import datetime

def date():
    now = datetime.datetime.now()
    # print(str(now.month))
    return ('0' + str(now.day) if len(str(now.day)) < 2 else str(now.day)) + '. ' + ('0' + str(now.month) if len(str(now.month)) < 2 else str(now.month)) 

print(date())

def parse(url, tag, details):
    response = requests.get(url)
    answer = BeautifulSoup(response.text, 'lxml')
    return answer.find_all(tag, details)


def corona():
    quote = parse(
        'https://coronavirus-control.ru/',
        'span',
        'rednum'
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
        'https://www.banki.ru/products/currency/usd/',
        'div',
        'currency-table__large-text'
    )[0]
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ',' + sum[2:]


def message():
    return 'За *' + date() + '* количество зараженных по Москве:  *' + corona() + '*' + ' человек\n\nКурс доллара: ' + '*' + dollar() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()

# print (message)