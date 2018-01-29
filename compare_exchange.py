# Compare price for bitcoin exchange script (for Python 3.X)
#
# programmed by beodeulpiri
#
# http://blog.naver.com/beodeulpiri
#

import sys
import pprint
import json, requests
import threading
import telegram

timer_count = 0

nOldDiffBTC = 0
nOldDiffBCH = 0
nOldDiffETH = 0
nOldDiffLTC = 0
nOldDiffDASH = 0

def diffPercent(inPrc, outPrc):
    diff = inPrc - outPrc
    diffPer = diff/outPrc * 100
    return round(diffPer, 2)
    
def checkBitcoin():

    global timer_count
    global ex_usd
    global ex_jpy
    global ex_cny
    
    global nOldDiffBTC 
    global nOldDiffBCH 
    global nOldDiffETH 
    global nOldDiffLTC 
    global nOldDiffDASH
        
    myToken = 'your_telegrambot_token''

    if timer_count == 0 :
        api_url = "https://api.manana.kr/exchange/rate/KRW/USD,JPY,CNY.json"
        
        resp = requests.get(api_url)
        ex_result = json.loads(resp.text)

        ex_usd = ex_result[0]["rate"]
        ex_jpy = ex_result[1]["rate"]
        ex_cny = ex_result[2]["rate"]
        
    print("========== 환율 ==========")
    print("USD: " , ex_usd)
    print("JPY: " , ex_jpy)
    print("CNY: " , ex_cny)

    timer_count += 1

    print("==================== 국내거래소 ====================")
    api_url = "https://api.bithumb.com/public/ticker/BTC"
    resp = requests.get(api_url)
    result = json.loads(resp.text)
    nBTC = int(float(result["data"]["closing_price"]))
    print("BTC price: " + format(nBTC,',') + ", sell: " + result["data"]["sell_price"] + ", buy: " + result["data"]["buy_price"]);
    
    api_url = "https://api.bithumb.com/public/ticker/BCH"
    resp = requests.get(api_url)
    result = json.loads(resp.text)
    nBCH = int(float(result["data"]["closing_price"]))
    print("BCH price: " + format(nBCH,',') + ", sell: " + result["data"]["sell_price"] + ", buy: " + result["data"]["buy_price"]);
    
    api_url = "https://api.bithumb.com/public/ticker/ETH"
    resp = requests.get(api_url)
    result = json.loads(resp.text)
    nETH = int(float(result["data"]["closing_price"]))
    print("ETH price: " + format(nETH,',') + ", sell: " + result["data"]["sell_price"] + ", buy: " + result["data"]["buy_price"]);
    
    api_url = "https://api.bithumb.com/public/ticker/LTC"
    resp = requests.get(api_url)
    result = json.loads(resp.text)
    nLTC = int(float(result["data"]["closing_price"]))
    print("LTC price: " + format(nLTC,',') + ", sell: " + result["data"]["sell_price"] + ", buy: " + result["data"]["buy_price"]);

    print("==================== 해외거래소 ====================")
    strBTC = ""
    strBCH = ""
    strETH = ""

    api_url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
    resp = requests.get(api_url)
    bittrex_result = json.loads(resp.text)
    
    if bittrex_result["success"]  is True:
        strBTC = bittrex_result["result"]["Last"]
    
    api_url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BCC"
    resp = requests.get(api_url)
    bittrex_result = json.loads(resp.text)
    
    if bittrex_result["success"]  is True:
        strBCH = bittrex_result["result"]["Last"]
        
    api_url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH"
    resp = requests.get(api_url)
    bittrex_result = json.loads(resp.text)
    
    if bittrex_result["success"]  is True:
        strETH = bittrex_result["result"]["Last"]
        
    api_url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-LTC"
    resp = requests.get(api_url)
    bittrex_result = json.loads(resp.text)
    
    if bittrex_result["success"]  is True:
        strLTC = bittrex_result["result"]["Last"]

    nOutBTC = int(strBTC*ex_usd)
    nOutBCH = int(strBCH*ex_usd)
    nOutETH = int(strETH*ex_usd)
    nOutLTC = int(strLTC*ex_usd)
    
    fDiffBTC = diffPercent(nBTC, nOutBTC)
    fDiffBCH = diffPercent(nBCH, nOutBCH)
    fDiffETH = diffPercent(nETH, nOutETH)
    fDiffLTC = diffPercent(nLTC, nOutLTC)
    
    print("bittrex [USD] BTC: " + str(strBTC) + ", BCH: " + str(strBCH) + ", ETH: " + str(strETH) + ", LTC: " + str(strLTC))
    print("bittrex [KRW] BTC: ", format(nOutBTC,',') ,"[" , fDiffBTC , "%], BCH: ", format(nOutBCH,',') ,"[" , fDiffBCH , "%]" )
    print("               ETH: ", format(nOutETH,','),"[" , fDiffETH , "%], LTC: ", format(nOutLTC,',') ,"[" , fDiffLTC , "%]" )
    
    api_url = "https://poloniex.com/public?command=returnTicker"
    resp = requests.get(api_url)
    polo_result = json.loads(resp.text)
    
    strBTC = polo_result["USDT_BTC"]["last"]
    strBCH = polo_result["USDT_BCH"]["last"]
    strETH = polo_result["USDT_ETH"]["last"]
    strLTC = polo_result["USDT_LTC"]["last"]

    nOutBTC = int(float(strBTC)*ex_usd)
    nOutBCH = int(float(strBCH)*ex_usd)
    nOutETH = int(float(strETH)*ex_usd)
    nOutLTC = int(float(strLTC)*ex_usd)

    fDiffBTC = diffPercent(nBTC, nOutBTC)
    fDiffBCH = diffPercent(nBCH, nOutBCH)
    fDiffETH = diffPercent(nETH, nOutETH)
    fDiffLTC = diffPercent(nLTC, nOutLTC)

    print("poloniex [USD] BTC: " + strBTC + ", BCH: " + strBCH + ", ETH: " + strETH + ", LTC: " + strLTC)
    print("poloniex [KRW] BTC: ", format(nOutBTC,',') ,"[" , fDiffBTC , "%], BCH: ", format(nOutBCH,',') ,"[" , fDiffBCH , "%]" )
    print("               ETH: ", format(nOutETH,','),"[" , fDiffETH , "%], LTC: ", format(nOutLTC,',') ,"[" , fDiffLTC , "%]" )

    botMessage = ''
    if timer_count % 10 == 0: #10분마다 비교
        if int(fDiffBTC) > nOldDiffBTC or int(fDiffBTC) < nOldDiffBTC:
            botMessage += 'BTC 한국시세[' + format(nBTC, ',') + '원], 해외시세[' + format(nOutBTC, ',') 
            botMessage += '원], 차이[' + str(fDiffBTC) + '%]\n'
            nOldDiffBTC = int(fDiffBTC)
        
        if int(fDiffBCH) > nOldDiffBCH or int(fDiffBCH) < nOldDiffBCH:
            botMessage += 'BCH 한국시세[' + format(nBCH, ',') + '원], 해외시세[' + format(nOutBCH, ',') 
            botMessage += '원], 차이[' + str(fDiffBCH) + '%]\n'
            nOldDiffBCH = int(fDiffBCH)
            
        if int(fDiffETH) > nOldDiffETH or int(fDiffETH) < nOldDiffETH:
            botMessage += 'ETH 한국시세[' + format(nETH, ',') + '원], 해외시세[' + format(nOutETH, ',') 
            botMessage += '원], 차이[' + str(fDiffETH) + '%]\n'
            nOldDiffETH = int(fDiffETH)
            
        if int(fDiffLTC) > nOldDiffLTC or int(fDiffLTC) < nOldDiffLTC:
            botMessage += 'LTC 한국시세[' + format(nLTC, ',') + '원], 해외시세[' + format(nOutLTC, ',') 
            botMessage += '원], 차이[' + str(fDiffLTC) + '%]\n'
            nOldDiffLTC = int(fDiffLTC)

    if botMessage != '':
        print("==================== 시세차이 ====================")
        print(botMessage)
        botMessage += "환율 USD: " + str(round(ex_usd, 2))
        bot = telegram.Bot(token = myToken)
        bot.sendMessage(chat_id='@your_channel', text=botMessage)

    timer = threading.Timer(60, checkBitcoin) #60초 마다 실행
    
    if timer_count > 60 : #한시간마다 환율조회
        print("========== 환율 재조회 ==========")
        timer_count = 0
    
    timer.start()
    
checkBitcoin()

sys.exit(0);

