
import requests
import re
from bs4 import BeautifulSoup
r=requests.get('http://bns.qq.com/cp/a20180619ggtrip/index.htm')
#print(r.text)

soup = BeautifulSoup(r.text,'lxml')
find = str(soup.find_all('tbody'))
#print(find)
key = find
#p1 = r"(?<=title=\").*?(?=\">)"
pattern1 = re.findall('(?<=tbody id=).*?(?=body>)',key,re.S)
#pattern1 = re.compile(p1)
#matcher1 = re.search(pattern1,key)
#print(matcher1.group())
#(?<=<h1>).+?(?=<h1>)

print(pattern1)