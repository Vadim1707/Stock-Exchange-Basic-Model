import time
import random
import bisect
import numpy as np
# from queue import PriorityQueue
from pprint import pprint 

class Stock: 
    def __init__(self, symbol): 
        self.symbol = symbol 
    def __str__(self) -> str:
        return self.symbol
    def __repr__(self) -> str:
        return self.symbol

class Trader: 
    def __init__ (self, name, balance): 
        self.name = name 
        self.balance = balance 
        self.portfolio = {} 
 
    def buy(self, stock, quantity, price):
        if quantity*price > self.balance:
            print("Not enough money to buy {quantity} {stock}")
            return True
        else: self.balance -= quantity*price
        qp = quantity*price
        print(f"trader {self.name} bought {quantity} {stock} for {qp}")
        self.portfolio[stock] = quantity
        return True
        
    def sell(self, stock, quantity, price):
        qp = quantity*price
        print(f"trader {self.name} sold {quantity} {stock} for {qp}")
        return True
    
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name

class StockOffer:
    def __init__(self, stock, price, trader, quantity, buy=True) -> None:
        self.stock = stock
        self.price = price
        self.trader = trader
        self.buy = buy
        self.quantity = quantity

    def __str__(self) -> str:
        tmptxt = " buys " if self.buy == True else " sells " 
        return str(self.trader) + tmptxt + str(self.quantity) + " stocks " + str(self.stock) + " at price " + str(self.price)
    def __repr__(self) -> str:
        tmptxt = " buys " if self.buy == True else " sells " 
        return str(self.trader) + tmptxt + str(self.quantity) + " stocks " + str(self.stock) + " at price " + str(self.price)


# create stocks
stocks = [ 
    Stock("AAPL"),
    Stock("GOOGL"),
    Stock("MSFT"),
    Stock("AMZN"),
    Stock("TSLA"),
    Stock("FB"),
    Stock("NFLX"),
]



# Create the traders 
traders = [ 
    Trader("Trader 1", 10000), 
    Trader("Trader 2", 15000), 
    Trader("Trader 3", 20000) 
] 



class StockExchange:
    def __init__(self, stocks) -> None:
        self.prices_buy = {s: random.random()*(25) + 25*i+1 for i, s in enumerate(stocks)}
        self.prices_sell = {s : self.prices_buy[s]-2 for s in self.prices_buy}
        # print(self.prices_buy, self.prices_sell)
        stock_offers = {"buy": {}, "sell": {}}
        for i, s in enumerate(stocks):
            stock_offers['buy'][s] = []
            price = random.random()*(25) + 25*i+1
            bisect.insort(stock_offers['buy'][s], StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=True))
            price = random.random()*(25) + 25*i+1
            # stock_offers['buy'][s].put((price, StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=True )))
            bisect.insort(stock_offers['buy'][s], StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=True), key= lambda x: x.price)
        for i, s in enumerate(stocks):
            stock_offers['sell'][s] = []
            price = random.random()*(25) + 25*i+1
            bisect.insort(stock_offers['sell'][s], StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=False))
            price = random.random()*(25) + 25*i+1
            # stock_offers['buy'][s].put((price, StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=True )))
            bisect.insort(stock_offers['sell'][s], StockOffer(s, price=price, trader = random.choice(traders), quantity=random.randint(10,30), buy=False), key= lambda x: x.price)

        self.stock_offers = stock_offers


    def run(self):
        # BUG: sometimes appends negative stock amounts
        # Simulate buying and selling requests every 0.1 seconds 
        # TODO: add abbility to change portfolios of traders using their Buy and Sell functions (modify actions in loop)
        i = 0
        while i < 1000: # while true for endless
            time.sleep(0.01) 
            stock = random.choice(stocks) 
            trader = random.choice(traders) 
            action = random.choice(["buy", "sell"]) 
            quantity = random.randint(1, 10) 
        
            if action == "buy": 
                price_of_trader = np.random.normal(self.prices_buy[stock], 1)
                offers = self.stock_offers['sell'][stock]

                while len(offers)!=0:
                    offer = offers.pop(0)
                    # print(offer[0], offer)
                    if offer.price > price_of_trader:
                        # stop buying
                        # return first entry back
                        bisect.insort(self.stock_offers['sell'][stock], offer, key=lambda x: x.price)
                        # add new buy proposition
                        bisect.insort(self.stock_offers['buy'][stock], StockOffer(stock, price_of_trader, trader, quantity), key=lambda x: x.price)
                        print(f"trader {trader} puts a buy option of {quantity} of stock {stock} with price {price_of_trader}")
                        break
                    elif offer.price <= price_of_trader and offer.quantity < quantity:
                        quantity -= offer.quantity
                        print(f"trader {trader} buys {quantity} of stock {stock} for {offer.price} each")
                        continue
                    elif offer.price <= price_of_trader and offer.quantity == quantity:
                        print(f"trader {trader} buys {quantity} of stock {stock} for {offer.price} each")
                        break
                    else:
                        print(f"trader {trader} buys {quantity} of stock {stock} for {offer.price} each")
                        new_quantity = quantity - offer.quantity
                        bisect.insort(self.stock_offers['sell'][stock], StockOffer(offer.stock, offer.price, offer.trader, new_quantity, buy=False), key=lambda x: x.price)
                        break
                    # buying has finished and tables updated
                    

                # find proposition of stocks where price of trader > price of selling
                # if quantity < proposition
                # print(not enough stocks)
                # else: trader.buy()
                # stock offers: change
                # trader.buy(stock, quantity, price_of_trader) 
            elif action == "sell": 
                price_of_trader = np.random.normal(self.prices_buy[stock], 1)
                offers = self.stock_offers['buy'][stock]

                while len(offers) != 0:
                    offer = offers.pop()
                    # print(offer[0], offer)
                    if offer.price < price_of_trader:
                        # stop buying
                        # return first entry back
                        bisect.insort(self.stock_offers['buy'][stock], offer, key=lambda x: x.price)
                        # add new buy proposition
                        bisect.insort(self.stock_offers['sell'][stock], StockOffer(stock, price_of_trader, trader, quantity, buy=False), key=lambda x: x.price)
                        print(f"trader {trader} puts a sell option of {quantity} of stock {stock} with price {price_of_trader}")
                        break
                    elif offer.price >= price_of_trader and offer.quantity < quantity:
                        quantity -= offer.quantity
                        print(f"trader {trader} sells {quantity} of stock {stock} for {offer.price} each")
                        continue
                    elif offer.price >= price_of_trader and offer.quantity == quantity:
                        print(f"trader {trader} sells {quantity} of stock {stock} for {offer.price} each")
                        break
                    else:
                        print(f"trader {trader} sells {quantity} of stock {stock} for {offer.price} each")
                        new_quantity = quantity - offer.quantity
                        bisect.insort(self.stock_offers['buy'][stock], StockOffer(offer.stock, offer.price, offer.trader, new_quantity), key=lambda x: x.price)
                        break
                    # selling has finished
            
            i += 1
    def show_stats(self):
        for s in stocks:
            pprint(self.stock_offers['sell'][s])
        for s in stocks:
            pprint(self.stock_offers['buy'][s])


SE = StockExchange(stocks)
SE.run()
# SE.show_stats()


