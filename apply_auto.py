from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

import time
import pandas
import os

statue_array  = ["특별광역시", "경기도", "강원도", "충청남도", "충청북도", "경상남도", "경상북도",
                 "전라남도", "전라북도"]

statue_saving_route = ["S001","S002","S003","S004","S005","S006","S007","S008","S009","S010"]
test_saving_route = ["T001","T002","T003","T004","T005","T006","T007","T008","T009", "T010", "T011", "T012"]

name_of_statue_route = []
name_of_test_route = list()

statue_table_dictionery = {0: "S001", 1: "S002", 2: "S003", 3: "S004", 4: "S005", 5: "S006", 6: "S007", 7: "S008", 8: "S009", 9: "S010"} # (!)
test_table_dictionery = {0: "T001", 1: "T002", 2: "T003", 3: "T004", 4: "T005", 5: "T006", 6: "T007", 7: "T008", 8: "T009", 9: "T010", 10: "T011", 11: "T012"} # (!)

capable_apply_table = list()
table_database = list()
date_table_database = list()
info_table_database = list()

statue_count = len(statue_array)
test_per_statue_count = list()
test_count = 0

statue_index = 0
test_index = 0

"""============================================== Chrome Webdriver 옵션 =============================================="""

options = webdriver.ChromeOptions()

options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재

driver = webdriver.Chrome('C:/Users/kyh94/chrome_driver/chromedriver.exe', options=options)

"""===================================================================================================================== """

def arrangement_ENVIRONMENT():
     URL = "http://license.korcham.net/"
     driver.get(URL)

     URL += "kor/member/login.jsp"
     driver.get(URL)

     id_blank = driver.find_element_by_name('uid')
     pw_blank = driver.find_element_by_name('upwd')

     USER_ID = "<input-your-user-id>" # 아이디 입력
     USER_PASSWORD = "<input-your-user-pw>" # 비밀번호 입력

     id_blank.send_keys(USER_ID)
     pw_blank.send_keys(USER_PASSWORD)

     driver.find_element_by_css_selector('#idMemberLogin > div.login_area01 > div.data01 > input').click()
     
def basic_AUTH():
     URL = "http://license.korcham.net/ex/dailyExam.do"
     driver.get(URL)
     driver.find_element_by_id('checkAll').click()
     driver.find_element_by_css_selector('#content_area > div > div > div.content_right > div.sub_content > div.txt_list_01_area > ul > p > span').click()

     time.sleep(1)
     driver.find_element_by_css_selector('#exam_step1 > input:nth-child(7)').click()
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_elevel_1').click()
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_program_5').click()
     
     driver.find_element_by_css_selector('#myForm > div.txt_list_01_area > p > span > a').click()
     

     
     user_code_pre = "<input-your-residance-number_1>" # 주민번호 앞자리 입력
     user_code_rear = "<input-your-residance-number_2>" # 주민번호 뒷자리 입력

     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno1').send_keys(user_code_pre)
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno2').send_keys(user_code_rear)
     driver.find_element_by_css_selector('#btnCustno').click()
     time.sleep(1)

     driver.switch_to.alert.accept()
     
     
     """
     # 전화번호 입력
     user_phone_number = "<input-your-phone-number>" # 전화번호 입력
     part1_phone_number = user_phone_number[0:3]
     part2_phone_number = user_phone_number[3:7]
     part3_phone_number = user_phone_number[7:11]

     # 전화번호 파싱후 입력
     #time.sleep(1)
     #driver.find_element_by_xpath("//*[@value='" + part1_phone_number + "']/table/tbody/tr[5]/td/select")
     time.sleep(1)
     driver.find_element_by_name("sc_htelno2").send_keys(part2_phone_number)
     time.sleep(1)
     driver.find_element_by_name("sc_htelno3").send_keys(part3_phone_number)
     """

     driver.find_element_by_css_selector('#myForm > p.btn_center_01 > span').click()

