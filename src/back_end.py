import pymysql
import pymysql.cursors

import requests
import json

from xml.etree.ElementTree import parse, fromstring
import xml.etree.ElementTree as ET

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database='db_ajou',
            port=3305,
            cursorclass=pymysql.cursors.DictCursor
        )

        self.cursor = self.connection.cursor()

    def fetch_trademark(self, query):
        if query:
            sql = "SELECT * FROM trademark WHERE title LIKE %s"
            self.cursor.execute(sql, ('%' + query + '%',))
        else:
            sql = "SELECT * FROM trademark"
            self.cursor.execute(sql)

        self.connection.commit()
        data = self.cursor.fetchall()

        dict_list = []

        for i in data:
            dict_list.append({
                "agentName": i.get("agentName", ""),
                'publicationDate': str(i.get("publicationDate", "")),
                'publicationNumber': i.get("publicationNumber", 0),
                'referenceNumber': i.get("referenceNumber", ""),
                'registrationDate': str(i.get("registrationDate", "")),
                'registrationNumber': i.get("registrationNumber", 0),
                'title': i.get("title", ""),
                'applicantName': i.get("applicantName", ""),
                'applicationDate': str(i.get("applicationDate", "")),
                'classificationCode': i.get("classificationCode", "")
            })

        return dict_list

    def fetch_patent(self, query):
        if query:
            sql = "SELECT * FROM patent WHERE inventionTitle LIKE %s"
            self.cursor.execute(sql, ('%' + query + '%',))
        else:
            sql = "SELECT * FROM patent"
            self.cursor.execute(sql)

        self.connection.commit()
        data = self.cursor.fetchall()

        dict_list = []

        for i in data:
            dict_list.append({
                'applicantName': i.get('applicantName', ""),
                'registrationNumber': i.get('registrationNumber', 0),
                'registerStatus': i.get('registerStatus', ""),
                'applicationDate': str(i.get('applicationDate', "")),
                'applicationNumber': i.get("applicationNumber", 0),
                'inventionTitle': i.get("inventionTitle", ""),
                "openDate": str(i.get("openDate", "")),
                "openNumber": i.get("openNumber", 0),
                "publicationNumber": i.get("publicationNumber", 0),
                "publishDate": str(i.get("publishDate", ""))
            })

        return dict_list

    def update_trademark(self):
        return

    def update_patent(self):
        return

    def get_kipris_data_patent(self):
        for i in range(1, 50):
            url = f"http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch?astrtCont=발명&inventionTitle=센서&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I=&pageNo={i}"
            response = requests.get(url)
            tree = ET.fromstring(response.text)
            patents = tree.find("body").find("items")

            sql = """
            INSERT INTO patent 
            (applicantName, registrationNumber, registerStatus, applicationDate, applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            for patent in patents:
                applicantName = patent.find("applicantName").text or ""
                registrationNumber = patent.find("registerNumber").text or '0'
                registerStatus = patent.find("registerStatus").text or ""
                applicationDate = patent.find("applicationDate").text or ""
                applicationNumber = patent.find("applicationNumber").text or '0'
                inventionTitle = patent.find("inventionTitle").text or ""
                openDate = patent.find("openDate").text or ""
                openNumber = patent.find("openNumber").text or '0'
                publicationNumber = patent.find("publicationNumber").text or '0'
                publishDate = patent.find("publicationDate").text or ""

                self.cursor.execute(sql, (
                    applicantName, registrationNumber, registerStatus, applicationDate,
                    applicationNumber, inventionTitle, openDate, openNumber, publicationNumber, publishDate
                ))
                self.connection.commit()
        self.connection.close()
        return

    def get_kipris_data_trademark(self):
        for i in range(1, 10):
            url = f"http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch?applicantName=가방&application=true&registration=true&refused=true&expiration=true&withdrawal=true&publication=true&cancel=true&abandonment=true&trademark=true&serviceMark=true&businessEmblem=true&collectiveMark=true&geoOrgMark=true&trademarkServiceMark=true&certMark=true&geoCertMark=true&internationalMark=true&character=true&figure=true&compositionCharacter=true&figureComposition=true&fragrance=true&sound=true&color=true&colorMixed=true&dimension=true&hologram=true&invisible=true&motion=true&visual=true&ServiceKey=j0VWdt=ivH6agdzPYqVaLjk4QiMFeNITpFlFxsP0a0I=&pageNo={i}"
            response = requests.get(url)
            tree = ET.fromstring(response.text)
            trademarks = tree.find("body").find("items")

            sql = """
            INSERT INTO trademark 
            (agentName, publicationDate, publicationNumber, referenceNumber, registrationDate, registrationNumber, title, applicantName, applicationDate, classificationCode) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            for trademark in trademarks:
                agentName = trademark.find("agentName").text or ""
                publicationDate = trademark.find("publicationDate").text or ""
                publicationNumber = trademark.find("publicationNumber").text or '0'
                referenceNumber = trademark.find("appReferenceNumber").text or ""
                registrationDate = trademark.find("registrationDate").text or ""
                registrationNumber = trademark.find("registrationNumber").text or '0'
                title = trademark.find("title").text or ""
                applicantName = trademark.find("applicantName").text or ""
                applicationDate = trademark.find("applicationDate").text or ""
                classificationCode = trademark.find("classificationCode").text or ""

                self.cursor.execute(sql, (
                    agentName, publicationDate, publicationNumber, referenceNumber, registrationDate,
                    registrationNumber, title, applicantName, applicationDate, classificationCode
                ))
                self.connection.commit()
        self.connection.close()
        return

database = Database()