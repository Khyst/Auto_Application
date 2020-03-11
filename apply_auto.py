from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import time
import os

statue_array  = ["특별광역시", "경기도", "강원도", "충청남도", "충청북도", "경상남도", "경상북도",
                 "전라남도", "전라북도"]
statue_count = len(statue_array)
statue_index = 0
test_count = 0
test_index = 0
checked_array = []
checked_index = 0

options = webdriver.ChromeOptions()

#options = webdriver.Options()
#options.add_argument('headless')
#options.add_argument("no-sandbox")

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재

driver = webdriver.Chrome('C:/Users/kyh94/chrome_driver/chromedriver.exe', options=options)
file = open("./info.txt", "a+") #File 입축력 append 기능을 위한 준비

def arrangement_ENVIRONMENT():
     URL = "http://license.korcham.net/"
     driver.get(URL)

     # 로그인page 접속후 로그인하기
     URL += "kor/member/login.jsp"
     driver.get(URL)

     id_blank = driver.find_element_by_name('uid')
     pw_blank = driver.find_element_by_name('upwd')

     USER_ID = "<아이디를 입력하는 부분>"
     USER_PASSWORD = "<비밀번호를 입력하는 부분>"

     id_blank.send_keys(USER_ID)
     pw_blank.send_keys(USER_PASSWORD)

     driver.find_element_by_css_selector('#idMemberLogin > div.login_area01 > div.data01 > input').click()
     
def basic_AUTH():
     # 상시 시험 접수창 접속후, 약관 동의
     URL = "http://license.korcham.net/ex/dailyExam.do"
     driver.get(URL)
     driver.find_element_by_id('checkAll').click()
     driver.find_element_by_css_selector('#content_area > div > div > div.content_right > div.sub_content > div.txt_list_01_area > ul > p > span').click()

     # 옵션 지정
     driver.find_element_by_css_selector('#exam_step1 > input:nth-child(7)').click()
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_elevel_1').click()
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_program_5').click()
     
     driver.find_element_by_css_selector('#myForm > div.txt_list_01_area > p > span > a').click()
     #driver.execute_script('fnSaveDailyExam02()')

     # 주민번호 입력
     user_code_pre = "<주민번호 앞자리를 입력하는 부분>"
     user_code_rear = "<주민번호 뒷자리를 입력하는 부분>"
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno1').send_keys(user_code_pre)
     time.sleep(1)
     driver.find_element_by_css_selector('#sc_custno2').send_keys(user_code_rear)

     driver.find_element_by_css_selector('#btnCustno').click()
     time.sleep(1)
     driver.switch_to.alert.accept()
     
     # 전화번호 입력
     """
     user_phone_number = "<전화번호를 입력하는 부분>"
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
     test_index = 8
     global test_count
     test_count = 0
     
     while True:
          basic_AUTH()
          
          #시험장 선택
          time.sleep(1)
          
          select = Select(driver.find_element_by_css_selector('#selectAreaCd'))
          select.select_by_visible_text(statue_array[statue_index])
          
          driver.find_element_by_css_selector('#myForm > div.tit_box01.mb10 > span > a').click()
          table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')

          # 시험장 자리 분석후 O, X (가능성) 판단
          table_soup = BeautifulSoup(driver.page_source, 'html.parser')
          list_statue = table_soup.find_all('tr')
          test_count = len(list_statue)-1 # 구분 행은 계산에서 제외를 하기 위

          print('--------------------------------------')
          print(list_statue)
          print('--------------------------------------')
          
          print("test_index: ", test_index, end="  ")
          print("test_count: ", test_count)
          
          if(test_index >= test_count):
               print('시험장 내부 Break')
               break

          test_place_table = driver.find_element_by_css_selector('#placeInfoTable > tbody:nth-child(3)')
          test_place_selector = 'tr:nth-child('+str(test_index+1)+')'
          test_place_picked_line = test_place_table.find_element_by_css_selector(test_place_selector)
          
          print(test_place_picked_line)
          #선택 박스
          test_place_picked_line.find_element_by_css_selector('td:nth-child(1) > input').click()
          print("선택 된 시험장: ", end="")
          
          #시험장 정보
          print(test_place_picked_line.find_element_by_css_selector('td:nth-child(2)').text)
          driver.find_element_by_css_selector('#myForm > p.btn_center_01 > span:nth-child(2)').click()
          time.sleep(1)
          
          """ BeautifulSoup 활용 HTML Table 분석 """
          soup = BeautifulSoup(driver.page_source, 'html.parser')
          list_statue = soup.find_all('tr')
          
          file.write(str(list_statue) + "\n")
          time.sleep(1)
          test_index += 1
          
     
def main():
     global statue_index
     arrangement_ENVIRONMENT()

     while True:
          checking_TESTPLACE()
          
          statue_index = statue_index + 1
          
          value = input('If you wanna to cancel program, type the "q" or "quit", plz??')
          
          if statue_index >= statue_count :
               break
          #FolderNaming = "S0" + str(statue_number)
          #createFolder("S001")
          
main()