def checking_TESTPLACE():
     global test_index
     test_index = 0

     global test_count
     test_count = 0

     temp_name_of_test_route = list()
     
     while True:

          basic_AUTH()
          
          time.sleep(1)
          select = Select(driver.find_element_by_css_selector('#selectAreaCd'))
          select.select_by_visible_text(statue_array[statue_index])
          
          driver.find_element_by_css_selector('#myForm > div.tit_box01.mb10 > span > a').click()
          table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')

          time.sleep(1)
          table_soup = BeautifulSoup(driver.page_source, 'html.parser')
          list_statue = table_soup.find_all('tr')
          
          test_count = len(list_statue)-1
          
          print('------------------------------------------------------------------------------------------------------------------')
          print(list_statue)
          print('------------------------------------------------------------------------------------------------------------------')
          
          print("test_index: ", test_index, end="  ")
          print("test_count: ", test_count)
          
          if(test_index >= test_count):
               break

          test_table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')
          test_selector = 'tr:nth-child('+str(test_index+1)+')'
          test_picked_line = test_table.find_element_by_css_selector(test_selector)
          print(test_picked_line)
          test_picked_line.find_element_by_css_selector('td:nth-child(1) > input').click()

          print("선택 된 시험장: ", end="")

          temp_name_of_test_route.append(str(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text))   
          print(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text)

          driver.find_element_by_css_selector('#myForm > p.btn_center_01 > span:nth-child(2)').click()

          save_table_PARSE()

          test_index += 1

     name_of_test_route.append(temp_name_of_test_route)
     temporary_record_for_ERROR(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text, name_of_test_route) # Error 체킹 

def temporary_record_for_ERROR(*args):
     temp_File = open("TEMP_NAME_TEST_PLACE.txt", "w+")

     print("시험장 원본: ", end="")
     print(args[0])
     temp_File.write(args[0])

     print("저장된 시험장 원본: ", end="")
     print(args[1])
     temp_File.write(name_of_test_route)

     temp_File.close()

def save_table_PARSE():
     
     """ BeautifulSoup 활용 HTML Table 분석 """
     save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/table_parsed.html"
     save_parse_file = open(save_url, "w+")
     time.sleep(3)
     soup = BeautifulSoup(driver.page_source, 'html.parser')
     save_table = soup.find_all('table')
     save_parse_file.write(str(save_table))
     time.sleep(1)

