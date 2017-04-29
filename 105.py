#coding:utf-8
import requests,re
from bs4 import BeautifulSoup
import xlwt,time
import pandas as pd

# 正規表達式
re1=r'(.+)</a></div></td>' # 抓出學校tag
re2=r'<img align="absbottom" alt="分發錄取" border="0" height="23" src="images/putdep1.png" title="分發錄取" width="23"/>' # 抓出有沒有上tag
re3=r'[\u4e00-\u9fa5]+' # 解析學校tag的校名
re4=r'\w\d+' # 甄試結果，正幾備幾
re5=r'<td scope="row" width="7%"><div align="right">' # 每個人的區隔

# 科系+有沒有上
def School():
    liCategory = []
    for x in soup.find_all('tr',align='left'):
        t1 = re.findall(re1, str(x)) # 抓出學校tag
        t2 = re.findall(re3, str(t1)) # 抓出學校名稱
        t3 = re.findall(re4, str(x.text)) # 抓出正備取
        school_str = (str(t2) + str(t3)).replace("']['"," ").replace("', '","").replace("[]","") # 學校&正備取
        if t2 != []: # 有可能出現空值學校(WTF)
            if re.findall(re2, str(x)): # 如果有上就在前面+上有上
                liCategory.append("有上" + school_str)
            else:
                liCategory.append(school_str)
    return(liCategory)

# 顯示每個人學校個數
def SchoolNumber():
    liNum = []
    n1=0
    for y2 in range(2):
        if y2 == 0:
            for y in soup.find_all('tr',align='left'): #他會一段一段去檢視(tr)
                if re5 in str(y): # 有出現這個就重新計算次數
                    if n1 != 0:
                        liNum.append(n1)
                    n1 = 0
                    n1+=1
                else: # 計算次數
                    t1 = re.findall(re1, str(y))
                    t2 = re.findall(re3, str(t1))
                    if t2 != []:
                        n1+=1
        else: # 最後一個人的個數並沒有加進去，因此要多層迴圈
            if n1 != 0:
                liNum.append(n1)
    return(liNum)

# 姓名
def name():
    liname = []
    for z in soup.find_all('td', width='8%'): # 尋找姓名tag
        if len(z.text) > 0:
            if re.findall(re4, str(z.text.replace(' ',''))): # 過濾掉正備取tag
                pass
            else:
                liname.append(z.text.replace(' ', ''))
    return(liname)

# result
def result(URL,sheet = 'very big face'):
    # http://www.com.tw 交叉查榜
    global soup
    res = requests.get(URL) # URL
    soup = BeautifulSoup(res.text, "html.parser") # 解析器
    # 呼叫function
    liCategory = School()
    liNum = SchoolNumber()
    liname = name()
    x1=1 # 第幾列
    ws = wb.add_sheet(sheet)
    # 輸入欄位名稱
    ws.write(0,0,"姓名")
    ws.write(0,1,"決定")
    ws.write(0,2,"學校")
    ws.write(0,3,"甄試結果")
    for i in range(len(liNum)): # 共有幾人
        for i2 in range(int(liNum[i])): # 把每個人有幾間學校抓出來，i2=1~42
            print(liname[i],str(liCategory[i2]).replace("['"," ").replace("']","")) # 人名 有沒有上 學校 甄試結果
            result = str(liCategory[i2]).replace("['", " ").replace("']", "")
            ws.write(x1,0,liname[i]) # 寫入人名
            if str(result[:2]) == "有上": # 如果開頭是有上，就列外處理
                ws.write(x1,1,"有上")
                ws.write(x1,2,str(result.split(" ")[1])) # 寫入學校
                if len(result.split(" ")) == 3: # 有些沒有甄試結果，所以要另外判斷
                    ws.write(x1,3,str(result.split(" ")[2])) # 寫入甄試結果
            else:
                ws.write(x1, 2, result.split(" ")[1]) # 寫入學校
                if len(result.split(" ")) == 3: # 有些沒有甄試結果，所以要另外判斷
                    ws.write(x1, 3, result.split(" ")[2]) # 寫入甄試結果
            x1 += 1 # 行數+1
        del liCategory[:i2+1] # 刪除已用過的學校及甄試結果

# 跑學校全部的科系
def SchoolAll(URL_all,SaveFile):
    global wb
    res2 = requests.get(URL_all)
    soup2 = BeautifulSoup(res2.text, "html.parser") # 解析器
    # All School URL
    re6 = r'<td id="university_dep_row_height"><div align="center" id="university_dep_row_height"><a href="(.+)">交叉查榜</a></div></td>'
    # All School Category
    re7 = r'<td colspan="2" id="university_dep_row_height"><div align="left" id="university_dep_row_height">(.+)</div><div align="left"></div></td>'
    SchoolAllUrl = re.findall(re6, str(soup2)) # 學校科系的連結
    SchoolAllCategory = re.findall(re7, str(soup2)) # 學校科系的名稱
    wb = xlwt.Workbook() # 要先宣告，之後做的東西才會存在一起，不然只會放在記憶體裡
    for r in range(len(SchoolAllUrl)):
        result('http://www.com.tw/cross/'+SchoolAllUrl[r],SchoolAllCategory[r]) # 去呼叫result function
        time.sleep(3) # 休息3秒
    wb.save(str(SaveFile) + '.xls')  # 存檔

SchoolAll('http://www.com.tw/cross/university_1107_105.html','虎尾科技大學') # 虎尾科技大學
SchoolAll('http://www.com.tw/cross/university_1101_105.html','台灣科技大學') # 台灣科技大學




# 備用方法 Pandas
# 學校及甄試結果Pandas
# liSchool = []
# df = pd.read_html('http://www.com.tw/cross/check_1107001_NO_1_105_1_3.html')[3]
# for a in range(df[1].count()+1):
#     if (isinstance(df[1][a],str) == True) or (isinstance(df[2][a],str) == True):
#         liSchool.append(str(df[1][a])+','+str(df[2][a]).replace('nan','null'))
# print(liSchool)
