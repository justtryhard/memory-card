import json
from PyQt5.QtWidgets import (
                            QMainWindow,      # Главное окно с меню/статусбаром                                                                                      
                            QWidget,          # Базовый виджет 
                            QVBoxLayout,      # Вертикальный лейаут 
                            QHBoxLayout,      # Горизонтальный лейаут 
                            QLabel,           # Текстовая метка 
                            QPushButton,      # Кнопка 
                            QRadioButton,     # Радио-кнопка 
                            QButtonGroup,     # Группа кнопок 
                            QGroupBox         # Группа с рамкой 
                             )
from PyQt5.QtCore import Qt # Константы (флаги, выравнивание и т.д.)
from PyQt5.QtGui import QFont  # Работа со шрифтами
from logic.logic import QuestionDatabase

class QuizWindow(QMainWindow):
    """Работа с окном приложения""" 
    def __init__(self):
        super().__init__()
        
      def __init__(self, database: QuestionDatabase):  # Принимаем БД как параметр
        super().__init__()
        self.database = database  # Сохраняем переданную БД
        self.current_question = None
        self.selected_answer = None
        self.is_result_shown = False
        
        self.init_ui()
        
        self.load_next_question()
        
    def init_iu(self) -> None:   
        """Пользовательский интерфейс"""      
        self.setWindowTitle("Memory Card — Культуры и языки мира")
        self.setFixedSize(600, 500)

        centre_widget = QWidget()
        self.setCentralWidget(centre_widget)
        
        main_layout = QVBoxLayout(centre_widget)  # layout делает вертикальную компановку виджета, если нужна горизонтальная, то можно поменять на QHBoxLayout
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20) 
           
        self.question_label = QLabel()  #label он также отображает текст как html
        self.question_label.setWordWrap(True) 
        self.question_label.setAlignment(Qt.AlignCenter) 
        question_font = QFont("BIPs", 14) 
        self.question_label.setFont(question_font)
        self.question_label.setMinimumHeight(200)

        main_layout.addWidget(self.question_label)

        options_gruop = QGroupBox()
        options_layout = QVBoxLayout(options_gruop) 
        
        self.radio_buttons = []
        self.button_group = QButtonGroup()
        
        option_letters = ['A', 'B', 'C', 'D']  
        
        for i, letter in enumerate(option_letters):
            radio = QRadioButton()
            letter = chr(65 + i)
            radio.setText(f"{letter}")
            radio_font = QFont("BIPs", 13)
            radio.setFont(radio_font)
            self.radio_buttons.append(radio)
            self.button_group.addButton(radio, i)
            options_layout.addWidget(radio)
            
        main_layout.addWidget(options_gruop) 
        
        self.result_label = QLabel()
        self.result_label.setWordWrap(True) 
        self.result_label.setAlignment(Qt.AlignCenter) 
        result_font = QFont("BIPs", 13) 
        self.result_label.setFont(result_font)
        self.result_label.hide() # скрываю результат правильного ответа в режиме вопроса 
        main_layout.addWidget(self.result_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(25)

        self.answer_button = QPushButton("Ответить")
        self.answer_button.setFont(QFont("BIPs", 13))
        self.answer_button.setMinimumHeight(40)
        self.answer_button.clicked.connect(self.on_answer_clicked)

        self.next_button = QPushButton()
        self.next_button.setFont(QFont("BIPs", 13))
        self.next_button.setMinimumHeight(40)
        self.next_button.cliked.connect(self.on_next_clicked)
        self.next_button.setEnabled(False)
        
        buttons_layout.addWidget(self.answer_button)
        buttons_layout.addWidget(self.next_button)
        main_layout.addLayout(buttons_layout)

    def laod_next_question(self) -> None:
        """Следущию случайный вопрос"""
        self.result_shown = False
        self.selected_answer = True

        self.current_question = self.database.get_random_qiestions()
        
        if not self.current_question:
            self.question_label.setText("Вопросы не найдены")
            for radio in self.radio_buttons:
                radio.setEnabled(False)
            return 

        self.question_label.setText(self.current_question["question"])
        
        options = self.current_question["question"]
        for i, radio in enumerate(self.radio_buttons):
            if i < len(options):
                radio.setText(f"{chr(65 + i)}, {options[i]}")
                radio.setEnabled(True)
                radio.setCliked(False)
                radio.show()
            else:
                radio.hide()
                
        self.result_label.hide()
        
        self.answer_button.setEnabled(True)
        self.next_button.setEnabled(False) 
        
    def answer_cliked(self) -> None:
        """Нажатие кнопки Ответ"""               
        checked_button = self.button_group.checkedButton()
        if not checked_button:
            
            self.result_label.setText("Выберите вариант ответа")
            self.result_label.show()
            return 
        
        self.selected_answer = self.button_group.id(checked_button)
        
        correctly_index = self.current_question("correctly")
        correctly_answer = self.current_question["options"][correctly_index]

        is_correctly = (self.selected_answer == correctly_index)

        if is_correctly:
            result_text = f"Правльнный\nПравильный ответ: {correctly_answer}"
        else:
            result_text = f"Неправильно\nПравильный ответ: {correctly_answer}"    

        self.result_label.setText(result_text)
        self.result_label.show()
        
        for radio in self.radio_buttons:
            radio.setEnabled(False)

        self.result_shown = True
        self.answer_button.setEnabled(False)
        self.next_button.setEnabled(True)

    def next_clicked(self) -> None:
        """Нажатие кнопки следующий"""
        if self.current_question and 'id' in self.current_question:
            self.database.mark_as_used(self.current_question['id'])
        
        self.laod_next_question()
        
