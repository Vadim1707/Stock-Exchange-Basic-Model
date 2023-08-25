# Stock-Exchange-Basic-Model

Explanation of model:

There's an entity of Stock, which only has it's name

There's entity of StockOffer, which defines a Trader who might want to sell or buy Stocks, he names the desired amount of Stocks, his desired price

And there's entity of StockExchange, which contains all information about current prices, all possible proposals for buying and selling stocks


If Trader wants to buy a stock for price X and StockExchange has cheaper options (and sufficient amount of them), then Trader immediately buys it

Else, if there's insufficient amount of stocks, his buying proposal stays in StockExchange and waits, maybe someone would like tosell him Stocks for his desired price

Same logic goes for selling stocks.

