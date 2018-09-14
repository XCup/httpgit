<<<<<<< HEAD
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
=======
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
>>>>>>> 79d6a477cdaf6ace01063f6a4412dd7d8bb10d22
#(?<=<h1>).+?(?=<h1>)