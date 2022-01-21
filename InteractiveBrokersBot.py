# Imports
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract # prices
from ibapi.order import *
import threading
import time

# Class for connection to Interactive Brokers
class IBApi(EWrapper,EClient):
  def __init__(self):
    EClient.__init__(self, self)
  # Listen for real time bars
  def realtimeBar(self,reqId,time,open_,high,low,close,volume,wap,count):
    bot.on_bar_update(reqId,time,open_,high,low,close,volume,wap,count)

# Bot Logic
class Bot:
  ib = None
  def __init__(self):
    self.ib = IBApi()
    self.ib.connect("127.0.0.1",0000,1)
    ib_thread = threading.Thread(target=self.run_loop,daemon=True)
    ib_thread.start() # will initiate the connection and start listening to the objects
    time.sleep(1) # because there are some messages when we are connecting to IB
    symbol = input("Enter the symbol you want to trade")

    # creating IB contract object
    contract = Contract() # Needed to buy, sell etc
    contract.symbol = symbol.upper()
    contract.secType = "STK" # refer the ticker as a stock see TWS Api
    contract.exchange = "SMART"
    contract.currency = "EUR"

    #request real time data
    self.ib.reqRealTimeBars(0,contract, 5, "TRADES", 1, [])

  #seperate thread otherwise it will be blocked after the ib.run() method
  def run_loop(self):
    self.ib.run()

  # Pass real time bars data back to our bot object
  def on_bar_update(self,reqId,time,open_,high,low,close,volume,wap,count):
    print(reqId)

# Starting bot
bot = Bot()

