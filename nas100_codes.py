from bs4 import BeautifulSoup
import requests
import pandas as pd

# The following codes is a simplified reference for scapping the page (https://en.wikipedia.org/wiki/Nasdaq-100).
# It will work for the historical page of 2008 - 2016. 
# I am still figuring out ways to have a program works for all years. Sorry for the inconvience.

final = pd.DataFrame(data=None)
while(True):
    # Enter the dates for the columns name and the url of the historical pages
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
    final.to_csv('Nasdaq100.csv')
