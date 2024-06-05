import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QComboBox, QMessageBox
)
from back_end import Database  # 백엔드 모듈 임포트

class IntellectualPropertySearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('지식 재산권 검색 서비스')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        title = QLabel('지식 재산권 검색 서비스')
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)
        
        admin_button = QPushButton('관리자', self)
        admin_button.setStyleSheet("font-size: 18px; padding: 10px;")
        admin_button.clicked.connect(self.open_admin_page)
        header_layout.addWidget(admin_button)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
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
        
        view_all_button = QPushButton('전체 확인', self)
        view_all_button.setStyleSheet("font-size: 18px; padding: 10px;")
        view_all_button.clicked.connect(self.view_all)
        layout.addWidget(view_all_button)
        
        self.setLayout(layout)
    
    def open_admin_page(self):
        self.admin_window = AdminPage()
        self.admin_window.setFixedSize(400, 300)
        self.admin_window.show()

    def fetch_data_from_backend(self, query, patent_checked, trademark_checked):
        db = Database()
        patent_results = []
        trademark_results = []
        
        if patent_checked:
            patent_results = db.fetch_patent(query)
        
        if trademark_checked:
            trademark_results = db.fetch_trademark(query)
        
        return patent_results, trademark_results
    
    def search(self):
        query = self.search_input.text()
        patent_checked = self.patent_checkbox.isChecked()
        trademark_checked = self.trademark_checkbox.isChecked()
        
        patent_results, trademark_results = self.fetch_data_from_backend(query, patent_checked, trademark_checked)
        
        self.result_window = ResultWindow(query, patent_results, trademark_results)
        self.result_window.setFixedSize(1000, 800)
        self.result_window.show()
    
    def view_all(self):
        patent_checked = self.patent_checkbox.isChecked()
        trademark_checked = self.trademark_checkbox.isChecked()
        
        patent_results, trademark_results = self.fetch_data_from_backend("", patent_checked, trademark_checked)
        
        self.result_window = ResultWindow("전체 확인", patent_results, trademark_results)
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
            patent_table.setColumnCount(10)
            patent_table.setHorizontalHeaderLabels([
                '출원인', '등록번호', '등록상태', '출원일자', '출원번호', '발명의 명칭', '공개일자', '공개번호', '공표번호', '공표일자'
            ])
            patent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            patent_table.setRowCount(len(self.patent_results))
            
            for row, result in enumerate(self.patent_results):
                patent_table.setItem(row, 0, QTableWidgetItem(result["applicantName"]))
                patent_table.setItem(row, 1, QTableWidgetItem(str(result["registrationNumber"])))
                patent_table.setItem(row, 2, QTableWidgetItem(result["registerStatus"]))
                patent_table.setItem(row, 3, QTableWidgetItem(str(result["applicationDate"])))
                patent_table.setItem(row, 4, QTableWidgetItem(str(result["applicationNumber"])))
                patent_table.setItem(row, 5, QTableWidgetItem(result["inventionTitle"]))
                patent_table.setItem(row, 6, QTableWidgetItem(str(result["openDate"])))
                patent_table.setItem(row, 7, QTableWidgetItem(str(result["openNumber"])))
                patent_table.setItem(row, 8, QTableWidgetItem(str(result["publicationNumber"])))
                patent_table.setItem(row, 9, QTableWidgetItem(str(result["publishDate"])))
            
            scroll_layout.addWidget(patent_table)
        
        if self.trademark_results:
            trademark_title = QLabel("---------상표권---------")
            trademark_title.setStyleSheet("font-size: 20px; font-weight: bold;")
            scroll_layout.addWidget(trademark_title)
            
            trademark_table = QTableWidget(self)
            trademark_table.setColumnCount(10)
            trademark_table.setHorizontalHeaderLabels([
                '대리인', '공고일자', '공고번호', '참조번호', '등록일자', '등록번호', '상표명', '출원인', '출원일자', '상품분류'
            ])
            trademark_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            trademark_table.setRowCount(len(self.trademark_results))
            
            for row, result in enumerate(self.trademark_results):
                trademark_table.setItem(row, 0, QTableWidgetItem(result.get("agentName", "")))
                trademark_table.setItem(row, 1, QTableWidgetItem(str(result["publicationDate"])))
                trademark_table.setItem(row, 2, QTableWidgetItem(str(result["publicationNumber"])))
                trademark_table.setItem(row, 3, QTableWidgetItem(result.get("referenceNumber", "")))
                trademark_table.setItem(row, 4, QTableWidgetItem(str(result["registrationDate"])))
                trademark_table.setItem(row, 5, QTableWidgetItem(str(result["registrationNumber"])))
                trademark_table.setItem(row, 6, QTableWidgetItem(result["title"]))
                trademark_table.setItem(row, 7, QTableWidgetItem(result["applicantName"]))
                trademark_table.setItem(row, 8, QTableWidgetItem(str(result["applicationDate"])))
                trademark_table.setItem(row, 9, QTableWidgetItem(result["classificationCode"]))
            
            scroll_layout.addWidget(trademark_table)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

class AdminPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('관리자 페이지')
        
        layout = QVBoxLayout()
        
        # Registration number input
        self.reg_num_input = QLineEdit(self)
        self.reg_num_input.setPlaceholderText('Registration Number')
        layout.addWidget(self.reg_num_input)
        
        # Patent or Trademark selection
        self.type_selector = QComboBox(self)
        self.type_selector.addItem('특허권')
        self.type_selector.addItem('상표권')
        self.type_selector.currentIndexChanged.connect(self.update_attributes)
        layout.addWidget(self.type_selector)
        
        # Attribute selection
        self.attribute_selector = QComboBox(self)
        layout.addWidget(self.attribute_selector)
        
        # Value input
        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText('Value')
        layout.addWidget(self.value_input)
        
        # Update button
        update_button = QPushButton('Update', self)
        update_button.clicked.connect(self.update_record)
        layout.addWidget(update_button)
        
        self.setLayout(layout)
        
        self.update_attributes()  # Initialize attributes based on the default selection

    def update_attributes(self):
        self.attribute_selector.clear()
        if self.type_selector.currentText() == '특허권':
            attributes = ['applicantName', 'registrationNumber', 'registerStatus', 'applicationDate', 'applicationNumber', 'inventionTitle', 'openDate', 'openNumber', 'publicationNumber', 'publishDate']
        else:
            attributes = ['agentName', 'publicationDate', 'publicationNumber', 'referenceNumber', 'registrationDate', 'registrationNumber', 'title', 'applicantName', 'applicationDate', 'classificationCode']
        self.attribute_selector.addItems(attributes)

    def update_record(self):
        db = Database()
        reg_num = self.reg_num_input.text()
        record_type = self.type_selector.currentText()
        attribute = self.attribute_selector.currentText()
        value = self.value_input.text()
        
        if record_type == '특허권':
            result = db.update_patent(reg_num, attribute, value)
        else:
            result = db.update_trademark(reg_num, attribute, value)
        
        if result == 0:
            self.show_error_message("존재하지 않는 등록번호입니다")
        else:
            self.show_info_message("성공적으로 업데이트되었습니다")

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
        
    def show_info_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Info")
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    ex = IntellectualPropertySearch()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()