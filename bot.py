import telebot

import requests
from bs4 import BeautifulSoup

import re

import schedule
import datetime
import time

TOKEN = '5010883386:AAGjmE4-q6WDcinGkFGjVfSU4kpna8Q7eEc'
bot = telebot.TeleBot(TOKEN)
chatId = -1001546899691


def date():
    now = datetime.datetime.now()
    return '0' + str(now.day) if len(str(now.day)) < 2 else str(now.day) + '. ' + '0' + str(now.month) if len(str(now.month)) < 2 else str(now.month)


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
    return 'На *' + date() + '* количество зараженных по Москве:  *' + corona() + '*' + ' человек\n\nКурс доллара: ' + '*' + dollar() + '*' + '\u20BD\nКурс биткойна: ' + '*' + bitcoin() + '*' + '$'

def botMessage():
    ret_msg = bot.send_message(chatId, message(), parse_mode="Markdown")
    assert ret_msg.message_id


schedule.every().day.at("02:58").do(botMessage)

while True: 
    schedule.run_pending()
    time.sleep(1)
