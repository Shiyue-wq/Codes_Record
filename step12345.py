import os
import pandas as pd


directory_path = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW4'

csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]


for file in csv_files:
    variable_name = os.path.splitext(file)[0].replace('-', '_').replace(' ', '_')
    file_path = os.path.join(directory_path, file)
    globals()[variable_name] = pd.read_csv(file_path)


#Converting into half year format
def convert_to_half_yearly(date):
    year = date.year
    if date.month == 6 and date.day == 30:
        return f"{year}h1"
    elif date.month == 12 and date.day == 31:
        return f"{year}h2"
    return None


# Function to adjust EPS for the second half of each year
def adjust_eps(group):
    if 'h1' in group['Half'].values and 'h2' in group['Half'].values:
        h1_eps = group.loc[group['Half'] == 'h1', 'EPS'].values[0]
        h2_eps = group.loc[group['Half'] == 'h2', 'EPS'].values[0]
        group.loc[group['Half'] == 'h2', 'EPS'] = h2_eps - h1_eps
    return group


#Step1: Individual stock return
stock_return = pd.concat([one, two, three, four, five, six, seven, eight, nine],ignore_index=True)
stock_return = stock_return.rename(columns={'Trddt':'TradingDate', 'Dretnd':'StockReturn'})
stock_return['TradingDate'] = pd.to_datetime(stock_return['TradingDate'])
stock_return.dropna()

#Step2: Market stock return
market_return = market_return.rename(columns={'Trddt':'TradingDate', 'Dretmdeq':'MarketReturn'})
market_return = market_return[market_return['Markettype'] == 1]
market_return = market_return[['TradingDate','MarketReturn']]
market_return['TradingDate'] = pd.to_datetime(market_return['TradingDate'])
market_return.dropna()


#Step3: EPS data
EPS = EPS[EPS['Typrep'] == 'A']
EPS = EPS[~EPS['ShortName_EN'].str.startswith(('ST ', 'PT '))]
EPS['Indcd'] = EPS['Indcd'].astype(str)
EPS = EPS[~EPS['Indcd'].str.startswith('J')]

EPS = EPS.rename(columns={'Accper':'RecordDate','F090101B':'EPS'})
EPS['RecordDate'] = pd.to_datetime(EPS['RecordDate'])
EPS = EPS[EPS['RecordDate'].dt.month.isin([6, 12]) & EPS['RecordDate'].dt.day.isin([30, 31])]
EPS['Date'] = EPS['RecordDate'].apply(convert_to_half_yearly)
EPS = EPS[['Stkcd','Date','EPS']]
EPS['Year'] = EPS['Date'].str.slice(0, 4)
EPS['Half'] = EPS['Date'].str.slice(4, 6)
df_EPS = EPS.groupby(['Stkcd', 'Year']).apply(adjust_eps).reset_index(drop=True)
#df_EPS = pd.read_csv('df_EPS.csv')
df_EPS.sort_values(by=['Stkcd', 'Year', 'Half'], inplace=True)
for stk in df_EPS['Stkcd'].unique():
    condition = df_EPS['Stkcd'] == stk
    company_data = df_EPS[condition].copy()
    company_data['Prev_EPS'] = company_data['EPS'].shift(1)
    company_data.loc[company_data['Half'] == 'h1', 'Adjusted_EPS'] = company_data['EPS']
    company_data.loc[company_data['Half'] == 'h2', 'Adjusted_EPS'] = company_data['EPS'] - company_data['Prev_EPS']
    company_data['UE'] = company_data['Adjusted_EPS'] - company_data['Adjusted_EPS'].shift(2)
    df_EPS.loc[condition, 'Adjusted_EPS'] = company_data['Adjusted_EPS']
    df_EPS.loc[condition, 'UE'] = company_data['UE']
df_EPS = df_EPS.dropna(subset=['Adjusted_EPS'])
df_EPS['Std'] = df_EPS.groupby('Stkcd')['UE'].transform(lambda x: x.rolling(window=4, min_periods=1).std())
df_EPS['SUE'] = df_EPS['UE'] / df_EPS['Std'].replace(0, pd.NA)
df_EPS.dropna(subset=['Std'], inplace=True)
df_EPS.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
"""percentile_5th = df_EPS['SUE'].quantile(0.05)
percentile_95th = df_EPS['SUE'].quantile(0.95)
df_EPS = df_EPS[(df_EPS['SUE'] >= percentile_5th) & (df_EPS['SUE'] <= percentile_95th)]"""
df_EPS.sort_values(by=['Date', 'SUE'], inplace=True)
df_EPS['label'] = df_EPS.groupby('Date')['SUE'].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates='drop'))
df_EPS.reset_index(inplace=True)
df_EPS = df_EPS.pivot(index='Stkcd', columns='Date', values='label')
df_EPS = df_EPS.drop('2015h2', axis=1)
df_EPS.reset_index(inplace=True)


#Step4: announcement data
announce_date = announce_date.rename(columns={'Accper':'RecordDate','Annodt':'AnnounceDate'})
announce_date['RecordDate'] = pd.to_datetime(announce_date['RecordDate'])
announce_date = announce_date[announce_date['RecordDate'].dt.month.isin([6, 12]) & announce_date['RecordDate'].dt.day.isin([30, 31])]
announce_date['Date'] = announce_date['RecordDate'].apply(convert_to_half_yearly)
df_anno = announce_date[['Stkcd','AnnounceDate','Date']].pivot(index='Stkcd', columns='Date', values='AnnounceDate')
df_anno = df_anno.dropna()

#Step5: Merge all data
df = pd.merge(stock_return, market_return, on='TradingDate', how='inner')
df = df.merge(df_EPS, on='Stkcd', how='inner')
df = df.merge(df_anno, on='Stkcd', how='inner')
df['AR'] = df['StockReturn'] - df['MarketReturn']
df = df.drop(columns=['StockReturn','MarketReturn'])
df = df.dropna()
df.to_csv('cleaned.csv')
print(df)