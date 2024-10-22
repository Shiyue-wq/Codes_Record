import pandas as pd
import numpy as np
import statsmodels.api as sm

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.4f}'.format)

one = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/TRD_Week.csv'
three = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/weekly_risk_free_rate.xlsx'

df = pd.read_csv(one)
rf = pd.read_excel(three)

df = df.rename(columns={'Trdwnt':'Date', 'Wretnd':'return'})
#merge with rf and calculate risk premium
rf['trading_date_yw'] = pd.to_datetime(rf['trading_date_yw'])
rf['Date'] = rf['trading_date_yw'].dt.strftime('%Y-%U')
rf = rf.drop(['trading_date_yw'],axis=1)
df_com = pd.merge(df, rf, how='left', on=['Date'])

#Calculate market returns
rm = df_com.groupby('Date')['return'].mean().reset_index()
rm = rm.rename(columns={'return':'market return'})

df_com = df_com.merge(rm, on='Date', how='left')
df_com['market premium'] = df_com['market return'] - df_com['risk_free_return']
df_com['risk premium'] = df_com['return'] - df_com['risk_free_return']
#Split into three periods
clean = df_com[['Stkcd','Date','market premium','risk premium']].dropna()
condition1 = (clean['Date'] >= '2017-01') & (clean['Date'] <= '2018-52')
condition2 = (clean['Date'] >= '2019-01') & (clean['Date'] <= '2020-52')
condition3 = (clean['Date'] >= '2021-01') & (clean['Date'] <= '2022-52')
year1 = clean[condition1]
year2 = clean[condition2]
year3 = clean[condition3]


# Calculate P1's beta to diversify unsystematic risks
def get_beta(group):
    if len(group) < 2 or group['market premium'].var() == 0:
        return pd.DataFrame({
            'beta': [pd.NA],
            'beta_t': [pd.NA],
            'beta_p': [pd.NA],
            'alpha': [pd.NA],
            'alpha_t': [pd.NA],
            'alpha_p': [pd.NA],
            'R_squared': [pd.NA],
            'obs': 0
        },index=[group.name])
    X = sm.add_constant(group['market premium'])
    y = group['risk premium']
    model = sm.OLS(y, X).fit()

    return pd.DataFrame({
        'alpha': model.params['const'],
        'alpha_t': model.tvalues['const'],
        'Alpha_p': model.pvalues['const'],
        'beta': model.params['market premium'],
        'beta_t': model.tvalues['market premium'],
        'Beta_p': model.pvalues['market premium'],
        'R_squared': model.rsquared,
        'obs': int(model.nobs)
    },index=[group.name])


betas = year1.groupby('Stkcd').apply(get_beta).reset_index()
betas = betas.dropna(how='all', axis=1)
print(betas)
# Merge with P2 data to construct portfolios
year2 = year2.merge(betas, on='Stkcd', how='left').dropna()
# year2.sort_values(by=['Date', 'beta'], ascending=[True, False], inplace=True)
# year2['label'] = year2.groupby('Date')['beta'].transform(lambda x: pd.qcut(x, 10, labels=range(10, 0,-1), duplicates='drop'))
year2 = year2.sort_values(by='beta', ascending=True)
year2['label'] = pd.qcut(year2['beta'], 10, labels=False, duplicates='drop')
rm = year2.groupby(['Date', 'label'], observed=True)['market premium'].mean().reset_index()
ri = year2.groupby(['Date', 'label'], observed=True)['risk premium'].mean().reset_index()
rp = pd.merge(rm, ri, on=['Date','label'])
bp = rp.groupby('label', observed=True).apply(get_beta).reset_index()
print(bp)
# Merge with P3 data to construct portfolios
portfolio_indexing = year2[['Stkcd','label']].drop_duplicates()
print(portfolio_indexing)
year3 = year3.merge(portfolio_indexing, on=['Stkcd'], how='left').dropna()
pi = year3.groupby('label', observed=True)['risk premium'].mean().reset_index()
yp = pd.merge(pi, bp[['label','beta']], on=['label'], how='inner')
print(yp)
X = sm.add_constant(yp['beta'])
y = yp['risk premium']
model = sm.OLS(y, X).fit()
final = model.summary()
print(final)