from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select

import time
import pandas
import os, sys

statue_array  = ["특별광역시", "경기도", "강원도", "충청남도", "충청북도", "경상남도", "경상북도",
                 "전라남도", "전라북도"]

statue_saving_route = ["S001","S002","S003","S004","S005","S006","S007","S008","S009","S010"]
test_saving_route = ["T001","T002","T003","T004","T005","T006","T007","T008","T009", "T010", "T011", "T012", "T013", "T014"]

name_of_statue_route = []
name_of_test_route = list()

table_database = list()
date_table_database = list()
info_table_database = list()
test_place_name_database = dict()

statue_count = len(statue_array)
test_count = 0

statue_index = 0 # 시험장 검사할 인덱스 ( 지역 인덱스 )
test_index = 0 # 시험장 검사할 인덱스 ( 시험장 인덱스 )

"""============================================== Chrome Webdriver 옵션 =============================================="""
#os.system('chrome_run.bat')

options = webdriver.ChromeOptions()

#options.add_argument('headless') # 화면을 띄우지 않고 사용, 속도 향상
options.add_argument("no-sandbox")

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재

driver = webdriver.Chrome('C:/Users/kyh94/chrome_driver/chromedriver.exe', options=options)

"""===================================================================================================================== """

""" 1. 웹에서 html > table 소스 크롤링 """
def arrangement_ENVIRONMENT():
     URL = "http://license.korcham.net/"
     driver.get(URL)

     URL += "kor/member/login.jsp"
     driver.get(URL)

     id_blank = driver.find_element_by_name('uid')
     pw_blank = driver.find_element_by_name('upwd')

     USER_ID = "<아이디 입력칸>" # 아이디 입력
     USER_PASSWORD = "<비밀번호 입력칸>" # 비밀번호 입력

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
     

     
     user_code_pre = "<주민번호 앞부분 입력칸>" # 주민번호 앞자리 입력
     user_code_rear = "<주민번호 뒷부분 입력칸>" # 주민번호 뒷자리 입력

     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno1').send_keys(user_code_pre)
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno2').send_keys(user_code_rear)
     driver.find_element_by_css_selector('#btnCustno').click()
     time.sleep(1)

     driver.switch_to.alert.accept()
     
     """
     # 전화번호 입력
     user_phone_number = "<전화번호 입력칸 (- 제외)>" # 전화번호 입력
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

def option_1(): # check_TESTPLACE 포함
     selection = input('mode: ')
     global statue_index

     if selection == "1":
          print("selection 1 is seleccted")
          while True:
               checking_TESTPLACE()
               statue_index = statue_index + 1
               
               if statue_index >= statue_count :
                    break
     
     elif selection == "2": # 특정 시험장 크롤링 (OPTION)
          print("selection 2 is seleccted")
          checking_particular_TESTPLACE()

     else: # 크롤링 하지 않고 빠져나감
          pass


def save_place_name(save_title):
     pass
     """file = open("./test_place_name", "w+")

     if save_title == "\n":
          file.write("\n")
     else :
          file.write(statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + ":" + save_title + "\n")

     file.close()"""

def checking_TESTPLACE(): # 모든 시험장 크롤링 (OPTION)
     global test_index
     test_index = 0
     
     global test_count
     test_count = 0

     first_flag = True
     temp_name_of_test_route = list()
     
     while True: 
          if first_flag == False: # 첫번째 프로세스(First_Flag)인지 검사
               if(test_index >= test_count):
                    first_flag = True
                    save_place_name("\n")
                    break

          basic_AUTH()
          
          time.sleep(1)
          select = Select(driver.find_element_by_css_selector('#selectAreaCd'))
          select.select_by_visible_text(statue_array[statue_index])
          
          driver.find_element_by_css_selector('#myForm > div.tit_box01.mb10 > span > a').click()
          table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')

          time.sleep(1)
          table_soup = BeautifulSoup(driver.page_source, 'html.parser')
          list_statue = table_soup.find_all('tr')
          
          if first_flag == True:
               test_count = len(list_statue)-1 # 시험지역에 따른 시험장 갯수 설정
               first_flag = False # 초기 프로세스 검사
          
          print("시험지역 번호(statue_index): ", statue_saving_route[statue_index])
          print("시험장 번호(test_index): ", test_saving_route[test_index], end="  ")
          print('------------------------------------------------------------------------------------------------------------------')
          print("시험지역에 따른 시험장 갯수(test_count): ", test_count)

          test_table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')
          test_selector = 'tr:nth-child('+str(test_index+1)+')'
          test_picked_line = test_table.find_element_by_css_selector(test_selector)
          test_picked_line.find_element_by_css_selector('td:nth-child(1) > input').click()

          temp_name_of_test_route.insert(test_index, str(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text))   
          
          driver.find_element_by_css_selector('#myForm > p.btn_center_01 > span:nth-child(2)').click()

          save_table_PARSE(temp_name_of_test_route[test_index], False)

          test_index += 1

     name_of_test_route.insert(statue_index, temp_name_of_test_route)
     #temporary_record_for_ERROR(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text, name_of_test_route) # Error 체킹 

def checking_particular_TESTPLACE(): # 특정 시험장 크롤링 (OPTION)
     # 특정 시험장에 대해 데이터 긁어오기 (statue_index와, test_index 받아옴)

     statue_index = int(input("지역 번호 : "))
     test_index = int(input("시험장 번호: "))

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

     # Crawling Test TimeTable

     print('------------------------------------------------------------------------------------------------------------------')
     print(list_statue)
     print('------------------------------------------------------------------------------------------------------------------')
     
     print("statue_index: ", statue_array[statue_index])
     print("test_index: ", test_index, end="  ")

     test_table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')

     test_selector = 'tr:nth-child('+str(test_index+1)+')'

     test_picked_line = test_table.find_element_by_css_selector(test_selector)

     test_picked_line.find_element_by_css_selector('td:nth-child(1) > input').click()

     driver.find_element_by_css_selector('#myForm > p.btn_center_01 > span:nth-child(2)').click()

     save_table_PARSE(str(test_picked_line.find_element_by_css_selector('td:nth-child(2)').text), True) 
     # 특정 시험장에 대한 크롤링 (test_index, statue_index 넘어감)

def temporary_record_for_ERROR(*args):
     temp_File = open("TEMP_NAME_TEST_PLACE.txt", "w+")

     print("시험장 원본: ", end="")
     print(args[0])
     temp_File.write(args[0])

     print("저장된 시험장 원본: ", end="")
     print(args[1])
     temp_File.write(name_of_test_route)

     temp_File.close()

def save_table_PARSE(save_title, particular):
     
     """ BeautifulSoup 활용 HTML Table 분석 """
     print(save_title, "를 저장\n")
     save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_code" + ".html"

     if not particular : 
          save_place_name(save_title)

     save_parse_file = open(save_url, "w+")
     time.sleep(3)
     soup = BeautifulSoup(driver.page_source, 'html.parser')
     save_table = soup.find_all('table')
     save_parse_file.write(str(save_table))
     time.sleep(1)
     save_parse_file.close()

""" 2. 크롤링한 데이터 분석 및 커스터 마이징 """
def option_2(): # save_to_CSV 포함
     selection = input('mode: ')
     if selection == "1":
          save_contents_by_CSV()
     elif selection == "2":
          save_contents_by_particular_CSV()
     else:
          pass

def analyzing_data_TABLE(): # 모든 테이블에 대해서 Analyzing 작업 수행
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
               

               resource_route = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_code" + ".html"
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
                    print(test_place_name_database[statue_saving_route[statue_index]][test_saving_route[test_index]].rstrip("\n"))
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
               
               temp_info_table.insert(test_index, info_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함
               temp_date_table.insert(test_index, date_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함
               temp_place_database.insert(test_index, application_table) # 각 시험장마다의 정보를 임시 테이블에 추가 -> 임시 테이블 리스트를 하나의 지역으로 묶기 위함

               test_index += 1

          except:
               if statue_index <= 9:
                    date_table_database.insert(statue_index, temp_date_table) # 각 지역 마다의 정보 리스트 추가
                    info_table_database.insert(statue_index, temp_info_table) # 각 지역 마다의 정보 리스트 추가
                    table_database.insert(statue_index, temp_place_database) # 각 지역 마다의 정보 리스트 추가


                    temp_date_table = list() # 지역마다, 리스트 새로 생성
                    temp_info_table = list() # 지역마다, 리스트 새로 생성
                    temp_place_database = list() # 지역마다, 리스트 새로 생성

                    test_index = 0
                    statue_index += 1
               else :
                    break

def save_contents_by_particular_CSV(): # 특정 콘텐츠를 CSV 파일로 변환
     global statue_index
     global test_index

     statue_index = int(input("지역 번호 : "))
     test_index = int(input("시험장 번호: "))

     pd_data = pandas.DataFrame(table_database[statue_index][test_index])

     if len(info_table_database[statue_index][test_index]) is len(pd_data.columns):
          pd_data.columns = info_table_database[statue_index][test_index]
                    
     if len(date_table_database[statue_index][test_index]) is len(pd_data):
          pd_data.insert(0, '일자', date_table_database[statue_index][test_index])
          
          temp_index = list()
          temp_index.append("일자")

          for times in info_table_database[statue_index][test_index]:
               temp_index.append(times)

          pd_data.reindex(index=temp_index)

     save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_table" + ".csv"

     pd_data.to_csv(save_url, encoding="cp949")

def save_contents_by_CSV(): # 모든 콘텐츠를 CSV 파일로 변환
     global statue_index
     global test_index

     statue_index = 0
     test_index = 0

     pairs = [table_database, info_table_database, date_table_database]

     # temp_pandas_test_place_table = pandas.DataFrame(name_of_test_route)
     # temp_pandas_test_place_table.to_csv("./place_pandas.csv", encoding="cp949")

     # temp_pandas_table = pandas.DataFrame(table_database)
     # temp_pandas_table.to_csv("./pandas.csv", encoding="cp949")

     # temp_pandas_table = pandas.DataFrame(date_table_database)
     # temp_pandas_table.to_csv("./date_pandas.csv", encoding="cp949")

     # temp_pandas_table = pandas.DataFrame(info_table_database)
     # temp_pandas_table.to_csv("./info_pandas.csv", encoding="cp949")

     for statue_database in table_database :
          for statue_test_database in statue_database :
               pd_data = pandas.DataFrame(statue_test_database)

               if len(info_table_database[statue_index][test_index]) is len(pd_data.columns):
                    pd_data.columns = info_table_database[statue_index][test_index]
                    
               if len(date_table_database[statue_index][test_index]) is len(pd_data):
                    pd_data.insert(0, '일자', date_table_database[statue_index][test_index])
                    
                    temp_index = list()
                    temp_index.append("일자")

                    for times in info_table_database[statue_index][test_index]:
                         temp_index.append(times)

                    pd_data.reindex(index=temp_index)

               save_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_table" + ".csv"
               pd_data.to_csv(save_url, encoding="cp949")
               test_index += 1

          statue_index += 1
          test_index = 0

def test_place_name_database_READ():

     file = open("test_place_name.txt", "r+")
     
     test_place_data = file.readlines()
     temp_data_list = dict()

     statue_code = "S001" # 초기값

     for part_of_data in test_place_data:
          if part_of_data == "\n":
               # test_place_name_database.insert(statue_code, temp_data_list)
               test_place_name_database[statue_code] = temp_data_list
               temp_data_list = dict()
               continue

          statue_code = part_of_data[0:4]
          test_code = part_of_data[5:9]
          place_name = part_of_data[10:]

          temp_data_list[test_code] = place_name

     print(test_place_name_database)

def option_3(): # analyzing_data_TABLE_2() 포함
     selection = input('mode: ')

     if selection == "1":
          analyzing_data_TABLE_2()

     elif selection == "2":
          analyzing_particular_data_TABLE_2()

     else:
          pass

def analyzing_particular_data_TABLE_2():
     global statue_index
     global tset_index

     statue_index = int(input("지역 번호 : "))
     test_index = int(input("시험장 번호: "))

     print(statue_saving_route[statue_index])
     print(test_saving_route[test_index])

     read_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_table" + ".csv"
     read_dataframe = pandas.read_csv(read_url, sep=",", dtype="unicode", encoding="cp949")

     print(read_dataframe)

     read_url = "./" + statue_saving_route[statue_index] + "/" + test_saving_route[test_index] + "/" + "result_table" + ".csv"
     read_dataframe = pandas.read_csv(read_url, sep=",", dtype="unicode", encoding="cp949")

     selected_date = read_dataframe.iloc[:, 1]
     selected_test_data = read_dataframe.iloc[:, 2:]

     selected_test_data_info = selected_test_data.columns # list형태(Array)로 정보를 반납
     selected_test_data_table = selected_test_data.values # list형태(Array)로 정보를 반납

     data_list = list()
     row_count = 0
     col_count = 0

     file = open("test_place_name.txt", "r+")
     test_place_data = file.readlines()

     temp_data_list = dict()
     statue_code = "S001" # 초기값
     for part_of_data in test_place_data:
          if part_of_data == "\n":
               # test_place_name_database.insert(statue_code, temp_data_list)
               test_place_name_database[statue_code] = temp_data_list
               temp_data_list = dict()
               continue

          statue_code = part_of_data[0:4]
          test_code = part_of_data[5:9]
          place_name = part_of_data[10:]

          # temp_data_list.insert(test_code, place_name)
          temp_data_list[test_code] = place_name

          # print(statue_code,"//", test_code, "::", place_name)


     # print(test_place_name_database)

     for row_select in selected_test_data_table:
          col_count = 0
          for data_select in row_select:

               if int(data_select) > 1:
                    temp_data_list = list()
                    temp_data_list.append(row_count)
                    temp_data_list.append(col_count)
                    temp_data_list.append(data_select)
                    data_list.append(temp_data_list)   

               col_count += 1

          row_count += 1

     print("==================================================================")

     test_place_name_database[statue_saving_route[statue_index]][test_saving_route[test_index]] = test_place_name_database[statue_saving_route[statue_index]][test_saving_route[test_index]].rstrip("\n")

     print("시험장: ",test_place_name_database[statue_saving_route[statue_index]][test_saving_route[test_index]])

     print("==================================================================\n\n")

     if len(data_list) == 0:
          print("응시 가능한 시험일정이 없습니다.")

     else:
          current = int(selected_date[0][6:8])
          print(current, "월 일정")
          print("==================================================================")

          for select_list in data_list:
               row = select_list[0]
               col = select_list[1]
               
               year = int(selected_date[row][0:4])
               month = int(selected_date[row][6:8])
               date = int(selected_date[row][10:12])

               # print(year, month, date)

               if current < month:
                    current += 1
                    print(current, "월 일정")
                    print("==================================================================")

               print(selected_date[row])
               print("-----------------------------------------------------------------")
               print(selected_test_data_info[col], "-->", select_list[2], "자리 남음\n")

def analyzing_data_TABLE_2():
     test_index = 0
     statue_index = 0
     while True:
          while True:
               analyzing_data_TABLE_2()
               test_index = test_index + 1

               if test_index >= test_count :
                    break

          statue_index = statue_index + 1     
          
          if statue_index >= statue_count :
               break

def option_4(): # transfer_DATA 포함
     selection = input('mode: ')

     if selection == "kakao" or 'k':
          transfer_DATA_to_KAKAOTALK()

     elif selection == 'twiter' or 't':
          transfer_DATA_to_TWITER()

     else:
          pass    

""" 3. 분석한 데이터를 통한 알림 기능 보내기 """
def transfer_DATA_to_KAKAOTALK():
     pass

def transfer_DATA_to_TWITER():
     pass

def main():
     global statue_index
     global test_index

     """ 1. 환경 설정 """
     arrangement_ENVIRONMENT()

     """ 2, 3, 4. 데이터 추출 """
     option_1() # check_TESTPLACE 포함

     """ 5. 데이터 가공 """
     statue_index = 0
     test_index = 0

     test_place_name_database_READ()

     analyzing_data_TABLE()

     option_2() # save_to_CSV 포함

     option_3() # analyzing_data_TABLE_2() 포함

     
     """ 
          6. 수집된 데이터를 이용해서, 필요로 하는 기능에 따라 사용자에게 알림보내기 
     
               #1. 구글 Crhome Alert
               #2. KAKAO TALK BOT
               #3. TWITTER BOT
     """

     option_4() # transfer_DATA 포함

main()
