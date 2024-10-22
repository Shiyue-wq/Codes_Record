import pandas as pd
import matplotlib.pyplot as plt

file_Q1 = 'output_Q1.csv'
df_old = pd.read_csv(file_Q1)
df = df_old.copy()
df['type'] = None
#The main board should exclude: 1&4-A Shares; 2&8-B Shares
condition_main = (df['Markettype'] != 2) | (df['Markettype'] != 8)
condition_GEM = (df['Markettype'] == 16) | (df['Markettype'] == 32)
df.loc[condition_main, 'type'] = 'Main'
df.loc[condition_GEM, 'type'] = 'GEM'
df_PE = df[['Stkcd', 'Trdmnt', 'PE Ratio', 'type']].copy()

df = df[(df['Markettype'] != 2) & (df['Markettype'] != 8)]
#df.dropna(subset=['Stock return without CD', 'PE Ratio', 'PB Ratio', 'ROE', 'ROA'], inplace=True)
condition1 = df['Stkcd'] == 1
condition2 = df['Stkcd'] != 1
df.loc[condition1, 'R&D ratio'] = df.loc[condition1, 'R&D ratio'].fillna(0)
df.loc[condition2, 'R&D ratio'] = df.loc[condition2, 'R&D ratio'].bfill()


def summary(df,col_type,col_describe):
    df.set_index(col_type, inplace=True)
    for col in col_describe:
        print(col)
        df.dropna(subset = [col])
        sum = df.groupby(col_type)[col].describe()
        print(sum)
        csv_file = f"{col}_summary.csv"
        sum.to_csv(csv_file)
    return print('finished')


summary(df, 'type', ['Stock return with CD','PE Ratio','PB Ratio','ROA','ROE','R&D ratio','Firm Age'])


df_PE['Trdmnt'] = pd.to_datetime(df_PE['Trdmnt'])
df_PE.set_index(['Trdmnt','type'], inplace=True)
median_PE = df_PE['PE Ratio'].groupby(['type','Trdmnt']).median().reset_index()


plt.figure(figsize=(8, 4))
for type_group in ['GEM', 'Main']:
    subset = median_PE[median_PE['type'] == type_group]
    plt.plot(subset['Trdmnt'], subset['PE Ratio'], linestyle='-', label=type_group)

plt.title('Monthly Median P/E Ratio Time Series')
plt.xlabel('Date')
plt.ylabel('Median P/E Ratio')
plt.legend()
plt.xticks(rotation=45)
plt.show()
plt.savefig('PE.png', dpi=300)




