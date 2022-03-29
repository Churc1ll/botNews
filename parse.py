import requests
from bs4 import BeautifulSoup
import re
from datetime import date

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

def parse(url, tag, details):
    response = requests.get(url, headers=headers)
    answer = BeautifulSoup(response.text, 'lxml')
    return answer.find_all(tag, details)


def coronaMoscow():
    quote = parse(
        'https://coronavirus-monitorus.ru/moskva/',
        'sup',
        'new-cases'
    )[0]
    answ = re.findall(r'\d+', str(quote))
    return ' '.join(answ)

def coronaRF():
    quote = parse(
        'https://coronavirus-monitorus.ru/v-rossii/',
        'b',
        ''
    )
    quote=str(quote).split(',')[1]
    return ''.join(re.findall(r'\d+\W\d+',quote ))

def dollarCB():
    quotes = parse(
        'https://finance.rambler.ru/currencies/USD/',
        'div',
        'finance-currency-plate__currency'
    )[1]
    sum = ''.join((str(quotes)[47:53]))
    return sum[0:2] + ',' + sum[3:5]

def dollarMarket():
    quotes = []
    # while quotes == []:
    quotes = parse(
        'https://quote.rbc.ru/ticker/59111',
        'span',
        'chart__info__sum',
    )
    return ''.join(re.findall(r'\d+\W\d\d', str(quotes)))

def dollarAliExpress():
  quotes = parse(
    'https://helpix.ru/currency/',
    'td',
    'b-tabcurr__td',
  )
  quotes = str(quotes).split(',')[2]
  return ''.join(re.findall(r'\d+\W\d+', str(quotes)))

def bitcoin():
    quote = parse(
        'https://www.google.com/finance/quote/BTC-USD',
        'div',
        'YMlKec fxKbKc'
    )
    sum = ''.join(re.findall(r'\d+', str(quote)))
    return sum[0:2] + ' ' + sum[2:5] + ',' + (sum[5:] if len(sum) > 6 else '00')

def weather():
    quote = parse(
        'https://www.gismeteo.ru/weather-moscow-4368/2-weeks/',
        'div',
        'widget-row-chart widget-row-chart-temperature-avg'
    )

    sum = re.findall(r'(?<=unit unit_temperature_c">)(−\d+|\d+)', str(quote))[0]
    return sum

def message():
#     return f'''
# *{date.today():%d.%m}_

# __Курс доллара__
# ЦБ: *{dollarCB()}$*
# Биржа: *{dollarMarket()}$*
# AliExpress:*{dollarAliExpress()}*$

# Курс биткойна: *{bitcoin()}*$

# Новые случаи короновируса 
# в Москве / России, человек:
# *{coronaMoscow()}* / *{coronaRF()}*

# Среднесуточная температура: *{weather()}*\u00B0
# '''.strip()
    return f''' 
*{date.today():%d.%m.%y}*

__Курс доллара__
ЦБ: *{dollarCB()}$*

AliExpress:*{dollarAliExpress()}*$

Курс биткойна: *{bitcoin()}*$

Новые случаи короновируса 
в Москве / России, человек:
*{coronaMoscow()}* / *{coronaRF()}*

Среднесуточная температура: *{weather()}*\u00B0
'''.strip()

    # return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на сегодня: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$' 

    # if now.hour > 15:
    #     # and now.weekday() <= 4:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на завтра: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

    # if now.weekday() > 4:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на понедельник: ' + dollar() + '\u20BD\nСтоимость 1$ на Aliexpress: ' + '*' + aliexpress() + '*' + ' \u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

    # else:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на завтра: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()

print(message)