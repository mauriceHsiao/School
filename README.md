大學科大四技二專交叉查榜
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