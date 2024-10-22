import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import shapiro

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.4f}'.format)

one = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/1.csv'
two = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/2.csv'
three = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/3.csv'
four = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/4.csv'
five = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/5.csv'

df1 = pd.read_csv(one)
df2 = pd.read_csv(two)
df3 = pd.read_csv(three)
df4 = pd.read_csv(four)
df5 = pd.read_csv(five)
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
df = df.rename(columns={'Indexcd':'Name','Idxtrd01':'Date','Idxtrd05':'Closing Index'})
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df_month = df.resample('M').last()
df_month.reset_index(inplace=True)
df_month['Monthly return'] = df_month['Closing Index'] / df_month['Closing Index'].shift(1) - 1
df_month = df_month.dropna()
stat, p = shapiro(df_month['Monthly return'])
print(f"Shapiro-Wilk Test Statistic: {stat}, P-value: {p}")
if p < 0.10:
    print("The data do not follow a normal distribution.")
else:
    print("The data follow a normal distribution.")

summary = df_month['Monthly return'].describe()
summary['skewness'] = df_month['Monthly return'].skew()
summary['Kurtosis'] = stats.kurtosis(df_month['Monthly return'], fisher=False)
print(summary)
plt.figure(figsize=(8, 4))
plt.hist(df_month['Monthly return'].dropna(), bins=30, color='blue', alpha=0.3)
plt.title('Histogram of CSI300 monthly returns')
plt.xlabel('Monthly returns')
plt.ylabel('Frequency')

plt.show()