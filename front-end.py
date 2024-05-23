import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox

class IntellectualPropertySearch(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('지식 재산권 검색 서비스')
        
        layout = QVBoxLayout()
        
        title = QLabel('지식 재산권 검색 서비스')
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText('원하시는 상품, 특허를 입력하세요')
        layout.addWidget(self.search_input)
        
        self.patent_checkbox = QCheckBox('특허권', self)
        layout.addWidget(self.patent_checkbox)
        
        self.trademark_checkbox = QCheckBox('상표권', self)
        layout.addWidget(self.trademark_checkbox)
        
        search_button = QPushButton('검색', self)
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)
        
        self.setLayout(layout)
    
    def search(self):
        query = self.search_input.text()
        patent_checked = self.patent_checkbox.isChecked()
        trademark_checked = self.trademark_checkbox.isChecked()
        
        results = f'검색어: {query}\n'
        if patent_checked:
            results += '특허권 검색\n'
        if trademark_checked:
            results += '상표권 검색\n'
        
        QMessageBox.information(self, '검색 결과', results)

def main():
    app = QApplication(sys.argv)
    ex = IntellectualPropertySearch()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()