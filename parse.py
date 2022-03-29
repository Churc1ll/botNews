import requests
from bs4 import BeautifulSoup
import re
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

now = datetime.datetime.now()


def date():
    return '*' + ('0' + str(now.day) if len(str(now.day)) < 2 else str(now.day)) + '.' + ('0' + str(now.month) if len(str(now.month)) < 2 else str(now.month)) + '*'


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
        'https://finance.rambler.ru/currencies/USD/',
        'div',
        'finance-currency-plate__currency'
    )
    quote = quotes[1]
    # quote = quotes[0] if now.day % 2 != 0 or now.hour > 12 else quotes[1]
    # sum = ''.join(re.findall(r'\d+', str(quote)[46:54]))
    sum = ''.join((str(quote)[47:53]))
    return '*' + sum[0:2] + ',' + sum[3:5] + '*'


# def dollarToday():
#     quotes = parse(
#         'https://finance.rambler.ru/currencies/USD/',
#         'div',
#         'finance-currency-plate__currency'
#     )
    quote = quotes[0]
    # quote = quotes[0] if now.day % 2 != 0 or now.hour > 12 else quotes[1]
    # sum = ''.join(re.findall(r'\d+', str(quote)[46:54]))
    sum = ''.join((str(quote)[47:53]))
    return '*' + sum[0:2] + ',' + sum[3:5] + '*'


def tradeDollar():
    quotes = parse(
        'https://quote.rbc.ru/ticker/59111',
        'span',
        'chart__info__sum',
    )
    return ''.join(re.findall(r'\d+\W\d\d', str(quotes)))


def aliexpress():
    quotes = parse(
        'https://aliexpress.ru/item/4000102877185.html?spm=a2g2w.productlist.0.0.4a3474d6GCz2Yn&sku_id=10000000267749576',
        'span',
        'ali-kit_Base__base__104pa1 ali-kit_Base__default__104pa1 ali-kit_Base__strong__104pa1 price ali-kit_Price__size-xl__12ybyf Product_Price__current__1uqb8 product-price-current'
    )
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
    sum = ''.join(re.findall(
        r'(?<=unit unit_temperature_c">)\d+', str(quote)))[2:4]
    return sum


def message():
    # if now.hour < 15:
    # and now.weekday() <= 4:
    return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на сегодня: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*'

    #  + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

    # if now.hour > 15:
    #     # and now.weekday() <= 4:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на завтра: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

    # if now.weekday() > 4:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на понедельник: ' + dollar() + '\u20BD\nСтоимость 1$ на Aliexpress: ' + '*' + aliexpress() + '*' + ' \u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

    # else:
    #     return 'За ' + date() + ' количество зараженных по Москве:  *' + corona() + '*' + ' человек\nСреднесуточная температура: ' + '*' + weather() + '\u00B0' + '*' + '\n\nКурс доллара ЦБ на завтра: ' + dollar() + '\u20BD\nБиржевой курс $: ' + '*' + tradeDollar() + '*' + '\u20BD\nСтоимость 1$ на Aliexpress:' + '*' + aliexpress() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'


message = message()

print(message)
