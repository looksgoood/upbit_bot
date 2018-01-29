import threading
import telegram
import json
import requests

interest_coin_list = ['BTC', 'ETH']
upbit_url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/%s/%d?code=CRIX.UPBIT.%s-%s&count=%d&to=%s'

def upbit_api(period_type, period, market, coin, data_count, time):
    upbit_maked_url = upbit_url % (period_type, period, market, coin, data_count, time)
    resp = requests.get(upbit_maked_url)
    result = json.loads(resp.text)
    print(result)


def get_current_market_price(coin):
    print('hello!', coin)

class AsyncTask:
    def __init__(self):
        pass

    def TaskA(self):
        print('Process A')
        for coin in interest_coin_list:
            get_current_market_price(coin)
        threading.Timer(10,self.TaskA).start()

    # def TaskB(self):
    #     print('Process B')
    #     threading.Timer(3, self.TaskB).start()

def main():
    print('Upbit coin market price checking bot')
    upbit_api('minute', 10, 'KRW', 'BTC', 1, )
    # print('Async Function')
    # at = AsyncTask()
    # at.TaskA()
    # at.TaskB()

if __name__ == '__main__':
    main()

# sched = BackgroundScheduler()

# sched.start()

# sched.add_job(job_function,'cron', hour='0-23', minute='*/5')
