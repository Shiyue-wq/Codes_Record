import pandas as pd

#数据整理
file_policy = '/Users/wwwzhang/Library/Application Support/Kim (Kim)/userData/8fec53658e604c81a9858c3b0ac22f76/Kim file/2024-08/IN Live Agency policy adjustment for Sept. 2024.xlsx'
database = '/Users/wwwzhang/Library/Application Support/Kim (Kim)/userData/8fec53658e604c81a9858c3b0ac22f76/Kim file/2024-08/7月公会任务完成情况 Elsa side(1).xlsx'

old = pd.read_excel(file_policy, sheet_name='Old host task')
old.fillna(0, inplace=True)
new = pd.read_excel(file_policy, sheet_name='New host task')
new.fillna(0, inplace=True)
level_upgrade = pd.read_excel(file_policy, sheet_name='level upgrade task')
level_upgrade.fillna(0, inplace=True)
revenue = pd.read_excel(file_policy, sheet_name='revenue & recruitment task')
revenue.fillna(0, inplace=True)


def host(data, policy, standard, old_list, new_list, old_choice, new_choice, merge_list):
    # Ensure the merge keys are of the same data type
    data[standard] = data[standard].astype('float64')
    policy[old_choice] = policy[old_choice].astype('float64')
    policy[new_choice] = policy[new_choice].astype('float64')

    sum_old = pd.merge_asof(
        data.sort_values(standard),
        policy[old_list].sort_values(old_choice),
        left_on=standard,
        right_on=old_choice,
        direction='backward'
    )
    sum_new = pd.merge_asof(
        data.sort_values(standard),
        policy[new_list].sort_values(new_choice),
        left_on=standard,
        right_on=new_choice,
        direction='backward'
    )
    result = pd.merge(sum_old, sum_new, on=merge_list, how='left')
    return result


"""主播"""
# 处理存量主播
host_old = pd.read_excel(database, sheet_name='存量主播7月')
host_old = host_old[(host_old['开播时长小时'] >= 40) & (host_old['开播有效天数'] >= 20)]
#host_old.loc[host_old['完成档位'] == 1, '收礼钻石'] = 3000
# 处理新主播
host_new = pd.read_excel(database, sheet_name='新主播7月')
#host_new.loc[host_new['完成档位'] == 1, '收礼钻石'] = 3000

merge_list = ['org_id', 'org_name', 'member_id','收礼钻石']
old_list = ['Level_old', 'Diamond target_old', 'Reward_old']
new_list = ['Level_new', 'Diamond target_new', 'Reward_new']

# 计算存量主播和新主播的结果
sum_old = host(host_old, old, '收礼钻石', old_list, new_list, 'Diamond target_old', 'Diamond target_new',merge_list)
sum_new = host(host_new, new, '收礼钻石', old_list, new_list, 'Diamond target_old', 'Diamond target_new',merge_list)


print('存量主播总额_旧政策：', sum_old['Reward_old'].sum(), '存量主播总额_新政策：', sum_old['Reward_new'].sum())
print('新主播总额_旧政策：', sum_new['Reward_old'].sum(), '新主播总额_新政策：', sum_new['Reward_new'].sum())


"""公会"""
agency_7 = pd.read_excel(database, sheet_name='存量公会7月')
agency_7 = agency_7[['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy', '有效新主播数量']]
agency_6 = pd.read_excel(database, sheet_name='存量公会6月')
agency_6 = agency_6[['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy']]

#招新
old_list = ['Level_old', 'Diamond Target_old','Valid New Host_old','Reward_old']
new_list = ['Level_new', 'Diamond Target_new','Valid New Host_new','Reward_new']
merge_list = ['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy','有效新主播数量']

diamond = host(agency_7,revenue,'Current Diamonds of Regular Policy', old_list,new_list,'Diamond Target_old','Diamond Target_new',merge_list) #按流水得出的档位
new_host = host(agency_7,revenue,'有效新主播数量',old_list,new_list,'Valid New Host_old','Valid New Host_new',merge_list) #按新增主播数得到的档位
new = pd.merge(diamond,new_host,on=merge_list,how='left')
new.fillna(0, inplace=True)
new['旧档位diff'] = new['Level_old_x'] - new['Level_old_y']
new.loc[(new['旧档位diff'] <= 0), 'Level_old'] = new['Level_old_x']
new.loc[(new['旧档位diff'] >= 0), 'Level_old'] = new['Level_old_y']

new['新档位diff'] = new['Level_new_x'] - new['Level_new_y']
new.loc[(new['新档位diff'] <= 0), 'Level_new'] = new['Level_new_x']
new.loc[(new['新档位diff'] >= 0), 'Level_new'] = new['Level_new_y']

summ = pd.merge(new,revenue[['Level_old','Reward_old']],on='Level_old',how='left')
summ = pd.merge(summ, revenue[['Level_new','Reward_new']],on='Level_new',how='left')
summ.to_csv('xxx.csv')

sum_re = pd.merge(new[['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy','有效新主播数量','Level_old','Level_new']],revenue[['Level_old','Reward_old']],on='Level_old',how='left')
sum_re = pd.merge(sum_re,revenue[['Level_new','Reward_new']],on='Level_new',how='left')
print('招新旧政策：',sum_re['Reward_old'].sum())
print('招新新政策：',sum_re['Reward_new'].sum())

"""
#跨档
old_list = ['Level_old', 'Diamond Target_old', 'Reward Rabate_old']
new_list = ['Level_new', 'Diamond Target_new', 'Reward Rebate_new']
merge_list = ['Agency ID', 'Agency Name', 'Current Diamonds of Regular Policy']

cal_agency_7 = host(agency_7,level_upgrade, 'Current Diamonds of Regular Policy', old_list, new_list,'Diamond Target_old','Diamond Target_new',merge_list)
cal_agency_6 = host(agency_6,level_upgrade, 'Current Diamonds of Regular Policy', old_list, new_list,'Diamond Target_old','Diamond Target_new',merge_list)

agency = pd.merge(
    cal_agency_7,
    cal_agency_6,
    on=['Agency ID', 'Agency Name'],
    suffixes=('_7', '_6'),
    how='left'
)


agency['旧档位diff'] = agency['Level_old_7'] - agency['Level_old_6']
agency['新档位diff'] = agency['Level_new_7'] - agency['Level_new_6']
agency.loc[(agency['旧档位diff'] <= 0) & (agency['Level_old_7'] < 8), 'Reward Rabate_old_7'] = 0
agency.loc[(agency['新档位diff'] <= 0) & (agency['Level_new_7'] < 17), 'Reward Rebate_new_7'] = 0

agency['rewards_new'] = agency['Current Diamonds of Regular Policy_7']*agency['Reward Rebate_new_7']/100
agency['rewards_old'] = agency['Current Diamonds of Regular Policy_7']*agency['Reward Rabate_old_7']/100

print('跨档旧政策：', agency['rewards_old'].sum(), '跨档新政策：', agency['rewards_new'].sum())
agency.to_csv('agency.csv',index=False)
"""

with pd.ExcelWriter('公会政策测算.xlsx') as writer:
    sum_old.to_excel(writer, sheet_name='存量主播', index=False)
    sum_new.to_excel(writer, sheet_name='新主播', index=False)
    agency.to_excel(writer, sheet_name='跨档', index=False)
    sum_re.to_excel(writer, sheet_name='招新', index=False)
