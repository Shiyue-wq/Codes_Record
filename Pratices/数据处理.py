import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time

start_time = time.time()

file1 = '/Users/wwwzhang/Downloads/数据匹配.csv'
file2 = '/Users/wwwzhang/Downloads/newfile.csv'
df1 = pd.read_csv(file1, dtype=str, low_memory=False, on_bad_lines='skip')
df2 = pd.read_csv(file2, dtype=str, low_memory=False, on_bad_lines='skip')
print(df1.head())

df = pd.merge(df1,df2,on='firm',how="left")

non_empty_firm_id_new_count = df['firm_id_new'].notna().sum()
total_rows = len(df)
proportion_non_empty_firm_id_new = non_empty_firm_id_new_count / total_rows

print(df.head())
print(f"Proportion of non-empty firm_id_new in stage1: {proportion_non_empty_firm_id_new:.2%}")
df.to_csv('matched1.csv',index=False)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

#df1 = df1.drop_duplicates(subset="firm")
#df2 = df2.drop_duplicates(subset="firm")

matched_rows_df1 = df['firm_id_new'].notna()
df1_unmatched = df1.loc[~df1['firm'].isin(df.loc[matched_rows_df1, 'firm'])]

matched_firms = df.loc[matched_rows_df1, 'firm']
df2_unmatched = df2[~df2['firm'].isin(matched_firms)]

df1_unmatched.loc[:, 'firm'] = df1_unmatched['firm'].str.replace('有限公司|责任公司|有限责任公司|公司|（|）|(|)', '', regex=True)
df2_unmatched.loc[:, 'firm'] = df2_unmatched['firm'].str.replace('有限公司|责任公司|有限责任公司|公司|（|）|(|)', '', regex=True)

df_unmatched = pd.merge(df1_unmatched,df2_unmatched,on='firm',how="left")

non_empty_firm_id_new_count = df_unmatched['firm_id_new'].notna().sum()
#total_rows = len(df_unmatched)
proportion_non_empty_firm_id_new = non_empty_firm_id_new_count / total_rows

print(df_unmatched.head())
print(f"Proportion of non-empty firm_id_new in stage2: {proportion_non_empty_firm_id_new:.2%}")
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

df_unmatched.to_csv('matched2.csv',index=False)

df_final = pd.merge(df,df_unmatched,on=["序号","symbol","shortname","enddate"],how="left")
df_final['firm_id_new'] = df_final['firm_id_new_x'].combine_first(df_final['firm_id_new_y'])
print(df_final.head())
df_final.drop(["firm_y",'firm_id_new_x','firm_id_new_y'],axis=1,inplace=True)
df_final.to_csv("sheet6_merged.csv",index=False)

non_empty_firm_id_new_count = df_final['firm_id_new'].notna().sum()
#total_rows = len(df_unmatched)
proportion_non_empty_firm_id_new = non_empty_firm_id_new_count / total_rows
print(f"Proportion of non-empty firm_id_new in stage2: {proportion_non_empty_firm_id_new:.2%}")
print(non_empty_firm_id_new_count)

"""
matched_rows_df1_fuzzy = df_unmatched['firm_id_new'].notna()
df1_unmatched_fuzzy = df1_unmatched.loc[~df1_unmatched['firm'].isin(df_unmatched.loc[matched_rows_df1_fuzzy, 'firm'])]

matched_firms_fuzzy = df_unmatched.loc[matched_rows_df1_fuzzy, 'firm']
df2_unmatched_fuzzy = df2_unmatched[~df2_unmatched['firm'].isin(matched_firms_fuzzy)]


def fuzzy_match_and_print(row, choices, scorer, threshold=80):

    match, score = process.extractOne(row['firm'], choices, scorer=scorer)
    if score >= threshold:
        print(f"Matching '{row['firm']}' with '{match}' (Score: {score})")
        return match
    else:
        print(f"'{row['firm']}' has no match above the threshold.")
        return None


choices = df2_unmatched_fuzzy['firm'].tolist()
df1_unmatched_fuzzy['fuzzy_match_firm'] = df1_unmatched_fuzzy.apply(
    fuzzy_match_and_print, axis=1, choices=choices, scorer=fuzz.token_sort_ratio)
df_fuzzy_matched = pd.merge(df1_unmatched_fuzzy, df2_unmatched_fuzzy, left_on='fuzzy_match_firm', right_on='firm',
                            suffixes=('_df1', '_df2'))

df_fuzzy_matched.to_csv('fuzzy_matched.csv', index=False)

"""