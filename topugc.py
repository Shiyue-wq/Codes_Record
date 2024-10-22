import pandas as pd
df_6no = pd.read_excel("/Users/wwwzhang/Downloads/6月删除.xlsx")
df_6yes = pd.read_excel("/Users/wwwzhang/Downloads/6月新增.xlsx")
df_5 = pd.read_excel("/Users/wwwzhang/Downloads/5月存量.xlsx")
df_6 = pd.read_excel("/Users/wwwzhang/Downloads/6月存量.xlsx")

df_6no = df_6no.rename(columns={'[收礼金额美元当天]/0ꓸ5_1711703258445':'上月流水'})
df_6yes = df_6yes.rename(columns={'[收礼金额美元当天]/0ꓸ5_1711703258445':'本月流水'})
df_5 = df_5.rename(columns={'[收礼金额美元当天]/0ꓸ5_1711703258445':'上月流水'})
df_6 = df_6.rename(columns={'[收礼金额美元当天]/0ꓸ5_1711703258445':'本月流水'})

#存量
df = pd.merge(df_5[['主播id', '上月流水']], df_6[['主播id', '本月流水']], on="主播id",how='outer')
df = df.fillna(0)
df['diff'] = df['本月流水']-df['上月流水']
df.to_excel('6vs5存量.xlsx')

#总表
df_5 = pd.concat([df_5[['主播id', '上月流水']],df_6no[['主播id', '上月流水']]])
df_6 = pd.concat([df_6[['主播id', '本月流水']],df_6yes[['主播id', '本月流水']]])

df = pd.merge(df_5[['主播id', '上月流水']], df_6[['主播id', '本月流水']], on="主播id",how='outer')
df = df.fillna(0)
df['diff'] = df['本月流水']-df['上月流水']
df.to_excel('6vs5总表.xlsx')