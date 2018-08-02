#Created this as part of a tutorial series where I followed along, and ended up making a few modifications at the end.
import talib

def initialize(context):  
    context.stocks = symbols('AAPL', 'XOM', 'GOOG', 'MSFT', 'WMT')  
    context.max_cash_per_stock = 10000000.0 / len(context.stocks)  
    context.LOW_RSI = 32 
    context.HIGH_RSI = 68 
    context.date = None

def handle_data(context, data):  
    todays_date = get_datetime().date()  
    if todays_date == context.date:  
        return  
    context.date = todays_date

    cash = context.portfolio.cash  
    prices = history(15, '1d', 'price')  
    rsi = prices.apply(talib.RSI, timeperiod=14).iloc[-1]  
    for stock in context.stocks:  
        current_position = context.portfolio.positions[stock].amount  
        if rsi[stock] > context.HIGH_RSI and current_position > 0:  
            order_target(stock, 0)  
            log.info('{0}: RSI is at {1}, selling {2} shares'.format(  
                stock.symbol, rsi[stock], current_position  
            ))  
        elif rsi[stock] < context.LOW_RSI and current_position == 0:  
            target_shares = context.max_cash_per_stock // data[stock].price  
            order_target(stock, target_shares)  
            log.info('{0}: RSI is at {1}, buying {2} shares.'.format(  
                stock.symbol, rsi[stock], target_shares  
            ))

    # record the current RSI values of each stock  
    record(wmt_rsi=rsi[symbol('WMT')],
           msft_rsi=rsi[symbol('MSFT')],
           goog_rsi=rsi[symbol('GOOG')],  
           xom_rsi=rsi[symbol('XOM')],  
           aapl_rsi=rsi[symbol('AAPL')])
