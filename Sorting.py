import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.4f}'.format)


file_stock = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW2/Monthly_data.csv'
df_portfolio = pd.read_csv(file_stock)
df_portfolio.sort_values(by=['Stkcd','Trdmnt'], inplace=True)
df_portfolio['Pr PB Ratio'] = df_portfolio.groupby('Stkcd')['PB Ratio'].shift(1)
df_portfolio = df_portfolio[df_portfolio['Trdmnt'] != "2009-12-01"]
df_portfolio['Trdmnt'] = pd.to_datetime(df_portfolio['Trdmnt'])
df_portfolio['Month'] = df_portfolio['Trdmnt'].dt.to_period('M')
df_portfolio.sort_values(by=['Month', 'Pr PB Ratio'], ascending=[True, False], inplace=True)
df_portfolio['label'] = df_portfolio.groupby('Month')['Pr PB Ratio'].transform(lambda x: pd.qcut(x, 10, labels=range(10, 0,-1)))
grouped_returns = df_portfolio.groupby(['Month', 'label'])['Return'].mean().reset_index()
pivot_returns = grouped_returns.pivot(index='Month', columns='label', values='Return')
print(pivot_returns)
average_return = pivot_returns.mean()
print(average_return)
market_return = df_portfolio['Return'].mean()

average_return.plot(kind='bar', figsize=(10, 6))

plt.axhline(y=market_return, color='b', linestyle='--', label='Market Return')
plt.title('Average Return by P/B Portfolio Decile (2021-2023)')
plt.xlabel('Portfolio')
plt.ylabel('Average Return')
plt.xticks(range(0, 10), [f'Portflio {i+1}' for i in range(10)])

plt.legend()
plt.show()




