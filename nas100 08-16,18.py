from bs4 import BeautifulSoup
import requests
import pandas as pd


final = pd.DataFrame(data=None)
while(True):
    date = input('Date:')
    url = input('url:')

    NAS100 = requests.get(url).text
    soup = BeautifulSoup(NAS100, 'lxml')
    Str = soup.find('ol').text

    Lst = Str.split("\n")
    L = []
    for x in Lst:
        S = x.find("(")
        E = x.find(")")
        L.append(x[S + 1:E])

    result = pd.DataFrame(L,columns = [date])
    final = pd.concat([final,result],axis = 1)
    print(final)
    final.to_csv('Nasdaq100_08after.csv')
