from selenium import webdriver
import time

def enrol():
    global s_count
    s_count+=1
    print("********엇 찾았다********")
    lecture_list = [["ZE10113", "067"], ["ZE10113", "068"], ["CB16556", "059"]]
    driver.get("https://sugang.pusan.ac.kr/sugang/Login.aspx")
    time.sleep(0.1)
    driver.find_element_by_id("txtid").send_keys("202055521")
    driver.find_element_by_id("txtpassword").send_keys("rladmswhd#1")
    time.sleep(0.1)
    driver.find_element_by_id("btnlogin").click()
    time.sleep(0.2)
    for i, j in lecture_list:
        driver.find_element_by_id("txtCode").clear()
        driver.find_element_by_id("txtCode").send_keys(i)
        driver.find_element_by_id("txtBunban").clear()
        driver.find_element_by_id("txtBunban").send_keys(j)
        time.sleep(0.1)
        driver.find_element_by_id("btninsert").click()
        time.sleep(0.2)
    driver.find_element_by_id("dgSinchungList_ctl04_txtChangeBunban").send_keys("060")
    driver.find_element_by_xpath("//*[@id=\"dgSinchungList\"]/tbody/tr[4]/td[13]/a").click()
    time.sleep(0.1)
    driver.close()


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
path = "C:\Program Files\Webdriver\chromedriver.exe"
control = 1
count = 0
e_count = 0
s_count = 0
while 1:
    try:
        if control == 1:
            driver = webdriver.Chrome(path, options=options)
            driver.implicitly_wait(3)
            driver.get("https://e-onestop.pusan.ac.kr/menu/class/C03/C03006?menuId=2000030306&rMenu=03")

        driver.find_element_by_id("btn_clear").click()
        driver.find_element_by_id("opt_stdtYear").send_keys("2")
        driver.find_element_by_id("opt_collCd").send_keys("정보의생명공학대학")
        driver.find_element_by_id("opt_deptCd").send_keys("정보컴퓨터공학부")
        driver.find_element_by_id("opt_subGbn").send_keys("전공필수")
        time.sleep(0.3)
        if control == 1:
            driver.find_element_by_xpath('//*[@id="wrapper"]/section[2]/div/div/div[3]/div[2]/div/div/button').click()
        control = 0
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="opt_weekdayGbn"]/option[1]')
        driver.find_element_by_id("tf_subNm").clear()
        driver.find_element_by_id("tf_subNm").send_keys("C++프로그래밍과실습")
        driver.find_element_by_id("tf_profNm").clear()
        driver.find_element_by_id("tf_profNm").send_keys("채흥석")
        time.sleep(0.2)
        driver.find_element_by_id("btn_search").click()
        time.sleep(0.3)
        text = driver.find_element_by_xpath('//*[@id="tbl_list"]/tbody/tr[2]/td[10]').text[0:5]
        if (int(text[0:2]) - int(text[3:5])) != 0:
            enrol()
            control = 1
            continue

        driver.find_element_by_id("tf_subNm").clear()
        driver.find_element_by_id("tf_subNm").send_keys("논리회로및설계")
        driver.find_element_by_id("tf_profNm").clear()
        time.sleep(0.2)
        driver.find_element_by_id("btn_search").click()
        time.sleep(0.3)
        text = driver.find_element_by_xpath('//*[@id="tbl_list"]/tbody/tr[2]/td[10]').text[0:5]
        if (int(text[0:2]) - int(text[3:5])) != 0:
            enrol()
            control = 1
            continue

        driver.find_element_by_id("opt_subGbn").send_keys("교양필수")
        driver.find_element_by_id("tf_subNm").clear()
        driver.find_element_by_id("tf_subNm").send_keys("대학영어")
        driver.find_element_by_id("opt_weekdayGbn").send_keys("금요일")
        time.sleep(0.2)
        driver.find_element_by_id("btn_search").click()
        my_list = [9, 10]
        for i in my_list:
            time.sleep(0.3)
            temp = '//*[@id="tbl_list"]/tbody/tr['+str(i)+']/td[10]'
            time.sleep(0.1)
            text = driver.find_element_by_xpath(temp).text[0:5]
            if (int(text[0:2]) - int(text[3:5])) != 0:
                enrol()
                control = 1
                continue
        count+=1
        print(count,e_count,s_count)
    except:
        print("*********ㅠㅠ 오류*********")
        control = 1
        e_count +=1
        driver.close()