def analyzing_data_TABLE():
     global statue_index
     global test_index

     temp_place_database = list()
     temp_date_table = list()
     temp_info_table = list()

     while True:
          try:
               date_table = list()
               info_table = list()
               application_table = list()
               

               resource_route = "./" + statue_table_dictionery[statue_index] + "/" + test_table_dictionery[test_index] + "/" + "table_parsed.html"
               file = open(resource_route)
               soup_file = BeautifulSoup(file, 'html.parser')

               table_soup = soup_file.find(id='placeInfoTable')
               table_body_soup = table_soup.tbody
               table_rows_soup = soup_file.find_all('tr')

               for selected in table_rows_soup[0].find_all('th')[2:]:
                    info_table.append(selected.get_text())
               
               for selected in table_rows_soup[1:-2]:
                    step = 0
                    today_table = list()
                    for single_select in selected.find_all('td'):
                         if step == 0:
                              date_table.append(str(single_select.get_text().strip())) 
                         elif step >= 2 and step <= 6:
                              select_data = single_select.get_text().strip()
                              result_data = 0
                              
                              if select_data == "마감":
                                   result_data = -1  

                              elif select_data == "":
                                   result_data = 0

                              else :
                                   result_data = int(select_data)
                              
                              today_table.append( result_data )
                         step += 1
                    application_table.append( today_table )
               step = 0

               """ -------------------------------------------- 크롤링한  Data 출력 --------------------------------------------"""
               print("시험장: ", end=" ")
               try:
                    print(name_of_test_route[0][0])
               except:
                    print("Error Detected")

               print("==========================================================================================")
               print("시간대>>", end="\t|\t")
               for info in info_table:
                    print(info, end="\t")
               print("\n==========================================================================================")

               step = 0
               for step_date in application_table:
                    print(date_table[step], end="\t|\t")
                    try:
                         for selected_date in step_date :
                              print(selected_date, end="\t")
                         
                    except:
                         break

                    step += 1
                    print()
               """ -------------------------------------------- 크롤링한  Data 출력 --------------------------------------------"""
               
               temp_info_table.append(info_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함
               temp_date_table.append(date_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함
               temp_place_database.append(application_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함

               test_index += 1
               #print(statue_index, "S/ ", test_index, "T/ \n")

          except:
               if statue_index <= 9:
                    date_table_database.append(temp_date_table) # 각 지역 마다의 정보 리스트 추가
                    info_table_database.append(temp_info_table) # 각 지역 마다의 정보 리스트 추가
                    table_database.append(temp_place_database) # 각 지역 마다의 정보 리스트 추가

                    # input()

                    # save_contetns_by_CSV_temp() # 각 지역 마다의 정보 리스트 저장
                    # save_date_by_CSV_temp() # 각 지역 마다의 정보 리스트 저장
                    # save_info_time_by_CSV_temp() # 각 지역 마다의 정보 리스트 저장

                    temp_date_table = list() # 지역마다, 리스트 새로 생성
                    temp_info_table = list() # 지역마다, 리스트 새로 생성
                    temp_place_database = list() # 지역마다, 리스트 새로 생성

                    test_index = 0
                    statue_index += 1
               else :
                    break

          
def save_date_by_CSV_temp():
     try:
        pd_data_2 = pandas.DataFrame(date_table_database)
        save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/pandas_date_table.csv"
        pd_data_2.to_csv(save_url)

     except:
        print("11")
        pass

def save_info_time_by_CSV_temp():
     try:
        pd_data_3 = pandas.DataFrame(info_table_database)
        save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/pandas_info_table.csv"
        pd_data_3.to_csv(save_url)

     except:
        print("11")
        pass

def save_contetns_by_CSV_temp():
    pd_data = pandas.DataFrame(table_database[statue_index][test_index])
    pd_data.columns = info_table_database[statue_index][test_index]
    pd_data.rename(index=date_table_database[statue_index][test_index])
    save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/pandas_table.csv"
    pd_data.to_csv(save_url)
    """try:
        pd_data = pandas.DataFrame(table_database[statue_index][test_index])
        pd_data.columns = info_table_database[statue_index][test_index]
        pd_data.rename(index=date_table_database[statue_index][test_index])
        save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/pandas_table.csv"
        pd_data.to_csv(save_url)
    except:
        print("11")
        pass"""
     
def save_contents_by_CSV():
     global statue_index
     global test_index

     statue_index = 0
     test_index = 0

     pairs = [table_database, info_table_database, date_table_database]

     for statue_database in table_database :
          for statue_test_database in statue_database :
               pd_data = pandas.DataFrame(statue_test_database)

               if len(info_table_database[statue_index][test_index]) is len(pd_data.columns):
                    pd_data.columns = info_table_database[statue_index][test_index]
                    
               if len(date_table_database[statue_index][test_index]) is len(pd_data):
                    temp_dic = {}
                    for x in range(0, len(pd_data), 1):
                         temp_dic[x] = date_table_database[statue_index][test_index][x]

                    pd_data.rename(index=temp_dic)
                    pd_data['<-'] = ""
                    pd_data['일자'] = date_table_database[statue_index][test_index]
                    
                    temp_index = list()
                    temp_index.append("일자")
                    for times in info_table_database[statue_index][test_index]:
                         temp_index.append(times)
               

                    pd_data.reindex(index=temp_index)

               save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/pandas_table.csv"
               pd_data.to_csv(save_url, encoding="cp949")
               test_index += 1

          statue_index += 1
          test_index = 0
          
def transfer_alert_message_to_USER():
     pass

def main():
     global statue_index
     global test_index

     """ 1. 환경 설정 """
     arrangement_ENVIRONMENT()

     """ 2, 3, 4. 데이터 추출 """
     while True:
          checking_TESTPLACE()
          test_per_statue_count.append(test_count)
          statue_index = statue_index + 1
          
          #value = input('If you wanna to cancel program, type the "q" or "quit", plz??')
          
          if statue_index >= statue_count :
               break
     
     """ 5. 데이터 가공 """

     statue_index = 0
     test_index = 0

     analyzing_data_TABLE()

     temp_pandas_table = pandas.DataFrame(table_database)
     temp_pandas_table.to_csv("./pandas.csv", encoding="cp949")

     temp_pandas_table = pandas.DataFrame(date_table_database)
     temp_pandas_table.to_csv("./date_pandas.csv", encoding="cp949")

     temp_pandas_table = pandas.DataFrame(info_table_database)
     temp_pandas_table.to_csv("./info_pandas.csv", encoding="cp949")

     # print(pandas.DataFrame(table_database))
     # print(pandas.DataFrame(date_table_database))
     # print(pandas.DataFrame(info_table_database))


     save_contents_by_CSV()

     """
     6. 수집된 데이터를 이용해서, 필요로 하는 기능에 따라 사용자에게 알림보내기
     #1. 구글 Crhome Alert
     #2. KAKAO TALK BOT
     #3. TWITTER BOT
     """
     transfer_alert_message_to_USER()

main()
