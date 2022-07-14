import certifi
from click import get_text_stream
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
mongodbUri = os.environ.get('mongodbUri')

ca = certifi.where()
client = MongoClient(mongodbUri, tlsCAFile=ca)
db = client.liquor

for p in range(7):
    url = 'https://thesool.com/front/find/M000000082/list.do?searchType=1&searchKey=%ED%98%BC%EC%88%A0&searchKind=&levelType=&searchString=&productId=&pageIndex=' + \
        str(p)+'&categoryNm=&kind='
    # get : request로 url의  html문서의 내용 요청
    html = requests.get(url)
    # html을 받아온 문서를 .content로 지정 후 soup객체로 변환
    soup = BeautifulSoup(html.content, 'html.parser')

    products = soup.select('.item')

    # 한 페이지 내의 술 목록을 하나씩 보면서 데이터 추출
    for liquor in products:
        liquorNAME = liquor.find("div", {"class": "name"}).get_text()
        manufacturer = liquor.find_all("div", {"class": "info"})[0].get_text()
        ingredient = liquor.find_all("div", {"class": "info"})[1].get_text()
        volume = liquor.find_all("div", {"class": "info"})[
            2].get_text().split("/")[0]
        proof = liquor.find_all("div", {"class": "info"})[
            2].get_text().split("/")[1].strip()
        feature = liquor.find_all("div", {"class": "info"})[
            3].get_text().strip()
        imageURL = "https://thesool.com" + \
            liquor.find("img", {"class": None})["src"]

        doc = {
            'liquorNAME': liquorNAME,
            'manufacturer': manufacturer,
            'ingredient': ingredient,
            'volume': volume,
            'proof': proof,
            'feature': feature,
            'imageURL': imageURL
        }
        # db.liquor.insert_one(doc)
