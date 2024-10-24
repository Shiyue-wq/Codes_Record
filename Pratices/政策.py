import pandas as pd
from scipy.optimize import minimize

file_path = '/Users/wwwzhang/Downloads/工会政策.xlsx'
df = pd.read_excel(file_path)

variables = df['variable'].tolist()
types = df['type'].tolist()
y_values = df['钻石'].tolist()
constants = df['常数'].tolist()

initial_values = constants


def objective(x):
    return -x[-1]


constraints = []

for i in range(len(variables)):
    constraints.append({'type': 'ineq', 'fun': lambda x, i=i: 0.25 - x[i]})

constraints.append({'type': 'ineq', 'fun': lambda x: 0.17 - x[0]})

# 第一个约束条件：当type=1时，对应的variable必须小于相邻两个type=0
for i in range(1, len(types)-1):
    if types[i] == 1:
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i-1] - x[i]})
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i+1] - x[i]})

# 第二个约束条件：当type=0时，variable必须大于等于0.17，但x40必须小于等于0.25
for i in range(len(types)):
    if types[i] == 0:
        if i == len(types) - 1:  # x40
            constraints.append({'type': 'ineq', 'fun': lambda x, i=i: 0.25 - x[i]})
        else:
            constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i] - 0.17})

# 第三个约束条件：当type=0时，随着x变量名称的增大，variable也增大
for i in range(len(types) - 1):
    if types[i] == 0 and types[i+1] == 0:
        constraints.append({'type': 'ineq', 'fun': lambda x, i=i: x[i+1] - x[i] - 1e-5})


# 第四个约束条件：常数一列的和-（x2/x1+x3/x2+x4/x3+...+x40/x39）<=0
def constraint4(x):
    sum_constants = sum(constants)
    fraction_sum = sum((y_values[i] * x[i]) / (y_values[i-1] * x[i-1]) for i in range(1, len(x)))
    return 0.32 - (sum_constants - fraction_sum)


constraints.append({'type': 'ineq', 'fun': constraint4})

# 变量范围
bounds = [(0.16, 0.25)] * len(variables)

# 求解非线性优化问题
solution = minimize(objective, initial_values, method='SLSQP', bounds=bounds, constraints=constraints)

optimized_values = solution.x

# 创建一个新的 DataFrame 行，包含优化后的变量值
new_row = pd.Series(optimized_values, index=df['variable'])

# 将新行添加到原始 DataFrame
df['result'] = optimized_values

# 保存结果到 Excel 文件（可选步骤）
df.to_excel('result.xlsx', index=False)

# 输出结果
for i, var in enumerate(variables):
    print(f"{var} = {optimized_values[i]}")

print("优化结果:", solution.success)
