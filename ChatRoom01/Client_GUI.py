import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit,QApplication,QWidget,QColorDialog
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)


class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.link_to_server('127.0.0.1', 5550) # 連線~~
        self.setupUi()
        self.show()
        th1 = threading.Thread(target=self.sendThreadFunc)
        th2 = threading.Thread(target=self.recvThreadFunc)
        threads = [th1, th2]
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join

    # 連線~~
    def link_to_server(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

    def sendThreadFunc(self):
        while True:
            try:
                myword = input()
                self.sock.send(myword.encode())
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                t = otherword.decode()
                self.showchat.append(t)
                #print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')


    def hello(self):
        self.line_hello.setText("hello")

    def cancel(self):
        self.line_hello.setText("")

    def setupUi(self):
        self.resize(500,400)
        self.setWindowTitle("Chat Application")

        #col=QColorDialog.getColor()
        #self.setAutoFillBackground(true)

        self.label = QLabel()
        self.label.setText("Nickname: ")        #show name lable

        self.labe2 = QLabel()
        self.labe2.setText("Change Password: ") #show Password lable

        self.button_Login = QPushButton()
        self.button_Login.setText("Add")

        self.button_cancel = QPushButton()
        self.button_cancel.setText("send")

        self.button_cance_updatePassword = QPushButton()
        self.button_cance_updatePassword.setText("update Password")       #update Password Button

        #self.button_cancel = QPushButton("Send") # b3不可按
        self.button_cancel.setEnabled(False)
        self.button_Login.setEnabled(True)

        self.name = QLineEdit()
        self.Password = QLineEdit()
        self.Change_Password = QLineEdit()

        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(self.label, 1, 1)        #name_lable
        grid.addWidget(self.name, 1, 2)         #name input
        grid.addWidget(self.Password, 1, 3)     #password_input
        grid.addWidget(self.button_Login, 1,4)  #login_button


        grid.addWidget(self.labe2, 2, 1)    #password_lable
        grid.addWidget(self.Change_Password, 2, 2)     #Change_Password_TextEdit
        grid.addWidget(self.button_cance_updatePassword, 2,3)  #login_button

        grid.addWidget(self.showchat, 4, 0, 6, 5)   #showchat
        grid.addWidget(self.chat, 9, 0, 5, 5)
        grid.addWidget(self.button_cancel, 10, 0, 5, 5)

        self.setLayout(grid)
        self.button_Login.clicked.connect(self.login)
        self.button_cancel.clicked.connect(self.showText)

    def login(self):
        # 取得 輸入的 nickname
        text=self.name.text()
        #　設定button 可按與不可按
        self.name.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_Login.setEnabled(False)
        #　將值傳給server
        self.sock.send(text.encode())

    def showText(self):
        #　將值傳給server
        self.sock.send(self.chat.text().encode())
        #  同時將自己輸入的值印在chat上
        self.showchat.append("\t\t" + self.chat.text() + " : You")




'''class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

    def sendThreadFunc(self):
        while True:
            try:
                myword = input()
                self.sock.send(myword.encode())
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')




    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')'''



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    sys.exit(app.exec_())
