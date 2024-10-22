import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('/Users/duilzhang/Library/CloudStorage/OneDrive-CUHK-Shenzhen/FIN3080/HW！/cleaned.csv')


def CAR(df, start_year=2016, end_year=2022):
    results_dict = {}

    for year in range(start_year, end_year + 1):
        for half in ['h1', 'h2']:
            half_year = f'{year}{half}'
            sue_col = f'{half_year}_x'
            event_date_col = f'{half_year}_y'

            df['TradingDate'] = pd.to_datetime(df['TradingDate'])
            df[event_date_col] = pd.to_datetime(df[event_date_col])
            df['index'] = (df['TradingDate'] - df[event_date_col]).dt.days

            df_filtered = df[(df['index'] >= -60) & (df['index'] <= 60)].copy()

            df_grouped = df_filtered.groupby([sue_col, 'index'])['AR'].mean().reset_index()
            df_grouped[f'CAR_{half_year}'] = df_grouped.groupby(sue_col)['AR'].cumsum()
            df_grouped = df_grouped.drop(columns=['AR'])
            df_grouped.rename(columns={sue_col: 'SUE_decile'}, inplace=True)

            if 'SUE_decile' in results_dict:
                results_dict['SUE_decile'] = pd.merge(results_dict['SUE_decile'], df_grouped,
                                                      on=['SUE_decile', 'index'], how='outer')
            else:
                results_dict['SUE_decile'] = df_grouped

    final_result = results_dict['SUE_decile']
    return final_result


port = CAR(df)
print(port)
port.to_csv('port.csv')
port['CAR_mean'] = port.iloc[:, 2:].mean(axis=1)
port_mean = port.pivot(index='SUE_decile',columns='index',values='CAR_mean')
print(port_mean)
plt.figure(figsize=(10, 6))
for decile in port_mean.index:
    plt.plot(port_mean.columns, port_mean.loc[decile], label=f'Decile {decile + 1}')

plt.title('Cumulative Abnormal Returns by SUE Decile')
plt.xlabel('Event Date Index')
plt.ylabel('Cumulative Abnormal Return')
plt.legend(title='SUE Decile')
plt.grid(True)
plt.show()

