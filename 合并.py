import pandas as pd
df1 = pd.read_excel('/Users/wwwzhang/Downloads/新入会公会主播_1716813390_1718780580_Snippet 1_1831735.xlsx')
df2 = pd.read_excel('/Users/wwwzhang/Downloads/腰尾.xlsx')

df = pd.merge(df1,df2,on='主播id',how='left')
df = df.dropna()
df.to_excel('y腰尾名单.xlsx')
