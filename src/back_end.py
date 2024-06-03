import pymysql
import pymysql.cursors

import requests
import json


class Database:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='COLTm1911a1',
                             database='db_ajou',
                             cursorclass=pymysql.cursors.DictCursor)
    
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

        url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getWordSearch?word=가방&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="

        response = requests.post(url)
        
        print(response.text)
        
        return
    
    def get_kipris_data_trademark(self):

        # url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getWordSearch?searchString=롯데&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="
        url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getWordSearch?articleName=롯데&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I="

        response = requests.post(url)

        print(response.text)

        return

database = Database()

database.get_kipris_data_trademark()
    