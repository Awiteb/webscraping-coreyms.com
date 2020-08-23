# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import requests
import json
import pandas as pd
print('''
    Developed by: Awiteb
    GitHub: Awiteb
    Email: Awiteb@hotmail.com
''')
maxpage = BS(requests.get("https://coreyms.com/page/1").content , "html.parser")
maxPage = maxpage.findAll('li')
maxPage = maxPage[-20].text
pageNumber = int(maxPage)

while True:
    try:
        jsonFileName = input("\n Enter name of json file: ").replace(".json" , '')
        csvFileName = input(" Enter name of csv file: ").replace(".csv" , '')
        excelFileName = input(" Enter name of excel file: ").replace(".xls" , '')
        fileJson = open(jsonFileName+'.json', 'w', encoding='utf8')
        csvFile = open(csvFileName+'.csv', 'w', encoding='utf8')
        excelFile = open(excelFileName+'.xls', 'w', encoding='utf8')
        break
    except FileNotFoundError as fileError:
        print(fileError)
fileJson.write('[\n')
data = {}
for page in range(pageNumber):
    page += 1
    print(f"-- {page} --")
    url = f"https://coreyms.com/page/{page}"
    print(url)
    r = requests.get(url)
    soup = BS(r.content , "html.parser")
    threads = soup.findAll('article')
    for thread in threads:
        if thread.find(class_ = "youtube-player"):
            headline = thread.find('a' , {'class': "entry-title-link"}).text
            summarydiv = thread.find('div' , {'class': "entry-content"})
            summary = summarydiv.find('p').text
            vid = thread.find(class_ = "youtube-player").get('src')
            date = thread.find('time').text
            data['Headline'] = headline
            data['Summary'] = summary
            data['Video'] = vid
            data['Date'] = date
            dataJson = json.dumps(data , ensure_ascii=False)
            fileJson.write(dataJson + ',\n')
fileJson.close()
readJson = open(jsonFileName+'.json' , 'r', encoding='utf8')
stringJson = readJson.read()
readJson.close()
editJson = stringJson.strip(',\n')
fileJson = open(jsonFileName+'.json', 'w', encoding='utf8')
fileJson.write(editJson + '\n]')
fileJson.close()
print(f"\n\n Done save all data on {jsonFileName}.json")
readJson = pd.read_json(f"{jsonFileName}.json")
readJson.to_csv(f"{csvFileName}.csv")
print(f"\n\n Done save all data on {csvFileName}.csv")
readJson.to_excel(f"{excelFileName}.xls")
print(f"\n\n Done save all data on {excelFileName}.xls\n")
csvFile.close()
excelFile.close()
