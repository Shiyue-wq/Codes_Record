import pandas as pd
from datetime import datetime
import time

star_time = time.time()


#read all csv files
file_age = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/age.csv'
file_stock = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/stock.csv'
file_balance = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/balance sheet.csv'
file_RD = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/RD.csv'
file_eps = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/eps.csv'
file_ratio = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/DATA/ratio.csv'
df_age = pd.read_csv(file_age)
df_stock = pd.read_csv(file_stock)
df_balance = pd.read_csv(file_balance)
df_RD = pd.read_csv(file_RD)
df_eps = pd.read_csv(file_eps)
df_ratio = pd.read_csv(file_ratio)
#Renaming data
df_age.rename(columns={'Listdt':'List Date','Estbdt':'Establishment Date'}, inplace=True)
df_ratio.rename(columns={'F050201B':'ROE','F050501B':'ROA'}, inplace=True)
df_RD.rename(columns={'B001216000':'R&D Expenses'}, inplace=True)
df_balance.rename(columns={'A001000000':'Total Assets','A002000000':'Total Liabilities'}, inplace=True)
df_stock.rename(columns={'Mclsprc':'Monthly Closing Price','Msmvosd':'Market value of tradable shares','Mretwd':'Stock return without CD','Mretnd':'Stock return with CD'}, inplace=True)


#Step1: Dropping all parents statement
def drop_parent(df):
    df_new = df[df['Typrep'] == 'A']
    return df_new.drop('Typrep', axis=1)


#Step2: Changing the format of date into YY-QX
def add_quarter(df,col):
    df[col] = pd.to_datetime(df[col])
    df['Quarter'] = df[col].dt.to_period('Q')
    return df


#Dropping parents statement
df_RD = drop_parent(df_RD)
df_balance = drop_parent(df_balance)
df_ratio = drop_parent(df_ratio)
df_RD = add_quarter(df_RD, 'Accper')
df_balance = add_quarter(df_balance, 'Accper')
df_eps = add_quarter(df_eps, 'Accper')
df_ratio = add_quarter(df_ratio, 'Accper')
#Merging Data
df_eps = df_eps[df_eps['EPS'] != 0]
df_balance = df_balance[(df_balance['Total Assets'] > df_balance['Total Liabilities'])]
df_balance['Total Equity'] = df_balance['Total Assets'] - df_balance['Total Liabilities']
quarter_data = pd.merge(df_RD,df_balance,on=['Stkcd','ShortName_EN','Accper','Quarter'])
quarter_data = pd.merge(quarter_data,df_eps,on=['Stkcd','ShortName_EN','Accper','Quarter'])
quarter_data = pd.merge(quarter_data,df_ratio,on=['Stkcd','ShortName_EN','Accper','Quarter'])
    #Calculating RD ratio
quarter_data['R&D Expenses'] = quarter_data['R&D Expenses'].ffill()
quarter_data['R&D ratio'] = quarter_data['R&D Expenses'] / quarter_data['Total Assets']
df_stock = add_quarter(df_stock,'Trdmnt')
df_stock['Previous Quarter'] = df_stock['Quarter'] - 1
merged_df = pd.merge(df_stock, quarter_data, on=['Stkcd','Quarter'],  how= 'left')
    #Calclulating firm age
df_age['Establishment Date'] = pd.to_datetime(df_age['Establishment Date'])
df_age['Establishment Quarter'] = df_age['Establishment Date'].dt.to_period('Q')
df_age_cal = df_age.drop(['ShortName_EN','List Date','Establishment Date'], axis=1)
merged_df = pd.merge(merged_df, df_age_cal, on=['Stkcd'])
merged_df['Firm Age'] = (merged_df['Quarter'] - merged_df['Establishment Quarter']).apply(lambda x: x.n)
merged_df.drop('Quarter',axis=1)
    #Calculating PE ratio
df_eps_2 = df_eps[['Stkcd','Quarter','EPS']]
df_eps_2.rename(columns={'EPS':'EPS(p)','Quarter':'Previous Quarter'}, inplace=True)
merged_df = pd.merge(merged_df, df_eps_2,  on=['Stkcd','Previous Quarter'],how= 'left')
merged_df['PE Ratio'] = merged_df['Monthly Closing Price'] / (merged_df['EPS(p)'] /3)
    #Calculating PB ratio
df_balance_2 = df_balance[['Total Equity','Quarter','Stkcd']]
df_balance_2.rename(columns={'Total Equity':'Total Equity(p)','Quarter':'Previous Quarter'}, inplace=True)
merged_df = pd.merge(merged_df, df_balance_2,  on=['Stkcd','Previous Quarter'],how= 'left')
merged_df['PB Ratio'] = merged_df['Market value of tradable shares'] * 1000 / merged_df['Total Equity(p)']
merged_df.to_csv('draft.csv')
merged_final = merged_df[['Stkcd','Markettype','Trdmnt','Stock return with CD','PE Ratio','PB Ratio','Quarter','ROE','ROA','R&D ratio','Firm Age']]
print(merged_final)
merged_final.to_csv('output_Q1.csv')

end_time = time.time()
seconds_elapsed = end_time - star_time
print(f"Total seconds elapsed: {seconds_elapsed}.")
