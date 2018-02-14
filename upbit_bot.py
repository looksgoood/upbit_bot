import threading
import telegram
import json
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

privacy = './privacy'
interest_coin_list = ['BTC', 'ETH', 'NEO', 'QTUM']
upbit_url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/%s/%d?code=CRIX.UPBIT.%s-%s&count=%d'
telegram_token = ''
telegram_chatbot_id = ''

def upbit_api(period_type, period, market, coin, data_count):
    upbit_maked_url = upbit_url % (period_type, period, market, coin, data_count)
    print(upbit_maked_url)
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    resp = requests.get(upbit_maked_url, headers=headers)
    result = json.loads(resp.text)
    # print(result)
    current_price = result[0]
    tradePrice = current_price['tradePrice']
    print(tradePrice)
    message = coin + ': %f' % tradePrice + '\n'

    return message

def get_current_market_price(coin):
    print('get', coin, 'current price.')
    return upbit_api('minutes', 10, 'KRW', coin, 2)

def process_func():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    bot_message = s + '  current price\n'

    for coin in interest_coin_list:
        bot_message += get_current_market_price(coin)

    print(bot_message)
    bot = telegram.Bot(token = telegram_token)
    bot.sendMessage(chat_id='474560073', text=bot_message)

def get_token_and_chat_id():
    f = open(privacy + '/token.txt', mode='r')
    token = f.readline()
    print('Telegram token : ', token)
    f.close()
    f = open(privacy + '/chat_id.txt', mode='r')
    chat_id = f.readline()
    print('Telegram chat id : ', chat_id)
    f.close()
    return token, chat_id

if __name__ == '__main__':
    # main()
    telegram_token, telegram_chatbot_id = get_token_and_chat_id()
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(process_func,'cron', hour='0-23', minute='*/10')
    # sched.add_job(process_func,'cron', hour='0-23', second='*/10')

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()

# class AsyncTask:
#     def __init__(self):
#         pass

#     def TaskA(self):
#         process_func()
#         threading.Timer(30,self.TaskA).start()

#     def TaskB(self):
#         print('Process B')
#         threading.Timer(3, self.TaskB).start()

# def main():
#     print('Upbit coin market price checking bot')
#     at = AsyncTask()
#     at.TaskA()
