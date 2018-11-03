# importing required dependencies
from pprint import pprint
import time
from binance.client import Client
from pprint import pprint
from yaspin import yaspin
from yaspin.spinners import Spinners
from clint.textui import colored, puts
from tabulate import tabulate
import pandas as pd
from pandas.io.json import json_normalize
from binance.enums import *
import qprompt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Insert your API keys here
API_KEY = ""
API_SECRET = ""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# connecting a client to Binance server
client = Client(API_KEY,API_SECRET) 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Bot Name and other info
from pyfiglet import Figlet
f = Figlet(font='eftiwall')
puts(colored.cyan(f.renderText("          X          ")+'\t\t\tThe  Binance Trading Bot '))
puts(colored.cyan("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))
puts(colored.red("\tDeveloped by @Ibrar_Ahmad \t\t\t (test version)\n\n"))


# Loading (connection to server)
puts(colored.red("Connecting to Binance Server !"))
with yaspin(text="To Binance Server").white.bold.blink.bouncingBall.on_cyan as sp:
    client = Client(API_KEY,API_SECRET) # connecting a client to Binance server
    time.sleep(1)
    sp.ok("Connected") 




# method for priting line   
def printLine():
    puts(colored.blue("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))

# Program Menu
def program_menu():
    # Printing Menu & asking user for enter a choice
    menu = [['1',"View Account Balance"],['2',"Place a Buy Order"],['3',"Place a Sell Order"]]
    qprompt.wrap("Choose one of the following choices")
    puts(colored.yellow(tabulate(menu,tablefmt="fancy_grid")))
    choice = qprompt.ask_str("Enter your Choice")
    return(choice)

# account balances
def view_portfolio():
    
    ac_info = client.get_account()
    puts(colored.green("\t >> Your Portfolio <<"))
    _header = ['Coin','Available Balance','Locked']
    ac_info = json_normalize(ac_info['balances'])
    raw_balances = pd.DataFrame(ac_info)
    raw_balances['free'] = raw_balances['free'].astype(float)  
    balances = raw_balances[(raw_balances['free'] != 0.0)]
    puts(colored.yellow(tabulate([[balances.to_string(index=False)]],tablefmt="grid")))

# showing a input coin data ( price,volume,24hr high/low)
def coin_data():
    while(True):
        puts(colored.yellow("\nEnter a coin symbol \tex: BTC NEO ETH BNB"))
        coin_input = raw_input("-> ")
        if len(coin_input) > 4 or len(coin_input) < 2:
            puts(colored.red("\n\t !! ERROR !! Invalid Input Coin Symbol \n\tPlease enter again"))
            continue
        else:
             break

    # Printing Coin Info (voulume 24hr high low etc)
    coin_symbol = coin_input+'BTC'
    coin_info = client.get_ticker(symbol=coin_symbol)

    puts("\nCoin Symbol : "+colored.yellow(coin_symbol)+"\t\t Volume : "+colored.cyan(coin_info['quoteVolume']+" BTC"))
    puts("Last Price : "+colored.yellow(coin_info['lastPrice'])+"\t\t24 hr High :"+colored.green(coin_info['highPrice']))
    puts("\t\t\t\t24 hr Low : "+colored.red(coin_info['lowPrice']))
    return(coin_symbol)

# method for showing order book 
def order_book(coin_symbol):
    depth = client.get_order_book(symbol=coin_symbol,limit=20)

    # Buy Orders
    HEADER = ["Price (BTC)","Amount","empty"]
    buy_orders= pd.DataFrame(depth['bids'],columns = HEADER)
    # converting type(object) to type(float)
    buy_orders["Price (BTC)"] = buy_orders["Price (BTC)"].astype(float)
    buy_orders["Amount"] = buy_orders["Amount"].astype(float)
    buy_orders["Total (BTC)"] = buy_orders["Price (BTC)"]*buy_orders["Amount"]

    # Sell Orders
    sell_orders = pd.DataFrame(depth['asks'],columns = HEADER)
    sell_orders["Price (BTC)"] = sell_orders["Price (BTC)"].astype(float)
    sell_orders["Amount"] = sell_orders["Amount"].astype(float)
    sell_orders["Total (BTC)"] = sell_orders["Price (BTC)"]*sell_orders["Amount"]

    # printing Order_book (BUY/Sell)
    order_book = pd.concat([buy_orders[["Price (BTC)","Amount","Total (BTC)"]],sell_orders[["Price (BTC)","Amount","Total (BTC)"]]],axis=1,sort=False)
    localtime = time.asctime(time.localtime(time.time()))
    puts(colored.yellow("\tOrder Book Data Fetched @ ")+ colored.yellow(localtime))
    puts(colored.green("\n\t~~~~~~~ BUY Orders~~~~~~~ ")+colored.red("\t~~~~~~ SELL Orders ~~~~~~~ "))
    puts(colored.cyan(tabulate([[order_book.to_string(index=False)]],tablefmt="grid")))

def coin_quantity(coin):
    balance = client.get_asset_balance(asset=coin)
    return (balance['free'])

# available balance
def avail_btc():
    balance = client.get_asset_balance(asset='BTC')
    return (balance['free'])

# BUY Order Method
def set_buyOrder(coin_symbol):

    qprompt.wrap("\t\t\t~> SET BUY ORDER <~")
    while (1):
        puts(colored.green("\t\t\t\tAvailable BTC : " + avail_btc() + " BTC"))
        per_coin_price = qprompt.ask_str("Enter Coin Price ")
        worth_btc = qprompt.ask_str("Total worth in BTC")
        quantity_coin = int(round(float(worth_btc)/float(per_coin_price)))
        puts(colored.red("\n\t\tPlease confirm your order"))
        puts(colored.green("\t\tBUY "+str(quantity_coin)+" coins @"+str(per_coin_price)+" (Total: "+str(worth_btc)+" ) BTC"))
        q = raw_input("\t[?] Confirm : ")
        if q == 'Y' or q == 'y':
            # uncomment this code - for actual use
            '''
            # placing a buy order
            order = client.order_limit_buy(
            symbol=coin_symbol,
            quantity=quantity_coin,
            price=per_coin_price)
            '''
            puts(colored.yellow("\n\t********* [?] Your Order has been placed *********"))
            #break
            #return (order)
        else:
            puts(colored.cyan("---- [!] ALERT Something went wrong | Plz set this order again ----"))
            continue
        break


 # Sell Order method

# SELL Order Mthod
def set_sellOrder():
    qprompt.wrap("\t\t\t~> SET SELL ORDER <~")
    coin_symbol = coin_data()
    coin = coin_symbol.replace('BTC','')
    while(1):
        puts(colored.blue("\n[***] SET YOUR ORDER [***]"))
        puts(colored.red("\t\t\t\tAvailable "+ coin +" : "+coin_quantity(coin)))
        per_coin_price = qprompt.ask_str("Enter Coin Price ")
        quantity = qprompt.ask_str("Enter quantity")
        worth_btc = float(quantity)*float(per_coin_price)
        puts(colored.green("\n\t\tPlease confirm your order"))
        puts(colored.red("\t\tSELL "+str(quantity)+" coins @"+str(per_coin_price)+" (Total: "+str(worth_btc)+" ) BTC"))
        q = raw_input("\t[?] Confirm : ")
        if q == 'Y' or q == 'y':
            # uncomment this code - for actual use
            '''
            # placing a buy order
            order = client.order_limit_sell(
            symbol=coin_symbol,
            quantity=quantity_coin,
            price=per_coin_price)
            '''
            puts(colored.yellow("\n\t********* [?] Your Order has been placed *********"))
            #break
            #return (order)
        else:
            puts(colored.cyan("---- [!] ALERT Something went wrong | Plz set this order again ----"))
            continue
        break

# main method
def main():
    while(1):
        choice = program_menu()
        if choice == '1':
            view_portfolio()

        if choice == '2': 
            coin_symbol = coin_data()
            order_book(coin_symbol)
            order = set_buyOrder(coin_symbol)  

        if choice == '3':
            order = set_sellOrder() 




        # +++++ asking for returing to menu or to quit the program ++++
        choice = qprompt.ask_str("Return to Main Menu ( Y for YES ) & ( q for quit)")
        if choice == 'q' or choice == 'Q':
            exit()
        else: 
            printLine()
            continue

main()