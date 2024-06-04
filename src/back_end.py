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
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
        

        self.cursor = self.connection.cursor()
    
    def fetch_trademark(self):

        return
    
    def fetch_patent(self):

        return
    
    def update_trademark(self):

        return
    
    def update_patent(self):

        return
    
    def search_trademark(self):
        
        return
    
    def search_patent(self):

        return

    def get_kipris_data_patent(self):

        for i in range(1,50):

            url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch?astrtCont=발명&inventionTitle=센서&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I=&pageNo=" + str(i)

            response = requests.get(url)
            
            # print(response.text)

            tree = ET.fromstring(response.text)
            # print(tree.items)


            patents = tree.find("body").find("items")

            sql = "INSERT INTO patent (applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            for patent in patents:
                applicantName = patent.find("applicantName").text
                registrationNumber = patent.find("registerNumber").text
                registerStatus = patent.find("registerStatus").text
                applicationDate = patent.find("applicationDate").text
                applicationNumber = patent.find("applicationNumber").text
                inventionTitle = patent.find("inventionTitle").text
                openDate = patent.find("openDate").text
                openNumber = patent.find("openNumber").text
                publicationNumber = patent.find("publicationNumber").text
                publishDate = patent.find("publicationDate").text

                
                if str(publicationNumber) == "None":
                    publicationNumber = '0'

                if str(registrationNumber) == "None":
                    registrationNumber = '0'

                # print(type(applicantName), type(registrationNumber), type(registerStatus), type(applicationDate), type(applicationNumber), type(inventionTitle), type(openDate), type(openNumber), type(publicationNumber), type(publishDate))
                
                # %s, %d, %s, %s, %d, %s, %s, %d, %d, %s

                # print((applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate))

                self.cursor.execute(sql, (applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate))

                print(sql, (applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate))
                self.connection.commit()
        self.connection.close()
        return
    
    def get_kipris_data_trademark(self):

        for i in range(1,10):

            url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch?applicantName=가방&application=true&registration=true&refused=true&expiration=true&withdrawal=true&publication=true&cancel=true&abandonment=true&trademark=true&serviceMark=true&businessEmblem=true&collectiveMark=true&geoOrgMark=true&trademarkServiceMark=true&certMark=true&geoCertMark=true&internationalMark=true&character=true&figure=true&compositionCharacter=true&figureComposition=true&fragrance=true&sound=true&color=true&colorMixed=true&dimension=true&hologram=true&invisible=true&motion=true&visual=true&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I=&pageNo=" + str(i)

            response = requests.get(url)

            print(response.text)
            
            tree = ET.fromstring(response.text)

            trademarks = tree.find("body").find("items")

            sql = "INSERT INTO trademark (agentName, publicationDate, publicationNumber, referenceNumber, registrationDate, registrationNumber, title, applicantName, applicationDate, classificationCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            for trademark in trademarks:
                agentName = trademark.find("agentName").text
                publicationDate = trademark.find("publicationDate").text
                publicationNumber = trademark.find("publicationNumber").text
                referenceNumber = trademark.find("appReferenceNumber").text
                registrationDate = trademark.find("registrationDate").text
                registrationNumber = trademark.find("registrationNumber").text
                title = trademark.find("title").text
                applicantName = trademark.find("applicantName").text
                applicationDate = trademark.find("applicationDate").text
                classificationCode = trademark.find("classificationCode").text
                print((agentName, publicationDate, publicationNumber, referenceNumber, registrationDate, registrationNumber, title, applicantName, applicationDate, classificationCode))

                self.cursor.execute(sql, (agentName, publicationDate, publicationNumber, referenceNumber, registrationDate, registrationNumber, title, applicantName, applicationDate, classificationCode))

                self.connection.commit()
        self.connection.close()
        return
    
# database = Database()

# database.get_kipris_data_trademark()

    