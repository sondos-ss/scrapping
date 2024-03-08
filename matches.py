import requests
from bs4 import BeautifulSoup
import csv


date = input("Please enter a date by the following format MM/DD/YYY : ")
page= requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")


def main(page) :
    src= page.content
    soup=BeautifulSoup(src,"lxml")

    match_details=[]
    
    championships=soup.find_all("div",{'class':'matchCard'})
    number_of_championships= len(championships)
    
    def get_match_info(championship):
     championship_title = championship.contents[1].find('h2').text.strip()
     all_matches = championship.contents[3].find_all("div", {'class': 'item finish liItem'})
     for match in all_matches:
        teamA = match.find("div", {'class': 'teams teamA'}).text.strip()
        teamB = match.find("div", {'class': 'teams teamB'}).text.strip()
        result = match.find("div", {'class': 'MResult'}).find_all('span', {'class': 'score'})
        score = f"{result[0].text.strip()}-{result[1].text.strip()}"
        time = match.find("div", {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()
        match_details.append({"نوع البطولة": championship_title, "الفريق الأول": teamA,
                              "الفريق الثانى": teamB, "ميعاد المباراة": time, "النتيجة": score})

    for i in range (number_of_championships):
       get_match_info(championships[i]) 

    keys=match_details[0].keys()
    with open('matches-details.csv', 'w', encoding='utf-8', newline='') as output_file:
        dict_writer= csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)
        print("file ceated")

main(page)    