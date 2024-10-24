import pandas as pd
df = pd.read_csv('/Users/wwwzhang/PycharmProjects/pythonProject/matched_main.csv')
non_empty_firm_id_new_count = df['登记机关'].notna().sum()
total_rows = len(df)
proportion_non_empty_firm_id_new = non_empty_firm_id_new_count / total_rows
print(f"Proportion of non-empty firm_id_new in stage2: {proportion_non_empty_firm_id_new:.2%}")
print(non_empty_firm_id_new_count)
