import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import yaml
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

today=date.today().strftime('%d.%m')

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
    return ''.join(re.findall(r'>*\d\d\D\d\d', str(quotes))).replace(r'.', ',')

    # sum = ''.join((str(quotes)[47:53]))
    # return sum[0:2] + ',' + sum[3:5]

def dollarCB4():
    quotes = parse(
        'https://finance.rambler.ru/currencies/USD/',
        'div',
        'finance-currency-plate__currency'
    )[1]
    return ''.join(re.findall(r'>*\d+\D\d+', str(quotes))).replace(r'.', ',')


def dollarMarket():
    quotes = parse(
        'https://ru.investing.com/currencies/usd-rub',
        'span',
        'text-2xl',
    )
    return ''.join(re.findall(r'\d+\W\d\d', str(quotes)))

def dollarAliExpress():
  quotes = parse(
    'https://helpix.ru/currency/',
    'td',
    'b-tabcurr__td',
  )
  quote = str(quotes).split(',')[2]
  if '-' in quote: 
    quote =  str(quotes).split(',')[8]
  answ = ''.join(re.findall(r'\d+\W\d+', str(quote)))
  return ','.join(answ.split('.'))

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
    sum = re.findall(r'(?<=unit unit_temperature_c">)(−\d+|\+\d+|0)', str(quote))[0]
    return (sum)

def message():
  with open('message.yaml', encoding="utf-8") as conf_file:
    template = yaml.safe_load(conf_file.read() )['message']
    return template.format(
      today=today,
      dollarCB=dollarCB(),
      dollarMarket=dollarMarket(),
      dollarAliExpress=dollarAliExpress(),
      bitcoin=bitcoin(),
      coronaMoscow=coronaMoscow(),
      coronaRF=coronaRF(),
      weather=weather(),
      degree=u'\u00B0',
      ruble=u'\u20BD',
    )

def messageCB():
  with open('message.yaml', encoding="utf-8") as conf_file:
    template = yaml.safe_load(conf_file.read() ) ['messageCB']
    return template.format(
      dollarCB4=dollarCB4(),
      ruble=u'\u20BD',
    )
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
Биржа: *{dollarMarket()}$*
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


    # else:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на завтра: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()
messageCB = messageCB()
# print(messageCB)
# print(message) 


#TODO 
# 1 chat with bot to send private messages
# 2 check growth fall and make icon
# 3 description on git