import pandas as pd

"""pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.4f}'.format)"""

file_stock = "/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/stock.csv"
file_index = "/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/Index.csv"
file_ROE = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/ROE.csv'
file_v = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/Volatility.csv'

df_stock = pd.read_csv(file_stock) #Monthly
df_index = pd.read_csv(file_index) #Quarterly
df_ROE = pd.read_csv(file_ROE) #Quarterly
df_v = pd.read_csv(file_v) #Daily


#Step1: Dropping all parents statement
def drop_parent(df):
    df_new = df[df['Typrep'] == 'A']
    return df_new.drop('Typrep', axis=1)


#Step2: Changing the format of date into YY-QX
def add_quarter(df,col):
    df[col] = pd.to_datetime(df[col])
    df['Quarter'] = df[col].dt.to_period('Q')
    return df


df_index = drop_parent(df_index)
df_ROE = drop_parent(df_ROE)
df_index = add_quarter(df_index,'Accper')
df_ROE = add_quarter(df_ROE, 'Accper')
df_stock = add_quarter(df_stock, 'Trdmnt')

#Derive monthly PB ratio
df_stock['Previous Quarter'] = df_stock['Quarter'] - 1
monthly_data = pd.merge(df_stock.drop('Quarter',axis=1), df_index, left_on=['Stkcd', 'Previous Quarter'], right_on=['Stkcd','Quarter'])
monthly_data['PB Ratio'] = monthly_data['Closing Price'] / monthly_data['Net Assets per Share']
monthly_data.drop('Quarter',axis=1)
lower_bond = monthly_data['PB Ratio'].quantile(0.05)
upper_bond = monthly_data['PB Ratio'].quantile(0.95)
print(lower_bond,upper_bond)
monthly_data = monthly_data[(monthly_data['PB Ratio'] > lower_bond) & (monthly_data['PB Ratio'] < upper_bond)]
monthly_data.to_csv('Monthly_data.csv')
monthly_data = add_quarter(monthly_data, 'Trdmnt')
quarter_data = pd.merge(df_index,df_ROE,on=['Stkcd','ShortName_EN','Accper','Quarter'])
df = pd.merge(monthly_data[['Stkcd','Trdmnt','Quarter','Closing Price','Return','PB Ratio']], quarter_data[['Stkcd','Quarter','Net Assets per Share', 'ROE']], on=['Stkcd','Quarter'])
df_2010 = df[df['Trdmnt'] == '2010-12-01']
df_reg = pd.merge(df_2010[['Stkcd','Trdmnt','PB Ratio','ROE']], df_v, on=['Stkcd'])
df_reg.to_csv('Q1.csv')

