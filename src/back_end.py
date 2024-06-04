import pymysql
import pymysql.cursors

import requests
import json

from xml.etree.ElementTree import parse, fromstring
import xml.etree.ElementTree as ET


class Database:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='COLTm1911a1',
                             database='db_ajou',
                             cursorclass=pymysql.cursors.DictCursor)
        

        self.cursor = self.connection.cursor()
    
    #
    def fetch_data(self):

        return
    
    #
    def update_data(self):

        return
    
    #검색 시 함수
    def search_data(self):
        
        return

    def get_kipris_data_patent(self):

        url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch?astrtCont=발명&inventionTitle=센서&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="

        response = requests.get(url)
        
        # print(response.text)

        tree = ET.fromstring(response.text)
        print(tree.items)

        patents = tree.find("body").find("items")

        for patent in patents:
            print(patent.tag)

        sql = "INSERT INTO patent (applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate) VALUES (%s, %d, %s, %s, %d, %s, %s, %d, %d, %s)"

        self.cursor.execute(sql, ())
        
        return
    
    def get_kipris_data_trademark(self):

        # url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getWordSearch?searchString=롯데&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="
        url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getWordSearch?articleName=롯데&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="

        response = requests.get(url)

        print(response.text)
        
        tree = parse(response.text)

        myroot = tree.find("items")

        trademarks = myroot.findall("item")

        for trademark in trademarks:
            print(trademark)

        return
    
database = Database()

database.get_kipris_data_patent()

    