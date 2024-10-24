import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the main dataframe
main_df = pd.read_csv('/Users/wwwzhang/PycharmProjects/pythonProject/sheet6_merged.csv', low_memory=False)
main_df.rename(columns={'firm_x': 'firm'}, inplace=True)

# Directory containing the CSV files to be matched
folder_path = '/Users/wwwzhang/Downloads/工商'

# Standard column names
column_names = [
    '企业组织机构代码', 'firm', '注册资本', '实缴资本', '纳税人识别号', '法定代表人', '企业状态', '所属行业',
    '统一社会信用代码', '工商注册号', '组织机构代码', '登记机关', '注册日期', '核准日期', '企业类型',
    '经营期限', '注册所在地', '地区编码', '详细地址', '经营范围', '参保人数', '企业电话', '企业座机', '企业邮箱'



def read_csv_with_bom_handling(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    if content[:3] == b'\xef\xbb\xbf':  # Detect BOM
        return pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)
    else:
        return pd.read_csv(file_path, low_memory=False, encoding='ISO-8859-1')


def process_file(file_path):
    try:
        df = read_csv_with_bom_handling(file_path)
    except UnicodeDecodeError:
        print(f"Could not decode file {file_path} with default encodings. Trying 'latin1'.")
        try:
            df = pd.read_csv(file_path, low_memory=False, encoding='latin1')
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            return None

    if len(df.columns) < 2:
        print(f"Not enough columns in {file_path}. Skipping this file.")
        return None

    df.columns = column_names[:len(df.columns)]

    if 'firm' not in df.columns:
        print(f"'firm' column not found in {file_path}. Skipping this file.")
        return None

    print(f"{file_path} has been prepared successfully.")
    return df


def merge_files(main_df, folder_path, chunk_size=10):
    files = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if
             file_name.endswith('.csv')]
    chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    for chunk in chunks:
        with ThreadPoolExecutor(
                max_workers=4) as executor:
            future_to_file = {executor.submit(process_file, file_path): file_path for file_path in chunk}

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    if result is not None:
                        main_df = main_df.merge(result, on='firm', how='left', suffixes=('', '_dup'))
                        print(f"{file_path} has been merged successfully.")

                        # Remove duplicate columns
                        for col in main_df.columns:
                            if col.endswith('_dup'):
                                base_col = col[:-4]
                                main_df[base_col] = main_df[base_col].combine_first(main_df[col])
                                main_df.drop(columns=[col], inplace=True)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return main_df


# Merge files in chunks to reduce memory usage
main_df = merge_files(main_df, folder_path, chunk_size=10)

# Remove duplicate rows
main_df = main_df.drop_duplicates()

# Save the matched data to a CSV file
output_path = 'matched_main.csv'
main_df.to_csv(output_path, index=False)

print(f'Matched data saved to {output_path}')

non_empty_firm_id_new_count = main_df['登记机关'].notna().sum()
total_rows = len(main_df)
proportion_non_empty_firm_id_new = non_empty_firm_id_new_count / total_rows
print(f"Proportion of non-empty firm_id_new in stage2: {proportion_non_empty_firm_id_new:.2%}")
print(non_empty_firm_id_new_count)