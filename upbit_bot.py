import threading
import telegram
import json
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

privacy = './privacy'
interest_coin_list = ['BTC', 'ETH', 'NEO', 'QTUM', 'ADA']
upbit_url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/%s/%d?code=CRIX.UPBIT.%s-%s&count=%d'
upbit_without_period_url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/%s?code=CRIX.UPBIT.%s-%s&count=%d'
telegram_token = ''
telegram_chatbot_id = ''
request_user_agent = ''
standard_price = {}

state_standard = 5.0

class CryptoCoin:
    def __init__(self, openingPrice):
            self.openingPrice = openingPrice
            self.now_state = 1.0

def check_diff_trigger(coin_name, tradePrice):
    openingPrice = standard_price[coin_name].openingPrice
    now_state = standard_price[coin_name].now_state

    if (now_state + 0.05) * openingPrice < tradePrice:
        standard_price[coin_name].now_state += 0.05
        return True
    elif (now_state - 0.05) * openingPrice > tradePrice:
        standard_price[coin_name].now_state -= 0.05
        return True
    
    return False

def calculate_percent(openingPrice, tradePrice):
    return (tradePrice - openingPrice) / openingPrice

def upbit_api(period_type, period, market, coin, data_count, date):
    upbit_maked_url = ''
    if period_type is 'minutes':
        upbit_maked_url = upbit_url % (period_type, period, market, coin, data_count)
    else:
        upbit_maked_url = upbit_without_period_url % (period_type, market, coin, data_count)

    if date:
        upbit_maked_url = '%s&to=%s' % (upbit_maked_url, date)

    print(upbit_maked_url)
    headers = {'user-agent': request_user_agent}
    resp = requests.get(upbit_maked_url, headers=headers)
    result = json.loads(resp.text)

    return result

def get_current_market_price(coin):
    print('get', coin, 'current price.')
    result = upbit_api('minutes', 10, 'KRW', coin, 1, None)
    # print(result)
    current_price = result[0]

    if coin not in standard_price:
        dic = upbit_api('days', None, 'KRW', coin, 1, None)
        new_coin = CryptoCoin(dic[0]['openingPrice'])
        standard_price[coin] = new_coin

    tradePrice = current_price['tradePrice']
    if check_diff_trigger(coin, tradePrice):
        percent = calculate_percent(standard_price[coin].openingPrice, tradePrice)
        message = coin + ': %f (%.2f%%)' % (tradePrice, percent*100) + '\n'
        return True, message

    return False, ''

def process_func():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    bot_message = s + '  current price\n'

    update_message = False
    for coin in interest_coin_list:
        result, message = get_current_market_price(coin)
        if result is True:
            bot_message += message
            update_message = True

    if update_message is True:
        print(bot_message)
        bot = telegram.Bot(token = telegram_token)
        bot.sendMessage(chat_id=telegram_chatbot_id, text=bot_message)

def get_token_and_chat_id():
    f = open(privacy + '/token.txt', mode='r')
    token = f.readline()
    print('Telegram token : ', token)
    f.close()
    f = open(privacy + '/chat_id.txt', mode='r')
    chat_id = f.readline()
    print('Telegram chat id : ', chat_id)
    f.close()
    f = open(privacy + '/user_agent.txt', mode='r')
    user_agent = f.readline()
    print('My user Agent : ', user_agent)
    f.close()
    return token, chat_id, user_agent

if __name__ == '__main__':
    # main()
    telegram_token, telegram_chatbot_id, request_user_agent = get_token_and_chat_id()
    process_func()
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
