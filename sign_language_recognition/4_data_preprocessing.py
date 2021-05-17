import pandas as pd
import random

i = input("데이터 확인=0 //// 데이터 전처리=else -> ")
data = pd.read_csv("https://raw.githubusercontent.com/eunjong147/tech/main/sklearn/dataset_ver_sun.csv")
if i=='0':
    print(data.head(2))
    print(data.tail(2))
else:
    value_data = pd.DataFrame(pd.value_counts(data[list(data)[-1]].values,sort=False))
    my_min = value_data[0].min()
    my_max = value_data[0].max()
    drop_list = []
    for i in range(0, 35):
        temp_list = data.index[data['C'] == i].tolist()
        my_abs = len(temp_list) - my_min
        if my_abs <= 0:
            continue
        a = random.sample(range(0, len(temp_list)), my_abs) #temp_list의 인덱스
        for j in a:
            drop_list.append(temp_list[j])
    print("최소갯수는 ",my_min)
    print("최대갯수는 ",my_max)
    answer = input("진짜 지울려면 1 : ")
    if answer == '1':
        data = data.drop(drop_list)
        data.to_csv("files/temp_dataset_sum.csv", mode='w', index=False)
