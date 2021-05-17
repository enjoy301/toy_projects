import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

data = pd.read_csv('files/temp_dataset_sum.csv')
data = np.round(data, decimals=5)
feature_list = list(data)[:-2]
data_input = data[feature_list].to_numpy()
data_target = data['C'].to_numpy()
train_input, test_input, train_target, test_target = train_test_split(data_input, data_target)
kn = KNeighborsClassifier(n_neighbors=3)
kn.fit(train_input, train_target)
print(kn.score(test_input,test_target))
joblib.dump(kn, 'files/temp_model_sun.pkl')
print("학습 모델 저장 완료")