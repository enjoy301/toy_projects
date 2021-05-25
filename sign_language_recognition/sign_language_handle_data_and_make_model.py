import cv2
import mediapipe as mp
import csv
import time
import math
import os
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def record_video_and_make_csv():
    is_save = False
    label_num = -1

    def on_mouse(event, x, y, flags, param):
        global is_save
        global label_num
        if event == cv2.EVENT_LBUTTONDOWN:
            is_save = not is_save
            if is_save == True:
                label_num = input("label_num(0 ~ 34) 입력 : ")
                print("한번 더 클릭 시 데이터화가 중단됩니다...")
            else:
                print("데이터화 종료")


    def record_video():
        print("녹화를 시작합니다... (녹화 종료 == q)")
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
        print("녹화가 종료되었습니다.")
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        return file_name

    def data_merge():
        reader = csv.reader(open("files/temp_data.csv"))
        f = open("files/dataset.csv", 'a', newline='', encoding='utf-8')
        wr = csv.writer(f)
        for row in reader:
            wr.writerow(row)
        f.close()

    def make_csv(file_name):
        print("곧 영상이 실행됩니다. 화면을 클릭해 label을 입력하세요.")
        time.sleep(1)
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
                            image = cv2.rectangle(image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 0, 0), 2)
                            feature_list.append(label_num)
                            wr.writerow(feature_list)
                            feature_list = []
                previous_time = time.time()
                cv2.imshow('window2', image)
                if cv2.waitKey(1) == ord('q'):
                    break
        if os.path.isfile("./"+file_name):
            os.remove("./"+file_name)
        cap.release()
        f.close()
        hands.close()
        cv2.destroyAllWindows()

    make_csv(record_video())
    i = input("temp_data.csv에 임시 저장됨.\ndataset.csv에 추가하시겠습니까?(y|n) : ")
    if i == 'y' or i == 'Y' or i == 'yes' or i == 'YES' or i == 'Yes':
        data_merge()
    else:
        return


# data_preprocessing()
# label - c의 개수를 맞춰주는 함수
# 몇몇의 자모만 개수가 많아지는 현상을 막기 위함
def data_preprocessing():
    data = pd.read_csv("files/dataset.csv")
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
    print("label c의 최소 개수는 ", my_min, " / 최대 개수는 ", my_max)
    data = data.drop(drop_list)
    data.to_csv("files/dataset.csv", mode='w', index=False)
    print("데이터 전처리 완료")


def make_model():
    data = pd.read_csv('files/dataset.csv')
    data = np.round(data, decimals=5)
    feature_list = list(data)[:-2]
    data_input = data[feature_list].to_numpy()
    data_target = data['C'].to_numpy()
    train_input, test_input, train_target, test_target = train_test_split(data_input, data_target)
    kn = KNeighborsClassifier(n_neighbors=3)
    kn.fit(train_input, train_target)
    print("모델 점수 : ", kn.score(test_input, test_target))
    joblib.dump(kn, 'files/ML-model.pkl')
    print("pkl파일에 학습 모델 저장 완료")



#record_video_and_make_csv()
#data_preprocessing()
#make_model()