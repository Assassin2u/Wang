import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QAbstractItemView
import info_manage
import set_id
import pymysql
import pwd

class info_ma(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.info_ui = info_manage.Ui_MainWindow()
        self.info_ui.setupUi(self)
        self.change_win = pwd.pwdWindow()
        self.info_ui.pushButton.clicked.connect(self.dele_face)
        self.info_ui.pushButton_2.clicked.connect(self.result_sta)
        self.info_ui.pushButton_3.clicked.connect(self.alter_result)
        self.info_ui.pushButton_4.clicked.connect(self.change_win.show)
        self.info_ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.info_ui.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def link_database(self):
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            db="face_manage",
            port=3306,
            charset="utf8"
        )
        cursor = conn.cursor()
        return conn, cursor

    def dele_face(self):
        conn, cursor = self.link_database()
        # conn = pymysql.connect(
        #     host="127.0.0.1",
        #     user="root",
        #     password="123456",
        #     db="face_manage",
        #     port=3306,
        #     charset="utf8"
        # )
        # cursor = conn.cursor()
        sql = "delete from face_table where id = %s;"
        sql_1 = "select * from face_table where id = %s"
        try:
            cursor.execute(sql_1 % set_id.get_id())
            ret = cursor.fetchone()
            # print(ret)
            if ret == None:
                reply = QMessageBox.warning(self, '提示', '信息不存在！')
                cursor.close()
                conn.close()
                return
            cursor.execute(sql % set_id.get_id())
            # print("删除成功")
            conn.commit()
            reply = QMessageBox.warning(self, '提示', '删除成功！')
        except Exception as e:
            conn.rollback()
            print(e)
        cursor.close()
        conn.close()

    def result_sta(self):
        time = self.info_ui.time_1.text()
        group_name = self.info_ui.group.text()
        if time == '' or group_name == '':
            reply = QMessageBox.warning(self, '警告', '时间和group都不能为空！')
            return
        conn, cursor = self.link_database()
        sql_1 = "select count(distinct (id)) from user_table where group_name = %s"
        sql_3 = "select count(distinct (id)) from manager_table where manage_group = %s"
        sql_2 = "select count(distinct (id)) from result_table where group_name = %s and if_success = %s and result_time like %s"
        try:
            cursor.execute(sql_1 % group_name)
            ret_1 = cursor.fetchone()
            cursor.execute(sql_2, [group_name, 'Y', time+'%'])
            ret_2 = cursor.fetchone()
            cursor.execute(sql_3 % group_name)
            ret_4 = cursor.fetchone()
            ret = int(ret_1[0]) + int(ret_4[0])
            ret_3 = ret-int(ret_2[0])
        except Exception as e:
            conn.rollback()
            print(e)
        cursor.close()
        conn.close()
        print(ret_1, ret_2)
        self.info_ui.tableWidget.setHorizontalHeaderLabels(['总人数', '识别成功人数', '识别失败人数'])
        self.info_ui.tableWidget.setVerticalHeaderLabels([group_name])
        r_1 = QTableWidgetItem(str(ret))
        self.info_ui.tableWidget.setItem(0, 0, r_1)
        # print(ret_1[0])
        r_2 = QTableWidgetItem(str(ret_2[0]))
        self.info_ui.tableWidget.setItem(0, 1, r_2)
        r_3 = QTableWidgetItem(str(ret_3))
        self.info_ui.tableWidget.setItem(0, 2, r_3)

    def alter_result(self):
        # print("进入函数")
        conn, cursor = self.link_database()
        sql = "select * from manager_table where id = '%s'"
        print(set_id.get_id())
        cursor.execute(sql % set_id.get_id())
        ret = cursor.fetchone()
        print(ret)
        if ret == None:
            reply = QMessageBox.warning(self, "警告", "您无权进行此操作！")
            return
        else:
            time = str(self.info_ui.time_2.text())
            user_id = str(self.info_ui.user_id.text())
            if time == '' or user_id == '':
                reply = QMessageBox.warning(self, '警告', '时间和id都不能为空！')
                return
            sql = "select * from result_table where id = %s and result_time like %s"
            sql_2 = "update result_table set if_success = %s where id = %s and result_time like %s"
            sql_3 = "select user_name from user_table where id = %s"
            try:
                cursor.execute(sql, [user_id, time+'%'])
                ret = cursor.fetchall()
                print(ret)
                cursor.execute(sql_3 % user_id)
                name = cursor.fetchone()
                print(name)
            except Exception as e:
                conn.rollback()
                print(e)
            # print(ret)
            if ret == None:
                reply = QMessageBox.warning(self, '提示', '信息不存在！')
                return
            elif ret[1] == 'Y' or ret[0][1] == 'Y':
                reply = QMessageBox.warning(self, '提示', '识别已成功！')
            else:
                cursor.execute(sql_2, ['Y', user_id, time+'%'])
                reply = QMessageBox.warning(self, '提示', '修改成功！')
                conn.commit()
            self.info_ui.tableWidget_2.setRowCount(len(ret))
            self.info_ui.tableWidget.setHorizontalHeaderLabels(['姓名', '识别是否成功', '识别时间'])
            if len(ret) == 1:
                r_1 = QTableWidgetItem(name[0])
                self.info_ui.tableWidget_2.setItem(0, 0, r_1)
                r_2 = QTableWidgetItem('识别成功')
                self.info_ui.tableWidget_2.setItem(0, 1, r_2)
                r_3 = QTableWidgetItem(ret[2])
                self.info_ui.tableWidget_2.setItem(0, 2, r_3)
                return
            i = 0
            j = 0
            for r in ret:
                for r_2 in r:
                    print(r_2)
                    if r_2 == 'Y':
                        r_2 = '识别成功'
                    elif r_2 == 'N':
                        r_2 = '识别失败'
                    elif r_2 == user_id:
                        r_2 = name[0]
                    r_2 = QTableWidgetItem(r_2)
                    self.info_ui.tableWidget_2.setItem(i, j, r_2)
                    print(i, j)
                    j = j + 1
                i = i + 1
                j = 0
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    info_win = info_ma()

    info_win.show()
    sys.exit(app.exec_())