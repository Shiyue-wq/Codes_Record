import pandas as pd
import os

def merge_excel_files(folder_path):
    # 获取文件夹中所有Excel文件的路径
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]

    # 创建一个空的DataFrame来存储合并后的数据
    combined_df = pd.DataFrame()

    # 遍历每一个Excel文件，并合并到combined_df中
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        try:
            # 使用正确的引擎读取Excel文件
            if file.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                df = pd.read_excel(file_path, engine='xlrd')
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"Successfully read and combined: {file_path}")
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    # 排除空列
    combined_df.dropna(axis=1, how='all', inplace=True)

    return combined_df

def calculate_sixth_column_sum(combined_df):
    # 打印合并后的DataFrame的形状和列名
    print("Combined DataFrame Shape:", combined_df.shape)
    print("Combined DataFrame Columns:", combined_df.columns)

    # 计算第六列的总和
    if combined_df.shape[1] >= 6:
        total_sum = combined_df.iloc[:, 5].sum()
        return total_sum
    else:
        raise ValueError("DataFrame does not contain six columns.")

# 使用示例
folder_path = '/Users/wwwzhang/Downloads/头部'  # 替换为你的文件夹路径
combined_df = merge_excel_files(folder_path)
if not combined_df.empty:
    total_sixth_column_sum = calculate_sixth_column_sum(combined_df)
    print(f"Total Sum of Sixth Column: {total_sixth_column_sum}")

    # 保存合并后的DataFrame到新的Excel文件（可选）
    output_file_path = 'merged_excel_file.xlsx'
    combined_df.to_excel(output_file_path, index=False)
    print(f"Merged file saved to: {output_file_path}")
else:
    print("No data to combine.")
