import pandas as pd
day5 = "/Users/wwwzhang/Downloads/5天数据.xlsx"
day7 = "/Users/wwwzhang/Downloads/7天数据.xlsx"
user = '/Users/wwwzhang/Downloads/user8.xlsx'
#user = '/Users/wwwzhang/Downloads/un.xlsx'

#user的名单直接copy上一周的,会包含名字和pic,在boosting data analysis

df_5 = pd.read_excel(day5)
df_7 = pd.read_excel(day7)
df_user = pd.read_excel(user) #流量：boost

df_5.replace('-',0)
df_7.replace('-',0)

df_5 = df_5.rename(columns={'主播id':'ID', '直播间被曝光次数':'exposure_5day', '直播主播开播时长(小时)':'livetime_5day','[收礼金额美元当天]/0ꓸ5_1711703258445':'income_5day','acu':'acu_5day','送礼用户数':'spender_5day','CTR(间内/间外)':'CTR_5day'})
df_7 = df_7.rename(columns={ '主播id':'ID', '直播间被曝光次数':'exposure_7day', '直播主播开播时长(小时)':'livetime_7day','[收礼金额美元当天]/0ꓸ5_1711703258445':'income_7day','acu':'acu_7day','送礼用户数':'spender_7day','CTR(间内/间外)':'CTR_7day'})
df = pd.merge(df_5,df_7,on='ID', how="left")
df = pd.merge(df, df_user, on='ID', how='outer')

#注意根据具体对比天数更改
days = 7

df['exposure_rate'] = (df['exposure_5day']/5 - df['exposure_7day']/days)/(df['exposure_7day']/days)
df['livetime_rate'] = (df['livetime_5day']/5 - df['livetime_7day']/days)/(df['livetime_7day']/days)
df['income_rate'] = (df['income_5day']/5 - df['income_7day']/days)/(df['income_7day']/days)
df['acu_rate'] = (df['acu_5day']/5 - df['acu_7day']/days)/(df['acu_7day']/days)
df['spender_rate'] = (df['spender_5day']/5 - df['spender_7day']/days)/(df['spender_7day']/days)
df['CTR_rate'] = (df['CTR_5day']/5 - df['CTR_7day']/days)/(df['CTR_7day']/days)


#给local查content的表
#df_local = df[['boost', 'ID', 'Name','Pic','exposure_5day', 'exposure_rate', 'livetime_5day', 'livetime_rate', 'income_5day', 'income_rate', 'acu_5day', 'acu_rate', 'spender_5day', 'spender_rate', 'CTR_5day','CTR_rate']]
df = df[['boost', 'ID','exposure_5day','exposure_7day', 'exposure_rate', 'livetime_5day','livetime_7day', 'livetime_rate', 'income_5day', 'income_7day','income_rate', 'acu_5day','acu_7day', 'acu_rate', 'spender_5day', 'spender_7day','spender_rate', 'CTR_5day','CTR_7day','CTR_rate']].copy()
df.replace('-', 0, inplace=True)

columns_of_5 = [col for col in df.columns if col.endswith('_5day')]
columns_of_7 = [col for col in df.columns if col.endswith('_7day')]

boosts = ['u1', 'u2', 'u3', 'u4', 'u5']
averages = {}

for boost in boosts:
    df_filtered = df[df['boost'] == boost]
    averages[boost] = {
        'mean_5day': df_filtered[columns_of_5].mean() / 5,
        'mean_7day': df_filtered[columns_of_7].mean() / 7
    }


for boost, avg in averages.items():
    print(f"Averages for {boost}:\n_5day:\n{avg['mean_5day']}\n_7day:\n{avg['mean_7day']}\n")

averages_df = pd.DataFrame({
    boost: {
        'mean_5day': averages[boost]['mean_5day'],
        'mean_7day': averages[boost]['mean_7day']
    }
    for boost in averages
}).T  # Transpose to have boosts as index

# Display the DataFrame
averages_df.reset_index(inplace=True)
averages_df.rename(columns={'index': 'boost'}, inplace=True)

df_u1 = df[df['boost'] == 'u1']
df_u2 = df[df['boost'] == 'u2']
df_u3 = df[df['boost'] == 'u3']
df_u4 = df[df['boost'] == 'u4']
df_u5 = df[df['boost'] == 'u5']


with pd.ExcelWriter('周日头部总结.xlsx') as writer:
    df.to_excel(writer, sheet_name='总表')
    df_u1.to_excel(writer, sheet_name='u1')
    df_u2.to_excel(writer, sheet_name='u2')
    df_u3.to_excel(writer, sheet_name='u3')
    df_u4.to_excel(writer, sheet_name='u4')
    df_u5.to_excel(writer, sheet_name='u5')
    averages_df.to_excel(writer, sheet_name='总览')


