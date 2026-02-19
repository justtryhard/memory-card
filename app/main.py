import os
import sys

# Настройка кодировки для консоли
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

# Путь к плагинам PyQt5
venv_path = sys.prefix
plugins_path = os.path.join(venv_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugins_path


from logic.logic import QuestionDatabase
from models.interface import QuizWindow  
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    database = QuestionDatabase()
    window = QuizWindow(database)
    window.show()
    sys.exit(app.exec_())
