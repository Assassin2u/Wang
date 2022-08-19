import sys
from numpy import array
import face_search
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import face_match
import face_recognition
import cv2
import pymysql
import set_id
import datetime
import info_ui

class faceWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.CAM_NUM = 0
        self.f = False
        self.reply_flag = 0
        self.face_ui = face_match.Ui_MainWindow()
        self.face_ui.setupUi(self)
        self.face_ui.face_register.clicked.connect(self.clicked_face_r)
        self.face_ui.face_match.clicked.connect(self.clicked_face_m)
        self.info_win = info_ui.info_ma()
        self.face_ui.face_manage.clicked.connect(self.info_win.show)
        self.timer_1 = QTimer()
        self.timer_2 = QTimer()
        self.timer_1.timeout.connect(self.face_reg)
        self.timer_2.timeout.connect(self.face_m)
        # self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        self.search_win = face_search.searchWindow()
        self.face_ui.face_search.clicked.connect(self.search_win.show)
        self.clock = 50

    def clicked_face_r(self):
        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        if self.timer_1.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(self, u"Warning", u"识别错误！", buttons=QMessageBox.Ok)
            else:
                self.timer_1.start(30)
                self.face_ui.face_register.setText(u'停止录入')
        else:
            self.timer_1.stop()
            self.cap.release()
            self.face_ui.label.clear()
            self.face_ui.label.setPixmap(QPixmap(":/images/c.jpg"))
            self.face_ui.face_register.setText(u'信息录入')
            self.f = False
            self.clock = 50
            self.reply_flag = 0

    def face_reg(self):
        flag, image = self.cap.read()
        show = cv2.resize(image, (640, 500))
        self.clock = self.clock - 1
        print(self.clock, self.f)
        if (not self.f) and (self.clock == 1):
            print("进入")
            face_locations = face_recognition.face_locations(image)
            face_encode = face_recognition.face_encodings(image, face_locations)
            print(face_encode)
            self.face_store(face_encode, set_id.get_id())
        # print(face_encode)
        # print(set_id.get_id())
        # face_locations = face_recognition.face_locations(image)
        # face_encode = face_recognition.face_encodings(image, face_locations)
        # print(face_encode)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.face_ui.label.setPixmap(QPixmap.fromImage(showImage))

    def face_store(self, face_encode, id):
        print("进入函数")
        if face_encode == []:
            self.clock = 50
            return
        # 将numpy array类型转化为列表
        encoding_array_list = face_encode[0].tolist()
        # print(id)
        # 将列表里的元素转化为字符串
        encoding_str_list = [str(i) for i in encoding_array_list]
        # 拼接列表里的字符串
        encoding_str = ','.join(encoding_str_list)
        # 被识别者姓名
        # print(encoding_str)
        name = id
        # 将人脸特征编码存进数据库
        self.saveinto_database(encoding_str, name)

    def saveinto_database(self, code, id):
        conn = pymysql.connect(
            # 数据库的IP地址
            host="127.0.0.1",
            # 数据库用户名称
            user="root",
            # 数据库用户密码
            password="123456",
            # 数据库名称
            db="face_manage",
            # 数据库端口名称
            port=3306,
            # 数据库的编码方式 注意是utf8
            charset="utf8"
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        # SQL插入语句
        insert_sql = "insert into face_table (id,code,register_time) values(%s,%s,%s);"
        try:
            dt = datetime.datetime.now()
            dt_now = str(dt.strftime('%Y-%m-%d %H:%M:%S'))
            # 执行sql语句
            # print(dt_now, id)
            cursor.execute(insert_sql, [id, code, dt_now])
            # 提交到数据库执行
            conn.commit()
            reply = QMessageBox.warning(self, "提示", "信息录入成功！")
            self.f = True
        except Exception as e:
            # 如果发生错误则回滚并打印错误信息
            if self.reply_flag == 0:
                conn.rollback()
                reply = QMessageBox.warning(self, "注册失败", "信息已存在！")
                print("录入失败！")
                self.reply_flag = 1
                # self.f = True
            print(e)
            # self.timer.stop()
            # self.cap.release()
            # self.face_ui.label.clear()
            # self.face_ui.label.setPixmap(QPixmap(":/images/c.jpg"))
            # self.face_ui.face_register.setText(u'信息录入')
        # 关闭游标
        self.clock = 50
        cursor.close()
        # 关闭数据库连接
        conn.close()

    def clicked_face_m(self):
        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        if self.timer_2.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(self, u"Warning", u"识别失败！", buttons=QMessageBox.Ok)
            else:
                self.timer_2.start(30)
                self.face_ui.face_match.setText(u'停止识别')
        else:
            self.timer_2.stop()
            self.cap.release()
            # print(self.cap.isOpened())
            self.face_ui.label.clear()
            self.face_ui.label.setPixmap(QPixmap(":/images/c.jpg"))
            self.face_ui.face_match.setText(u'人脸识别')
            self.clock = 50
            self.f = False

    def face_m(self):
        # print('进入函数')
        # process_this_frame = True
        # 读取摄像头画面
        # print(self.cap.isOpened())
        ret, image = self.cap.read()
        show_1 = cv2.resize(image, (640, 500))
        # show = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        show = cv2.cvtColor(show_1, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.face_ui.label.setPixmap(QPixmap.fromImage(showImage))
        print(self.f)
        self.clock = self.clock - 1
        if self.clock <= 0:
            self.clock = 50
        print(self.clock)
        if (not self.f) and (self.clock == 1):
            face_code1 = self.search_database()
            # print(face_code1)
            face_locations = face_recognition.face_locations(image)
            face_code2 = face_recognition.face_encodings(image, face_locations)
            for face_encoding in face_code2:
                # print(face_encoding)
                match = face_recognition.compare_faces([face_code1], face_encoding, tolerance=0.31)
                if match[0]:
                    judge = "Y"
                    print("match successful")
                    reply = QMessageBox.warning(self, "提示", "匹配成功！")
                else:
                    judge = "N"
                    print("match fail")
                    reply = QMessageBox.warning(self, '提示', '匹配失败！')
            self.store_result(judge, set_id.get_id())
            # face_loc = face_recognition.face_locations(show_1)
            # for (top, right, bottom, left) in face_loc:
            #     cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            #     cv2.rectangle(image, (left, bottom), (right, bottom), (0, 0, 255), 2)

    def search_database(self):
        conn = pymysql.connect(
            # 数据库的IP地址
            host="127.0.0.1",
            # 数据库用户名称
            user="root",
            # 数据库用户密码
            password="123456",
            # 数据库名称
            db="face_manage",
            # 数据库端口名称
            port=3306,
            # 数据库的编码方式 注意是utf8
            charset="utf8"
        )
        cursor = conn.cursor()
        try:
            sql = "select code from face_table where id = '%s'"
            # 执行SQL语句
            cursor.execute(sql % set_id.get_id())
            # 获取所有记录列表
            results = cursor.fetchall()
            # print(results[0][0])
            # 返回的结果集为元组
            # print("name=%s,encoding=%s" % (name, encoding))
            # 将字符串转为numpy ndarray类型，即矩阵
            # 转换成一个list
            dlist = results[0][0].strip(' ').split(',')
            # 将list中str转换为float
            dfloat = list(map(float, dlist))
            arr = array(dfloat)
            # print(arr, type(arr))
            return arr
        except Exception as e:
            print(e)
            # 关闭数据库连接
        conn.close()

    def store_result(self, a, user_id):
        conn = pymysql.connect(
            # 数据库的IP地址
            host="127.0.0.1",
            # 数据库用户名称
            user="root",
            # 数据库用户密码
            password="123456",
            # 数据库名称
            db="face_manage",
            # 数据库端口名称
            port=3306,
            # 数据库的编码方式 注意是utf8
            charset="utf8"
        )
        cursor = conn.cursor()
        # SQL插入语句
        # print("输入语句")
        insert_sql = "insert into result_table(id,if_success,result_time,group_name) values(%s,%s,%s,%s)"
        group_sql = "select group_name from user_table where id = %s"
        group_sql_1 = "select manage_group from manager_table where id = %s"
        try:
            dt = datetime.datetime.now()
            dt_now = dt.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(group_sql % user_id)
            group_name = cursor.fetchone()
            # print(group_name)
            if group_name == None:
                cursor.execute(group_sql_1 % user_id)
                group_name = cursor.fetchone()
                # print(group_name)
            # 执行sql语句
            print(dt_now, a, group_name)
            cursor.execute(insert_sql, [user_id, a, dt_now, group_name[0]])
            print('执行存储')
            # 提交到数据库执行
            conn.commit()
            print('存储成功')
            self.f = True
        except Exception as e:
            # 如果发生错误则回滚并打印错误信息
            conn.rollback()
            print(e)
        # 关闭游标
        self.clock = 50
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    face_win = faceWindow()  #实例对象

    face_win.show()
    sys.exit(app.exec_())