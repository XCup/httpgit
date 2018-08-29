import requests
import re
from bs4 import BeautifulSoup
r=requests.get('https://github.com/XCup/gitpushscript')
#print(r.text)

soup = BeautifulSoup(r.text,'lxml')
find = str(soup.find_all('span'))
#print(find)
key = find
p1 = r"(?<=title=\").*?(?=\">)"
pattern1 = re.compile(p1)
matcher1 = re.search(pattern1,key)
print(matcher1.group())
#(?<=<h1>).+?(?=<h1>)