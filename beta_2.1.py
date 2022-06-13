from binance.client import Client
from binance.websockets import BinanceSocketManager

import time

import math


api_key = 'SPECIAL_KEY'

api_secret = 'SECRETKA'

client = Client(api_key, api_secret)


ASSET = 'ETHUSDT'

CURRENCY = 'USDT'

CRYPTOCURRENCY = 'ETH'

START_CRYPTOCURRENCY = 'my_balance'




def balance(symbol):
    balance = client.get_asset_balance(asset=symbol)
    balance = {'free': balance['free'], 'locked': balance['locked']}
    return balance




def history(symbol):
    history = client.get_my_trades(symbol=symbol)
    return history




def price(symbol):
    price = client.get_avg_price(symbol=symbol)['price']
    return float(price)




def order_market_buy(quantity):
    order = client.order_market_buy(symbol=ASSET, quantity=quantity)





def order_market_sell(quantity):
    order = client.order_market_sell(symbol=ASSET, quantity=quantity)



import telebot


bot = telebot.TeleBot('Токен')

ID = 'мой айдишник в папке - Телеграм ID'



def message(text):
    bot.send_message(ID, text)



def buy_message_success():

    data = history(ASSET)[-1]

    message('Покупка')
    message('Информация о сделке \n\nРынок: ' + data['symbol'] + '\nПокупка: ' + data[
        'commissionAsset'] + '\nКупленный актив: ' + data['qty'] + ' ' + data[
                'commissionAsset'] + '\nПроданный актив: ' + data[
                'quoteQty'] + ' ' + CURRENCY + '\nЦена на момент покупки: ' + data[
                'price'] + ' ' + CURRENCY + '\nКомиссия: ' + data[
                'commission'] + ' ' + CURRENCY + '\nВремя сделки: ' + str(data['time']))
    message('Информация о балансе \n\nБаланс ' + CURRENCY + ': ' + str(
        balance(CURRENCY)['free']) + '\nБаланс ' + CRYPTOCURRENCY + ': ' + str(balance(CRYPTOCURRENCY)['free']))
    message('Прибыль \n\nПрибыль ' + CRYPTOCURRENCY + ': ' + str(
        float(balance(CRYPTOCURRENCY)['free']) - START_CRYPTOCURRENCY))



def sell_message_success():

    data = history(ASSET)[-1]

    message('Продажа')
    message('Информация о сделке \n\nРынок: ' + data['symbol'] + '\nПокупка: ' + data[
        'commissionAsset'] + '\nКупленный актив: ' + data['quoteQty'] + ' ' + data[
                'commissionAsset'] + '\nПроданный актив: ' + data[
                'qty'] + ' ' + CRYPTOCURRENCY + '\nЦена на момент продажи: ' + data[
                'price'] + ' ' + CRYPTOCURRENCY + '\nКомиссия: ' + data[
                'commission'] + ' ' + CRYPTOCURRENCY + '\nВремя сделки: ' + str(data['time']))
    message('Информация о балансе \n\nБаланс ' + CURRENCY + ': ' + str(
        balance(CURRENCY)['free']) + '\nБаланс ' + CRYPTOCURRENCY + ': ' + str(balance(CRYPTOCURRENCY)['free']))
    message('Прибыль\n\nПрибыль ' + CRYPTOCURRENCY + ': ' + str(
        float(balance(CRYPTOCURRENCY)['free']) - START_CRYPTOCURRENCY))



TIME = 10

GROW_PERCENT = 0.5

FALL_PERCENT = -0.25



def main(FIRST_PRICE):

    def toFixed(f: float, n=0):
        a, b = str(f).split('.')
        return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))


    time.sleep(TIME)

    PRICE = price(ASSET)

    PROCENT = ((PRICE - FIRST_PRICE) / FIRST_PRICE) * 100

    print('Цена отсчета:', str(FIRST_PRICE), '| Процент:', str(PROCENT))


    if PROCENT >= GROW_PERCENT:
        try:
            print('BUY')

            order_market_buy(toFixed(float(balance(CURRENCY)['free']) / price(ASSET), 5))

            buy_message_success()

            main(PRICE)
        except:
            print('Ошибка при покупке!')

            main(PRICE)

    elif PROCENT <= FALL_PERCENT:
        try:
            print('SELL')

            order_market_sell(toFixed(float(balance(CRYPTOCURRENCY)['free']), 5))

            sell_message_success()

            main(PRICE)
        except:
            print('Ошибка при продаже!')

            main(PRICE)

    else:
        main(FIRST_PRICE)



START_PRICE = price(ASSET)

main(START_PRICE)
