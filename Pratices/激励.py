import pandas as pd
import numpy as np

df = pd.read_excel("/Users/wwwzhang/Downloads/激励.xlsx")

# 创建一个空的DataFrame来存储分组结果
grouped_df = pd.DataFrame()

# 遍历每一列，并将其随机分成两组
for column in df.columns:
    data = df[column].dropna().values  # 获取当前列的数据，并去除空值
    np.random.shuffle(data)  # 随机打乱数据

    cut1 = len(data) // 3  # 计算中间索引
    cut2 = cut1*2

    group1, group2, group3 = data[:cut1], data[cut1:cut2], data[cut2:]

    grouped_df[f'{column}_group1'] = pd.Series(group1)
    grouped_df[f'{column}_group2'] = pd.Series(group2)
    grouped_df[f'{column}_group3'] = pd.Series(group3)

grouped_df.reset_index(drop=True, inplace=True)
print(grouped_df)

output_file_path = 'grouped_excel_file.xlsx'
grouped_df.to_excel(output_file_path, index=False)
