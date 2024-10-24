import pandas as pd
import matplotlib.pyplot as plt

file_ROE  = '/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/HW1/problem3_data.csv'
df = pd.read_csv(file_ROE)
df['EndDate'] = pd.to_datetime(df['EndDate'])
#Calcularing total revenue growth rate
df['GrowthRate'] = (df['TotalRevenue'] - df['TotalRevenue'].shift(1)) / df['TotalRevenue'].shift(1)
df['Year'] = df['EndDate'].dt.year
cond = df['EndDate'] == '2000-12-31'
df.loc[cond, 'GrowthRate'] = 0
    #Choosing 2011-2020
years = range(2011, 2021)
df['Year'] = df['Year'].astype(int)
sub_df = df[df['Year'].isin(years)].copy()
#Dropping all NaN values
sub_df.dropna()
""" symbols_with_nan = df[pd.isna(df[target])]['Symbol'].unique()
    new_df = df[~df['Symbol'].isin(symbols_with_nan)]"""
median_ROEC = df.groupby('EndDate')['ROEC'].median()
median_g = df.groupby('EndDate')['GrowthRate'].median()
merge_df = pd.merge(sub_df, median_ROEC, on='EndDate')
merge_df = pd.merge(merge_df, median_g, on='EndDate')
#merge_df.rename(columns={'ROEC_y': 'ROEC_median', 'GrowthRate_y': 'GrowthRate_median'})


#Median calculation
def median_plot(df, target, median):
    df['AboveMedian'] = df[target] > df[median]
    #Percentage calculation
    percentages = {}
    new_df = df.copy()
    for year in years:
        total_firms = len(df[df['Year'] == year])
        df_firms = new_df[(new_df['Year'] == year) & new_df['AboveMedian']]
        percentages[year] = 100 * len(df_firms) / total_firms if total_firms > 0 else 0
        new_df = new_df[new_df['Symbol'].isin(df_firms['Symbol'])]
    percentages_series = pd.Series(percentages, name=f"Percentage of Firms with Consecutive Above-Median {target}")
    #print(percentages_series)

    plt.figure(figsize=(10, 6))
    plt.plot(percentages_series.index, percentages_series.values, marker='o', linestyle='-', color='b')
    plt.title(f'Percentage of Firms with Consecutive Above-Median {target} (2011-2020)')
    plt.xlabel('Year')
    plt.ylabel('Percentage (%)')
    plt.grid(True)
    plt.show()
    plt.savefig(f'{target}.png', dpi=300)


median_plot(merge_df, 'ROEC_x', 'ROEC_y')
median_plot(merge_df, 'GrowthRate_x', 'GrowthRate_y')
