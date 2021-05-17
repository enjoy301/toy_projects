from selenium import webdriver
from datetime import datetime
import time

time1 = datetime(2021, 3, 2, 0, 0, 0)
time2 = datetime.now()
weeks = int(((time2-time1).days)/7) + 1
print(str(weeks)+"주차")

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_extension('C:\ofjjanaennfbgpccfpbghnmblpdblbef.crx')
path = "C:\Program Files\Webdriver\chromedriver.exe"

driver = webdriver.Chrome(path, options=options)
driver.implicitly_wait(3)
driver.get('https://plato.pusan.ac.kr/')

driver.find_element_by_id("input-username").send_keys("202055521")
driver.find_element_by_id("input-password").send_keys("ghbusan@1")
driver.find_element_by_xpath('//*[@id="page-header"]/div[1]/div/div[2]/form/div/input[3]').click()

time.sleep(5)

notice_list = driver.find_elements_by_css_selector('[class|="modal notice_popup ui-draggable"]')
z_index_list = []
for i in notice_list:
    z_index_list.append(i.value_of_css_property("z-index"))

for i in range(len(notice_list)):
    max_index = z_index_list.index(max(z_index_list))
    notice_list[max_index].find_element_by_class_name('close_notice').click()
    z_index_list.pop(max_index)
    notice_list.pop(max_index)

lecture_index = [1,3,4,5,6]#1~6
for i in lecture_index:
    checker = 1
    check_list = []
    link = '//*[@id="page-content"]/div/div[1]/div[2]/ul/li['+str(i)+']/div/a/div'
    driver.find_element_by_xpath(link).click()
    li = driver.find_elements_by_css_selector('[title|="온라인출석부"]')
    if len(li) == 1:
        li[0].click()
    else:
        checker = 0
        driver.find_element_by_css_selector('[title|="학습진도현황"]').click()

    if checker == 1: # 데과입 빼고 다
        tbl = driver.find_element_by_css_selector('[class|="table  table-bordered user_progress_table table-coursemos"]')
        tbody = tbl.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')
        control = 0
        for j in trs:
            child = j.find_elements_by_xpath('.//*')[0]
            if child.text == str(weeks+1):
                break
            if child.text == str(weeks):
                control = 1
            if child.text == str(weeks):
                if j.text[-3] == 'X':
                    check_list.append(j.find_element_by_class_name('text-left').text)
            elif control == 1:
                if j.text[-1] == 'X':
                    check_list.append(j.find_element_by_class_name('text-left').text)
    else:
        tbl = driver.find_element_by_css_selector(
            '[class|="table table-bordered user_progress table-coursemos"]')
        tbody = tbl.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')
        control = 0
        for j in trs:
            child = j.find_elements_by_xpath('.//*')[0]
            if child.text == str(weeks + 1):
                break
            if child.text == str(weeks):
                control = 1
            if child.text == str(weeks) or control == 1:
                if j.text[-4:] != "100%":
                    check_list.append(j.find_element_by_class_name('text-left').text)
    print(check_list)
    driver.find_element_by_xpath('//*[@id="page-content"]/div[1]/nav/ol/li[3]/a').click()

    li_week = driver.find_elements_by_css_selector('[class|="weeks ubsweeks ubformat"]')[
        2].find_elements_by_css_selector('[role|="region"')
    housekeeper = 0
    li_week = li_week[weeks-1:]
    for i in li_week:
        time.sleep(1)
        li_video = i.find_elements_by_css_selector('[class|="activity vod modtype_vod "]')
        if len(li_video) == 0:
            break
        for j in li_video:
            if len(j.find_elements_by_css_selector('[class|="availabilityinfo isrestricted"]')) > 0:
                continue
            else:
                imp = j.find_element_by_class_name("instancename")

                for t in check_list:
                    if imp.text[:-4] in t:
                        housekeeper = 1
                        break
                if housekeeper != 1:
                    continue
                housekeeper = 0
                imp.click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="vod_viewer"]').click()

                while True:
                    left_hour = driver.find_element_by_xpath('//*[@id="my-video"]/div[4]/div[7]/div').text
                    if "-0:00" == left_hour:
                        break
                    time.sleep(60)

                time.sleep(5)
                driver.find_element_by_class_name('vod_close_button').click()
                time.sleep(2)  # 동영상 재생 시간

                try:
                    driver.switch_to.alert.accept()
                except:
                    pass
                driver.switch_to.window(driver.window_handles[0])

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(.1)
    driver.find_element_by_xpath('//*[@id="page-header"]/div[2]/div[1]/a').click()
