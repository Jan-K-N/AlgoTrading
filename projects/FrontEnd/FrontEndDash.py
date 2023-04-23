"""
Front-End for various strategies.
"""
from RSI import RSIStrategy

k = RSIStrategy('AAPL', '2010-01-01', '2022-04-21')

l = k.backtest()
print(f'Returns: {l:.2%}')

# print(l)