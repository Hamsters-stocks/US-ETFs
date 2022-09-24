from bs4 import BeautifulSoup
import requests
import pandas as pd

# Here is an another way to deducing the past ETFs members
# As S&P500 is relatively stable and seldom make changes, we can work out the path of the evolution of the existing lists bit by bit.

# Get the S&P 500 members at the moment
SP500 = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components').text
soup = BeautifulSoup(SP500,'lxml')
List = soup.find('table')
tickers = List.find_all('a', class_ = 'external text')
final = []
for ticker in tickers:
    if ticker.text != 'reports':
        final.append(ticker.text)

# Get the changes of the list in the past 
SP500_changes = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components').text
soup1 = BeautifulSoup(SP500_changes,'lxml')
Listraw = soup1.find_all('table')
List1 = Listraw[1]
result1 = List1.find_all('td')
L1 = []
for x in result1:
    L1.append(x.text)
L2 = [L1[i:i+6] for i in range(0,len(L1),6)]
df = pd.DataFrame(L2)
df = df.drop([2,4,5], axis=1)
df.columns = ['date', 'add', 'remove']
df.set_index('date', inplace = True)
df.index = pd.to_datetime(df.index)
df = df.iloc[3:]


# Find the past holdings by undoing every change (Remove the newly added ones and restore the deleted ones)
sp = pd.DataFrame(data=None)
for Date, rows in df.iterrows():
    try:
        if type(rows[0]) != float:
            final.remove(rows[0])

        if type(rows[1]) != float:
            final.append(rows[1])
        df2 = pd.DataFrame([final], index=[Date])
        sp = pd.concat([sp, df2], axis=0)
    except:
        continue

 
sp.to_csv('S&P500.csv')
