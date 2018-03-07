大學科大四技二專交叉查榜爬網教學
=========================

網址：http://www.com.tw

# 安裝套件：

Python3.6
```
pip install requests
pip install BeautifulSoup4
pip install xlwt
```

# request與BeautifulSoup4解析

先用request去查看網頁，看看從server端回傳的內容長怎樣，可以用res.text去檢視他，然後用BeautifulSoup去解析，BeautifulSoup解析方式有很多種，像是select、find_all等等，依據網頁回傳的內容再去選擇。

```python
res = requests.get(URL) # URL
soup = BeautifulSoup(res.text, "html.parser") # 解析器
print(soup)
```

# 正規表達式
用正規表達式抓資料內容，先撈出學校的tag(re1)，再從tag中找出學校名字(re3)，再用re2找到學生最後選擇哪個學校，最後用re5把它們分隔開來，主要從requests回傳的網址中查看，
也可以從瀏覽器的開發人員工具中看，但不一定正確。

. 代表任意字元

\+ 代表1個以上

\w 代表任意字(除了符號、空白)

\d 代表任意數字

[\u4e00-\u9fa5] 代表任意中文

```python
re1=r'(.+)</a></div></td>' # 抓出學校tag
re2=r'<img align="absbottom" alt="分發錄取" border="0" height="23" src="images/putdep1.png" title="分發錄取" width="23"/>' # 抓出有沒有上tag
re3=r'[\u4e00-\u9fa5]+' # 解析學校tag的校名
re4=r'\w\d+' # 甄試結果，正幾備幾
re5=r'<td scope="row" width="7%"><div align="right">' # 每個人的區隔
```

# xlwt將資料寫至Excel

將爬網的資料存至Excel中，首先要先import xlwt，那是專門在寫excel的涵式庫(xlrd是專門讀取excel檔案的涵式庫)
，先用Workbook()打開暫存資料表，再用add_sheet()新增一張資料表後再新增資料上去，
要注意的點是如果要新增多張資料表，必須在前面宣告Workbook()後，在一張一張add_sheet()上去。
寫資料進去的方式很簡單，只要用write方法，告訴她第幾欄第幾列，就可以新增上去了，以下是範例，新增ABC的內容。

```python
import xlwt
wb = xlwt.Workbook()
ws = wb.add_sheet('Example')
ws.write(0, 0, A)
ws.write(1, 0, B)
ws.write(2, 0, C)
wb.save('example.xls')
```

# License
The [MIT](LICENSE) License

