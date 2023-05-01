import sys
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
import mysql.connector
import random

# import base64
# from PIL import ImageQt
# 소켓 정의

HEADER = 64 # 기본 메세지 크기 (바이트)
FORMAT = "utf-8" # 인코딩 형식

SERVER = socket.gethostbyname(socket.gethostname()) # IP 주소 (로컬)
PORT = 9058 # 통신용 포트
ADDR = (SERVER, PORT)

# 시스템 통신용 번호
NEW_MESSAGE = '0'
NAME_LIST = '1'
CLEAR_LIST = '2'
DISCONNECT_MESSAGE = '3'
SAVE_LIST = '4'
MEMBER_INVITE = '5'
INQURE_MESSAGE = '6'

form_class = uic.loadUiType("chatroomGOING.ui")[0]


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    
    return binaryData, filename

def finderoom():
    print("Find Chatting Room ... ")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT profile, host, roomname, roompeople FROM cat_talk_chat_room")
        result = cursor.fetchall()
        return result
    
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def createroom(profile, id, roomname):
    print("Create Chatting Room ...")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO cat_talk_chat_room (profile, host, roomname) VALUES (%s,%s,%s)"""

        insert_blob_tuple = (profile, id, roomname)

        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Profile and ID and roomname inserted successfully as a BLOB into cat_talk_chat_room table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def chattry(id):
    print("chatting try ...")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT profile, host, roomname FROM cat_talk_chat_room where host = '"+str(id)+"'")
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as error:
        print("Failed chatting {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("User chatTry Finish.  MySQL connection is closed")


def checkLogout(id):
    print("Checking User Logout.....")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        result = cursor.execute("UPDATE cat_talk SET online = '오프라인' where name = '"+str(id)+"' ")
        connection.commit()
        print("User logout successfully update cat_talk table", result)
    except mysql.connector.Error as error:
        print("Failed Logout {}".format(error))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("User Logout Finish.  MySQL connection is closed")

def checkUser():
    print("Checking User ....")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT profile, name, online from cat_talk")
        result = cursor.fetchall()
        return result
    
    except mysql.connector.Error as error:
        print("Failed select {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("User Check Finish.  MySQL connection is closed")

def checkID(id):
    print("Checking ID ....")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT * from cat_talk where name = '"+str(id)+"'")
        result = cursor.fetchall()
        if result:
            return result
        else:
            pass
    except mysql.connector.Error as error:
        print("Failed select {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Id Check Finish.  MySQL connection is closed")

def insertBLOB(name, photo, ip, port, act):
    print("Inserting BLOB into chating_member table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO cat_talk
                                    (profile, name, ip, port, online) VALUES (%s,%s,%s,%s,%s)"""
        # empPicture = convertToBinaryData(photo)

        insert_blob_tuple = (photo, name, ip, port, act)

        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Profile and User_information inserted successfully as a BLOB into cat_talk table", result)
                
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def loginDB(loginid):
    print("FIND LOGIN DB....")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT profile from cat_talk where name = '"+str(loginid)+"'")
        result = cursor.fetchone()
        if result:
            return result
        else:
            pass

    except mysql.connector.Error as error:
        print("Failed Find data MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def historyInquire(data):
    print("Message Inquire about data .... ")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, message, time from cat_talk_chatting where time = '"+str(data)+"' ")
        result = cursor.fetchall()
        if result:
            return result
        else:
            pass

    except mysql.connector.Error as error:
        print("Failed Find message data MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def history():
    print("Message History inquire....")
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='chat',
                                            user='root',
                                            password='0000')
        cursor = connection.cursor()
        cursor.execute("SELECT distinct user_id, time from cat_talk_chatting")
        result = cursor.fetchall()
        if result:
            return result
        else:
            pass

    except mysql.connector.Error as error:
        print("Failed Find message data MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

class MySignal(QtCore.QObject):

    listUser = QtCore.pyqtSignal(str)
    chatLabel = QtCore.pyqtSignal(str)

# class Button(QtCore.QObject):

#     button = QtCore.pyqtSignal(int)

class LogWindow(QMainWindow, form_class):

    def __init__(self):

        super(QMainWindow, self).__init__()
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.statusBar().setFixedHeight(0)
        self.actionLogout.triggered.connect(self.logout)

        self.profileList = []

        for i in range(1, 13):
            self.profileList.append(convertToBinaryData(f"C:\Language\Python\Python\Client\one{i}.png"))

        self.name = False
        self.addr = False
        self.prt = False
        self.act = ""

        # self.test_btn.clicked.connect(self.gogo)

        self.user_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.chat_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.room_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.message_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.room_tableWidget.cellDoubleClicked.connect(self.chatgo)
        self.history_table.cellDoubleClicked.connect(self.history_show)
        # self.chat_tableWidget.cellDoubleClicked.connect(self.friendinvite)

        self.msg_lienEdit.returnPressed.connect(self.newmsg)

        self.make_profile_btn.clicked.connect(self.makeprofile)
        self.chat_exit_btn.clicked.connect(self.waitroom)
        self.profile_check_btn.clicked.connect(self.check)
        self.entrance_btn.clicked.connect(self.entrance)
        self.create_room_btn.clicked.connect(self.makeroom)
        self.find_room_btn.clicked.connect(self.findroom)
        self.msg_history_btn.clicked.connect(self.viewhistory)
        self.mainpage_btn.clicked.connect(self.mainpage)
    
    def gogo(self):
        print("테스트중입니다....")
        self.cnt = 0
        self.cnt += 1
        print(self.cnt)
        self.addr = SERVER
        self.prt = PORT
        self.Idchat(self.addr, self.prt, self.cnt)

    def mainpage(self):
        self.tabWidget.setCurrentIndex(1)

    def viewhistory(self):

        self.tabWidget.setCurrentIndex(3)

        history_list = []
        message_inquire = history()

        for i in message_inquire:
            history_list.append(i)

        self.history_table.setColumnWidth(0, round(self.width() * 2 / 5))
        self.history_table.setColumnWidth(1, round(self.width() * 3 / 5))

        self.message_table.setColumnWidth(0, round(self.width() * 1 / 10))
        self.message_table.setColumnWidth(1, round(self.width() * 3 / 10))
        self.message_table.setColumnWidth(2, round(self.width() * 6 / 10))

        self.history_table.setRowCount(len(message_inquire))  # 테이블의 행 갯수를 rows의 길이로 정함
        self.history_table.setColumnCount(len(message_inquire[0]))

        for i in range(len(history_list)):
            for j in range(len(history_list[i])):
                self.history_table.setItem(i, j, QTableWidgetItem(str(history_list[i][j])))

    def history_show(self, row, col):
        reply = QMessageBox.question(self,'메세지','메세지 조회를 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            data = self.history_table.item(row, col)
            # print("셀 클릭 셀 값 : ", data.text())
            message_data = historyInquire(data.text())
            message_list = []
            if message_data:
                for i in message_data:
                    message_list.append(i)
            
                self.message_table.setRowCount(len(message_data))
                self.message_table.setColumnCount(len(message_data[0]))

                for i in range(len(message_list)):
                    for j in range(len(message_list[i])):
                        self.message_table.setItem(i, j, QTableWidgetItem(str(message_list[i][j])))
            else:
                QMessageBox.information(self, "메세지", "메세지 기록이 없습니다.")          

        else:
            pass

    def makeroom(self):
        self.id = self.id_label.text()
        self.roomname = self.chat_room_name.text()
        if len(self.roomname) == 0:
            QMessageBox.information(self, "메세지", "채팅방 이름을 작성 해 주세요.")
        else:
            reply = QMessageBox.question(self,'메세지','채팅방을 만드시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.profile = loginDB(self.id_label.text())
                # print(self.profile)
                # print("테스트 중입니다...\n")
                # print(self.profile[0])
                createroom(self.profile[0], self.id, self.roomname)
                QMessageBox.information(self, "메세지", "채팅방이 개설 되었습니다.")

            else:
                pass

    def findroom(self):
        while self.room_tableWidget.rowCount() > 0:
            self.room_tableWidget.removeRow(0)

        for row_number, row_data in enumerate(finderoom()):
                    self.room_tableWidget.insertRow(row_number)
                    for column_number, column_data in enumerate(row_data):
                        item = str(column_data)

                        if (column_number == 0):
                            item = self.profileImage(column_data)
                            print(item)
                            self.room_tableWidget.setCellWidget(row_number,column_number, item)
                            self.room_tableWidget.setRowHeight(row_number, 150)
                        else:
                            self.room_tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

    def entrance(self):

        reply = QMessageBox.question(self,'메세지','접속 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.id_label.setText(self.user_name.text())
            self.a = loginDB(self.user_name.text())
            if self.a:
                self.menubar.setVisible(True)
                self.tabWidget.setCurrentIndex(1)
                for row in self.a:
                # 튜플을 리스트로 변환하기. 각 행마다 요소에 접근하여 변환
                    row_to_list = [pic for pic in row]
                    pixmap = QPixmap()
                    pixmap.loadFromData(bytearray(row_to_list))
                    self.profile_id_label.setPixmap(pixmap)
                    for row_number, row_data in enumerate(checkUser()):
                        self.user_tableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            item = str(column_data)

                            if (column_number == 0):

                                item = self.profileImage(column_data)
                                self.user_tableWidget.setCellWidget(row_number,column_number, item)
                                self.user_tableWidget.setRowHeight(row_number, 150)

                            else:
                                self.user_tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))
                return self.a
            else:
                QMessageBox.information(self, "메세지", "ID가 존재하지 않습니다.")
        else:
            pass

    def check(self):

        self.name = self.user_name.text()
        self.addr = str(self.user_ip.text())
        self.prt = self.user_port.text()

        if len(self.name) ==0:
            self.name = "User"
        if len(self.addr) ==0:
            self.addr = SERVER
        if len(self.prt) ==0:
            self.prt = PORT
        a = loginDB(self.name)
        if a:
            # print(a)
            # print(type(a))
            for row in a:
                # 튜플을 리스트로 변환하기. 각 행마다 요소에 접근하여 변환
                row_to_list = [pic for pic in row]
                # print(row_to_list)
                pixmap = QPixmap()
                pixmap.loadFromData(bytearray(row_to_list))
                self.profile_choice_label.setPixmap(pixmap)
                QMessageBox.information(self, "메세지", "ID 찾기 완료되었습니다.")
        else:
            QMessageBox.information(self, "메세지", "ID가 존재하지 않습니다.")
        
    def chatgo(self):
        # self.data = self.user_tableWidget.item(row, col)
        # print("친구 이름 : ", self.data.text())

        a = self.room_tableWidget.currentRow() # 클릭한 셀 row(행)값 얻기
        b = self.room_tableWidget.currentColumn() # 클릭한 셀 column 값 얻기
        c = self.room_tableWidget.item(a,b).text() # 클릭한 셀 값 얻기
        d = self.room_tableWidget.columnCount() # 해당 테이블위젯 칼럼 개수
        f = self.room_tableWidget.horizontalHeaderItem(b).text() # 클릭한 셀 칼럼 값 얻기

        self.chatfriend = []
        for i in range(1,d-2):
            self.chatfriend.append(self.room_tableWidget.item(a, i).text())
        print(self.chatfriend)
        print(self.chatfriend[0])
        reply = QMessageBox.question(self,'메세지','채팅방에 입장하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
                self.chatting()
                if self.chat_tableWidget.rowCount() == False:
                    for row_number, row_data in enumerate(chattry(self.chatfriend[0])):
                        self.chat_tableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            item = str(column_data)

                            if (column_number == 0):
                                item = self.profileImage(column_data)
                                print(item)
                                self.chat_tableWidget.setCellWidget(row_number,column_number, item)
                                self.chat_tableWidget.setRowHeight(row_number, 150)

                            else:
                                self.chat_tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))
                else:
                    pass     
        else:
            pass

    def logout(self):
        reply = QMessageBox.question(self,'메세지','로그아웃 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            checkLogout(self.name)
            self.tabWidget.setCurrentIndex(0)
            self.menubar.setVisible(False)
        else:
            pass

    def picture(self):
        a = random.choice(self.profileList)
        # print(self.profileList[0][0])
        print(a[1])
        self.profile_choice_label.setPixmap(QPixmap(a[1]))

        return a

    def waitroom(self):

        reply = QMessageBox.question(self,'메세지','채팅방에서 나가시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self,'Quit', '채팅방에서 나갑니다.')
            self.tabWidget.setCurrentIndex(1)

            self.client.disconnect()

        else:
            pass

    def makeprofile(self):
            # 입력 받기 
            self.name = self.user_name.text()
            self.addr = str(self.user_ip.text())
            self.prt = self.user_port.text()
            self.pic = self.picture()

            # 입력 값 중 하나가 비어 있으면 기본값이 전송된다.
            if len(self.name) ==0:
                self.name = "User"
            if len(self.addr) ==0:
                self.addr = SERVER
            if len(self.prt) ==0:
                self.prt = PORT

            reply = QMessageBox.question(self,'메세지','현재 프로필로 아이디를 생성하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if checkID(self.name):
                    QMessageBox.information(self, "Login", "이미 등록되어 있는 유저 이름입니다. 다른 이름을 등록해 주세요.")
                else:
                    self.act = "온라인"
                    print("테스트중입니다....\n")
                    print("이거진짜테스트임>...\n")
                    print(self.pic[0])
                    insertBLOB(self.name, self.pic[0], self.addr, self.prt, self.act)
                    QMessageBox.information(self,'생성', 'ID가 생성되었습니다.')
                pass

    def chatting(self):
        self.tabWidget.setCurrentIndex(2)
        self.Chat(self.name, self.addr, self.prt)

    def profileImage(self, image):
        self.imageLabel = QtWidgets.QLabel(self.centralWidget())
        self.imageLabel.setText("")
        self.imageLabel.setScaledContents(True)
        # imageLabel.setContentsMargins
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'png')
        self.imageLabel.setPixmap(pixmap)
        return self.imageLabel

    # 키보드 입력 감지
    def keyPressEvent(self, event):
        # 키보드 입력 저장
        key = event.key()
        # 키보드 입력이 반환인 경우 (ENTER)
        if self.name == False:
            if key == QtCore.Qt.Key_Return:
                self.entrance_btn.click()

    def Idchat(self, address, port, cnt):
        self.idclient = ID(address, port, cnt)
        # b = self.entrance()

        # if b:
        #     self.idclient.disconnect()

    def Chat(self, username, address, port):

        self.signal = MySignal()
        self.signal.listUser.connect(self.listUpdate)
        self.signal.chatLabel.connect(self.chatUpdate)

        self.client = Client(username, address, port, self)

        self.msg_send_btn.clicked.connect(self.newmsg)
        self.chat_tableWidget.cellDoubleClicked.connect(self.friendinvite)

    def friendinvite(self):
        column = self.chat_tableWidget.columnCount()
        row = self.chat_tableWidget.currentRow()

        self.chatinvite = []
        for i in range(1, column):
            self.chatinvite.append(self.chat_tableWidget.item(row, i).text())
        reply = QMessageBox.question(self,'초대',f'{self.chatinvite[0]}님을 채팅방에 초대하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.client.sendMsg(self.chatinvite[0], MEMBER_INVITE)

    def newmsg(self):

        msg = self.msg_lienEdit.text()
        if(msg):

            self.client.sendMsg(msg, NEW_MESSAGE)
            self.msg_lienEdit.setText('')
    
    def chatUpdate(self, str):
        self.chat.append(str)
        
    def listUpdate(self, str):

        if(str == ''):
            self.userList.clear()
        
        else:
            self.userList.append(str)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,'메세지','프로그램 종료 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            checkLogout(self.name)
            self.close()
        else:
            pass
    # def keyPressEvent(self, event):

    #     key = event.key()

    #     if key == QtCore.Qt.Key_Return and self.msg_lienEdit:
    #         self.msg_send_btn.click()

# 버튼 클릭시 신호를 서버와 주고 받기

class ID():
    # 소켓 클라이언트 초기화
    def __init__(self, address, port, cnt):
#         # 연결 유형 정리
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # 소켓 서버와 연결
        ADDR = (address, int(port))
        self.client.connect(ADDR)
        self.cnt = cnt

        self.online = True

        message, send_length = encodeMsg(self.cnt)
        self.client.send(send_length) 
        self.client.send(message) 
        self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        self.thread_recv.start()
    
    def recvMsg(self):
        while self.online:
            try:
                # 서버에서 메세지 받기 위해 대기 중
                msg_length = self.client.recv(HEADER).decode(FORMAT)

                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)
                    # 메세지 처리를 위한 함수 호출
                    self.handleMsg(msg)
            
            except: # 오류 또는 연결 실패가 있는 경우
                self.online = False
#         # 매개 변수 수신
#         self.username = username
#         self.online = True

# 클라이언트 작업자 클래스
# 소켓 연결 관리
# 메세지 수신 및 처리 
# 메세지 전송 처리

class Client():

    # 소켓 클라이언트 초기화
    def __init__(self, username, address, port, win):
        # 연결 유형 정리
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 소켓 서버와 연결
        ADDR = (address, int(port))
        self.client.connect(ADDR)

        # 매개변수 수신
        self.username = username # 인스턴스 사용자 이름 설정
        self.win = win # 통신창 참조 저장
        self.online = True # 클라이언트를 온라인으로 설정

        # 사용자 이름을 서버로 보내기

        message, send_length = encodeMsg(self.username)
        self.client.send(send_length) # 유저 이름 길이
        self.client.send(message) # 유저 이름


        # 메세지를 받을 쓰레드 생성
        self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        self.thread_recv.start()
    
    # 메세지 수신
    def recvMsg(self):

        while self.online: # 온라인 상태일 동안만
            try:
                # 서버에서 메세지 받기 위해 대기 중
                msg_length = self.client.recv(HEADER).decode(FORMAT)

                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.recv(msg_length).decode(FORMAT)
                    # 메세지 처리를 위한 함수 호출
                    self.handleMsg(msg)
            
            except: # 오류 또는 연결 실패가 있는 경우
                self.online = False
        
    # 메세지 처리
    def handleMsg(self, msg):

        # 메세지에서 태그 분리
        print(msg)
        re = msg[0] # 첫 번째 문자 저장
        msg_list = list(msg) # 목록으로 변환
        print(msg_list)
        msg_list.pop(0) # 태그 삭제
        msg = "".join(msg_list)  # 문자열에 저장
        print(msg)


        # 수행할 작업 정의
        if (re == NEW_MESSAGE): # 새로운 메세지 TAG인 경우
            self.win.signal.chatLabel.emit(msg) # 메세지를 나타내기 위해 인터페이스에 신호 보내기

        elif (re == CLEAR_LIST): # 목록을 지우는 TAG인 경우
            self.win.signal.listUser.emit('') # 연결된 사용자 목록을 지우는 창에 빈 신호를 보낸다.
        
        elif (re == NAME_LIST): # 이름 목록인 경우
            self.win.signal.listUser.emit(msg) # 창에 이름 보내기, 연결된 사용자 목록에 추가

    # 메세지 전송
    def sendMsg(self, msg, re):

        if (self.online): # 사용자가 온라인 상태인 경우
            try:
                msg = re + msg # 메세지에 태그 추가
                message, send_length = encodeMsg(msg)
                self.client.send(send_length) 
                self.client.send(message)


            except: # 통신이 실패할 경우
                self.disconnect() # 연결 해제

    # 연결 해제
    def disconnect(self):

        if (self.online):
            # 연결 해제 메시지와 함께 신호를 보낸다
            self.win.signal.chatLabel.emit("연결을 끊는 중입니다...")

            # 서버에 연결 해제 메세지 보내기
            message, send_length = encodeMsg(DISCONNECT_MESSAGE)
            self.client.send(send_length)
            self.client.send(message)

            # 클라이언트를 오프라인으로 설정하고 연결을 닫고 신호를 보낸다.
            self.online = False
            self.client.close()
            self.win.signal.chatLabel.emit("연결이 종료 되었습니다.")


# 소켓을 통해 보낼 메세지를 인코드 하는 함수
def encodeMsg(msg):

    message = str(msg).encode(FORMAT) # UTF-8 형식으로 인코드
    msg_length = len(message) # 인코딩된 메세지 크기 저장
    send_length = str(msg_length).encode(FORMAT)
    # 정의된 HEADER와 같을 때까지 공백으로 길이 메세지를 완성한다.
    send_length += b' ' * (HEADER - len(send_length))  

    return message, send_length
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LogWindow()
    win.show()
    app.exec_()
