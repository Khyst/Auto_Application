from bs4 import BeautifulSoup
#from request import request.urllib
import time

file = open("table_soup.html", encoding='UTF8')

#soup_file = file
soup_file = BeautifulSoup(file, 'html.parser')

# table 파싱
table_soup = soup_file.find('table')

# >> tbody 파싱
table_soup = table_soup.tbody

print(table_soup) # 출력
#print(table_soup.get_text())

# Table내 각 행을 파
selected_soups = soup_file.find_all('tr') # 한 줄씩 파싱

# 제목 부분만 파싱 (info_date)
"""print(selected_soups[0].find_all('th')[2:])"""

info_date = list()
for selected in selected_soups[0].find_all('th')[2:]:
     info_date.append(selected.get_text())

print(info_date)

# 컨텐츠(스케줄) 부분만 파싱 (time_date, date_table)
time_date = list()
date_table = list()

for selected in selected_soups[1:]:
     step = 0
     #print(selected.find_all('td'))
     today_table = list()
     
     for single_select in selected.find_all('td'): #0번 부터 : 4월 1일 시작
          
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
               #print(result_data)
          step += 1
          
     time_date.append( today_table ) # 날짜마다 시간표 추가
          

"""print(date_table)
print(time_date)"""

step = 0
for step_date in time_date:
     
     try:
          print(date_table[step], end="// ")
          
          for selected_date in step_date :
               print(selected_date, end="\t")
               
          print()
          step += 1
          
     except:
          break


     
"""
info_bool = False
for selected in selected_soups :
     if info_bool == False: # 맨 앞줄은 정보를 나타내는 데이터이므로 선택적으로 처리
          info_bool = True
          print("---------------------Info---------------------")
          print(selected)
          print("---------------------Info---------------------")
          continue
     print(selected)
     time.sleep(1)
"""

