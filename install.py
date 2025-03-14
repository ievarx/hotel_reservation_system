import os
try:
    import mysql.connector
except ImportError:
    print("Installing mysql-connector-python...")
    os.system('pip install mysql-connector-python')

try:
    import kivy
except ImportError:
    print("Installing Kivy")
    os.system('pip install kivy')


os.system('python app.py')
