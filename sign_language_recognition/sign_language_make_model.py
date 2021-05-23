import cv2
import mediapipe as mp
import csv
import time
import math
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def make_csv():
    is_save = False
    label_num = -1

    def on_mouse(event, x, y, flags, param):
        global is_save
        global label_num
        if event == cv2.EVENT_LBUTTONDOWN:
            is_save = not is_save
            if is_save == True:
                label_num = input("label_num : ")

    def record_video():
        global w
        global h
        cv2.namedWindow('window')
        cap = cv2.VideoCapture(0)
        w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        file_name = 'files/output.avi'
        out = cv2.VideoWriter(file_name, fourcc, fps, (w, h))
        while True:
            success, image = cap.read()
            if not success:
                continue
            out.write(image)
            image = cv2.flip(image, 1)
            cv2.imshow('window', image)
            if cv2.waitKey(1) == ord('q'):
                break
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        return file_name

    def data_merge():
        reader = csv.reader(open("files/temp_data.csv"))
        f = open("files/temp_dataset.csv", 'a', newline='', encoding='utf-8')
        wr = csv.writer(f)
        for row in reader:
            wr.writerow(row)
        f.close()

    def make_csv(file_name):
        cv2.namedWindow('window2')
        cv2.setMouseCallback('window2', on_mouse)
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)
        f = open("files/temp_data.csv", 'w', newline='', encoding='utf-8')
        wr = csv.writer(f)
        cap = cv2.VideoCapture(file_name)
        FPS = 10
        count = 0
        feature_list = []
        dot_list = [4, 8, 12, 14, 16, 18, 20]
        previous_time = time.time()
        while True:
            time_delay = time.time() - previous_time
            if time_delay > (1.0 / FPS):
                success, image = cap.read()
                if success != True:
                    count += 1
                    if count > 5:
                        break
                    continue
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        if is_save == True:
                            mean_x = hand_landmarks.landmark[0].x  # x가 왼오 0이 왼 1이 오
                            mean_y = hand_landmarks.landmark[0].y  # y가 위아래 0이 젤위 1이 젤아래
                            min_x = w - 1;
                            max_x = 0.0;
                            min_y = h - 1;
                            max_y = 0.0
                            for i in range(0, 21):  # 요기부터
                                hlm = hand_landmarks.landmark[i]
                                if hlm.x * w > max_x:
                                    max_x = hlm.x * w
                                if hlm.x * w < min_x:
                                    min_x = hlm.x * w
                                if hlm.y * h > max_y:
                                    max_y = hlm.y * h
                                if hlm.y * h < min_y:
                                    min_y = hlm.y * h
                            for i in dot_list:
                                hlm = hand_landmarks.landmark[i]
                                feature_list.append(((hlm.x - mean_x) * w) / (max_x - min_x))
                                feature_list.append((hlm.y - mean_y) * h / (max_y - min_y))
                            d8 = hand_landmarks.landmark[8]
                            d12 = hand_landmarks.landmark[12]
                            d16 = hand_landmarks.landmark[16]
                            d23 = math.sqrt(pow(d8.x * w - d12.x * w, 2) + pow(d8.y * h - d12.y * h, 2))
                            d34 = math.sqrt(pow(d16.x * w - d12.x * w, 2) + pow(d16.y * h - d12.y * h, 2))
                            feature_list.append(d23 / d34 - 1)
                            feature_list.append((max_y - min_y) / (max_x - min_x) - 1)
                            image = cv2.rectangle(image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 0, 0),
                                                  2)
                            feature_list.append(label_num)
                            wr.writerow(feature_list)
                            feature_list = []  # 요기까지 오른손 용
                previous_time = time.time()
                cv2.imshow('window2', image)
                if cv2.waitKey(1) == ord('q'):
                    break
        cap.release()
        f.close()
        hands.close()
        cv2.destroyAllWindows()

    i = input("입력(0 or else) : ")  # 0이면 녹화시작 파일이름이면 그 동영상으로
    if i == '0':
        file_name = record_video()
    else:
        file_name = "files/" + i
    make_csv(file_name)

    j = input("입력(0 or else) : ")
    if i == '0':
        data_merge()

def data_preprocessing():
    i = input("데이터 확인=0 //// 데이터 전처리=else -> ")
    data = pd.read_csv("https://raw.githubusercontent.com/eunjong147/tech/main/sklearn/dataset_ver_sun.csv")
    if i == '0':
        print(data.head(2))
        print(data.tail(2))
    else:
        value_data = pd.DataFrame(pd.value_counts(data[list(data)[-1]].values, sort=False))
        my_min = value_data[0].min()
        my_max = value_data[0].max()
        drop_list = []
        for i in range(0, 35):
            temp_list = data.index[data['C'] == i].tolist()
            my_abs = len(temp_list) - my_min
            if my_abs <= 0:
                continue
            a = random.sample(range(0, len(temp_list)), my_abs)  # temp_list의 인덱스
            for j in a:
                drop_list.append(temp_list[j])
        print("최소갯수는 ", my_min)
        print("최대갯수는 ", my_max)
        answer = input("진짜 지울려면 1 : ")
        if answer == '1':
            data = data.drop(drop_list)
            data.to_csv("files/temp_dataset_sum.csv", mode='w', index=False)

def make_model():
    data = pd.read_csv('files/temp_dataset_sum.csv')
    data = np.round(data, decimals=5)
    feature_list = list(data)[:-2]
    data_input = data[feature_list].to_numpy()
    data_target = data['C'].to_numpy()
    train_input, test_input, train_target, test_target = train_test_split(data_input, data_target)
    kn = KNeighborsClassifier(n_neighbors=3)
    kn.fit(train_input, train_target)
    print(kn.score(test_input, test_target))
    joblib.dump(kn, 'files/temp_model_sun.pkl')
    print("학습 모델 저장 완료")