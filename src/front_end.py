import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)

class IntellectualPropertySearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('지식 재산권 검색 서비스')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        title = QLabel('지식 재산권 검색 서비스')
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('원하시는 상품, 특허를 입력하세요')
        self.search_input.setStyleSheet("font-size: 18px; padding: 10px;")
        layout.addWidget(self.search_input)
        
        self.patent_checkbox = QCheckBox('특허권', self)
        self.patent_checkbox.setStyleSheet("font-size: 18px; padding: 5px;")
        layout.addWidget(self.patent_checkbox)
        
        self.trademark_checkbox = QCheckBox('상표권', self)
        self.trademark_checkbox.setStyleSheet("font-size: 18px; padding: 5px;")
        layout.addWidget(self.trademark_checkbox)
        
        search_button = QPushButton('검색', self)
        search_button.setStyleSheet("font-size: 18px; padding: 10px;")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)
        
        self.setLayout(layout)
    
    def fetch_data_from_api(self, query, patent_checked, trademark_checked):
        # 여기에 API 데이터 입력
        patent_results = []
        trademark_results = []
        
        if patent_checked:
            patent_results = [
                {"application_number": "2019000001", "application_date": "2020.01.01", "registration_number": "1000001", 
                 "registration_date": "2021.01.01", "publication_number": "2000001", "publication_date": "2020.07.01", 
                 "agent": "홍길동", "inventor": "이순신"},
                # Add more dynamically fetched patent results here
            ]
        
        if trademark_checked:
            trademark_results = [
                {"product_classification": "09", "applicant": "포스코", "application_number": "2019000001", "application_date": "2020.01.01", 
                 "registration_number": "1000001", "registration_date": "2021.01.01", "application_notice_number": "2000001", 
                 "application_notice_date": "2020.07.01", "shape_code": "B01", "agent": "홍길동"},
                # Add more dynamically fetched trademark results here
            ]
        
        return patent_results, trademark_results
    
    def search(self):
        query = self.search_input.text()
        patent_checked = self.patent_checkbox.isChecked() # 체크박스 체크 bool
        trademark_checked = self.trademark_checkbox.isChecked()
        
        patent_results, trademark_results = self.fetch_data_from_api(query, patent_checked, trademark_checked)
        
        self.result_window = ResultWindow(query, patent_results, trademark_results)
        self.result_window.setFixedSize(1000, 800)
        self.result_window.show()

class ResultWindow(QWidget):
    def __init__(self, query, patent_results, trademark_results):
        super().__init__()
        
        self.query = query
        self.patent_results = patent_results
        self.trademark_results = trademark_results
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('검색 결과')
        
        layout = QVBoxLayout()
        
        title = QLabel(f"'{self.query}' 검색 결과")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget(scroll_area)
        scroll_layout = QVBoxLayout(scroll_content)
        
        if self.patent_results:
            patent_title = QLabel("---------특허권---------")
            patent_title.setStyleSheet("font-size: 20px; font-weight: bold;")
            scroll_layout.addWidget(patent_title)
            
            patent_table = QTableWidget(self)
            patent_table.setColumnCount(8)
            patent_table.setHorizontalHeaderLabels([
                '출원번호', '출원일자', '등록번호', '등록일자', '공개번호', '공개일자', '대리인', '발명자'
            ])
            patent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            patent_table.setRowCount(len(self.patent_results))
            
            for row, result in enumerate(self.patent_results):
                patent_table.setItem(row, 0, QTableWidgetItem(result["application_number"]))
                patent_table.setItem(row, 1, QTableWidgetItem(result["application_date"]))
                patent_table.setItem(row, 2, QTableWidgetItem(result["registration_number"]))
                patent_table.setItem(row, 3, QTableWidgetItem(result["registration_date"]))
                patent_table.setItem(row, 4, QTableWidgetItem(result["publication_number"]))
                patent_table.setItem(row, 5, QTableWidgetItem(result["publication_date"]))
                patent_table.setItem(row, 6, QTableWidgetItem(result["agent"]))
                patent_table.setItem(row, 7, QTableWidgetItem(result["inventor"]))
            
            scroll_layout.addWidget(patent_table)
        
        if self.trademark_results:
            trademark_title = QLabel("---------상표권---------")
            trademark_title.setStyleSheet("font-size: 20px; font-weight: bold;")
            scroll_layout.addWidget(trademark_title)
            
            trademark_table = QTableWidget(self)
            trademark_table.setColumnCount(10)
            trademark_table.setHorizontalHeaderLabels([
                '상품분류', '출원인', '출원번호', '출원일자', '등록번호', '등록일자', '출원공고번호', '출원공고일자', '도형코드', '대리인'
            ])
            trademark_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            trademark_table.setRowCount(len(self.trademark_results))
            
            for row, result in enumerate(self.trademark_results):
                trademark_table.setItem(row, 0, QTableWidgetItem(result["product_classification"]))
                trademark_table.setItem(row, 1, QTableWidgetItem(result["applicant"]))
                trademark_table.setItem(row, 2, QTableWidgetItem(result["application_number"]))
                trademark_table.setItem(row, 3, QTableWidgetItem(result["application_date"]))
                trademark_table.setItem(row, 4, QTableWidgetItem(result["registration_number"]))
                trademark_table.setItem(row, 5, QTableWidgetItem(result["registration_date"]))
                trademark_table.setItem(row, 6, QTableWidgetItem(result["application_notice_number"]))
                trademark_table.setItem(row, 7, QTableWidgetItem(result["application_notice_date"]))
                trademark_table.setItem(row, 8, QTableWidgetItem(result["shape_code"]))
                trademark_table.setItem(row, 9, QTableWidgetItem(result["agent"]))
            
            scroll_layout.addWidget(trademark_table)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    ex = IntellectualPropertySearch()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()