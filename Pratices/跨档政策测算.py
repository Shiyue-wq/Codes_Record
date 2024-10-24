from email import policy

import pandas as pd

#数据整理
file_policy = '/Users/wwwzhang/Library/Application Support/Kim (Kim)/userData/8fec53658e604c81a9858c3b0ac22f76/Kim file/2024-08/IN Live Agency policy adjustment for Sept. 2024.xlsx'
database = '/Users/wwwzhang/Library/Application Support/Kim (Kim)/userData/8fec53658e604c81a9858c3b0ac22f76/Kim file/2024-08/7月公会任务完成情况 Elsa side(1).xlsx'
level_upgrade = pd.read_excel(file_policy, sheet_name='level upgrade task')
level_upgrade.fillna(0, inplace=True)

"""修改前置月份的时候在months，和new_level_names加上对应的名称，months需要和database里的一致"""
months = ['May DM', 'June DM', 'July DM']
new_level_names = ['May level', 'June level', 'July level']
lasted_3 = months[-3]

list = ['Level_old', 'Diamond Target_old', 'Reward Rabate_old']
#list = ['Level_new', 'Diamond Target_new', 'Reward Rebate_new']

level = 'Level_old'
#level = 'Level_new'

choice = 'Diamond Target_old'
#choice = 'Diamond Target_new'

reward = 'Reward Rabate_old'
#reward = 'Reward Rebate_new'

agency_now = pd.read_excel(database, sheet_name='存量公会now')
agency_now = agency_now[['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy', '有效新主播数量']]
agency_past = pd.read_excel(database, sheet_name='存量公会past')


def cal_level(data, policy, standard, choice, name):
    data = data[['Agency ID','Agency Name',standard]]
    data[standard] = data[standard].astype('float64')
    policy[choice] = policy[choice].astype('float64')
    result = pd.merge_asof(data.sort_values(standard),
                           policy.sort_values(choice),
                           left_on=standard,
                           right_on=choice,
                           direction='backward')
    result = result.rename({'Level_old':name}, axis='columns')
    return result


cal_now = cal_level(agency_now, level_upgrade, 'Current Diamonds of Regular Policy', choice, 'level')
agency = None
for i, (month, new_level) in enumerate(zip(months, new_level_names), 1):
    month_data = cal_level(agency_past, level_upgrade, month, choice, new_level)

    if agency is None:
        agency = pd.merge(cal_now, month_data[['Agency ID', 'Agency Name', month, new_level]], on=['Agency ID', 'Agency Name'], how='left')
        agency[f'diff_{i}'] = agency['level'] - agency[new_level]
    else:
        agency = pd.merge(agency, month_data[['Agency ID', 'Agency Name', month, new_level]], on=['Agency ID', 'Agency Name'], how='left')
        agency.fillna(0, inplace=True)
        agency[f'diff_{i}'] = agency['level'] - agency[new_level]

    agency.loc[(agency[f'diff_{i}'] <= 0) & (agency['level'] <= 8), reward] = 0

agency.loc[agency[lasted_3] == 0, reward] = 0
agency['rewards'] = agency['Current Diamonds of Regular Policy']*agency[reward]/100

print('跨档政策：', agency['rewards'].sum())
agency.to_csv('agency.csv',index=False)