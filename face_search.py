import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
import pymysql
import search_face
import set_id

class searchWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.search_ui = search_face.Ui_MainWindow()
        self.search_ui.setupUi(self)
        self.search_ui.radioButton_2.setChecked(True)#设置默认选项
        self.search_ui.search.clicked.connect(self.Search)
        self.search_ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def Search(self):
        conn = pymysql.connect(
            # 数据库的IP地址
            host="127.0.0.1",  # 数据库用户名称
            user="root",  # 数据库用户密码
            password="123456",  # 数据库名称
            db="face_manage",  # 数据库端口名称
            port=3306,  # 数据库的编码方式 注意是utf8
            charset="utf8"
        )
        cursor = conn.cursor()
        self.search_ui.tableWidget.setColumnWidth(2, 200)
        if self.search_ui.radioButton.isChecked():
            ret = self.r_checkbox(cursor)
            if ret == ():
                reply = QMessageBox.warning(self, "警告", "信息不存在！")
                return
            elif ret == 0:
                reply = QMessageBox.warning(self, "警告", "查询失败，输入为空！")
                return
            # TableWidget.setHorizontalHeaderLabels(['姓名','性别','体重（kg）'])
            self.search_ui.tableWidget.setRowCount(len(ret))
            self.search_ui.tableWidget.setHorizontalHeaderLabels(['id', '结果', '时间'])
            i = 0
            j = 0
            for r in ret:
                for r_2 in r:
                    print(r_2)
                    if r_2 == 'Y':
                        r_2 = '识别成功'
                    elif r_2 == 'N':
                        r_2 = '识别失败'
                    r_2 = QTableWidgetItem(r_2)
                    self.search_ui.tableWidget.setItem(i, j, r_2)
                    print(i, j)
                    j = j + 1
                i = i + 1
                j = 0
            #结果查询
        elif self.search_ui.radioButton_2.isChecked():
            ret = self.r2_checkbox(cursor)
            if ret == ():
                reply = QMessageBox.warning(self, "警告", "信息不存在！")
                return
            elif ret == 0:
                reply = QMessageBox.warning(self, "警告", "查询失败，输入为空！")
                return
            self.search_ui.tableWidget.setRowCount(len(ret))
            self.search_ui.tableWidget.setHorizontalHeaderLabels(['id', '信息录入', '录入时间'])
            i = 0
            j = 0
            for r in ret:
                for r_2 in r:
                    print(r_2)
                    if j == 1:
                        r_2 = '录入成功'
                    r_2 = QTableWidgetItem(r_2)
                    self.search_ui.tableWidget.setItem(i, j, r_2)
                    print(i, j)
                    j = j + 1
                i = i + 1
                j = 0

            #信息查询
        else:
            sql = "select * from manager_table where id = '%s'"
            print(set_id.get_id())
            cursor.execute(sql % set_id.get_id())
            ret = cursor.fetchone()
            print(ret)
            if ret == None:
                reply = QMessageBox.warning(self, "警告", "您无权进行此操作！")
                return
            else:
                ret = self.r3_checkbox(cursor)
                print(ret)
                if ret == ():
                    reply = QMessageBox.warning(self, "警告", "信息不存在！")
                    return
                elif ret == 0:
                    reply = QMessageBox.warning(self, "警告", "查询失败，输入为空！")
                    return
                self.search_ui.tableWidget.setRowCount(len(ret))
                self.search_ui.tableWidget.setHorizontalHeaderLabels(['id', '姓名', '性别', 'group'])
                i = 0
                j = 0
                for r in ret:
                    for r_2 in r:
                        # print(r_2)
                        r_2 = QTableWidgetItem(r_2)
                        self.search_ui.tableWidget.setItem(i, j, r_2)
                        # print(i, j)
                        j = j + 1
                    i = i + 1
                    j = 0
            #用户查询
        cursor.close()
        conn.close()

    #结果查询的复选框
    def r_checkbox(self, cursor):
        if self.search_ui.checkBox.isChecked():
            c1_id = self.search_ui.lineEdit.text()
            if self.search_ui.checkBox_2.isChecked():
                c1_time = self.search_ui.lineEdit_2.text()
                sql = "select * from result_table where id = '%s' and result_time like '%s'"
                cursor.execute(sql % (c1_id, c1_time+'%'))
            else:
                sql = "select * from result_table where id = '%s'"
                cursor.execute(sql % c1_id)
        elif self.search_ui.checkBox_2.isChecked():
            c1_time = self.search_ui.lineEdit_2.text()
            sql = "select * from result_table where result_time like '%s'"
            cursor.execute(sql % (c1_time+'%'))
        else:
            sql = ''
            return 0
        ret = cursor.fetchall()
        print(ret)
        return ret

    def r2_checkbox(self, cursor):
        if self.search_ui.checkBox_8.isChecked():
            c2_id = self.search_ui.lineEdit_7.text()
            if self.search_ui.checkBox_7.isChecked():
                c2_time = self.search_ui.lineEdit_8.text()
                sql = "select * from face_table where id = '%s' and register_time like '%s'"
                cursor.execute(sql % (c2_id, c2_time+'%'))
            else:
                sql = "select * from face_table where id = '%s'"
                cursor.execute(sql % c2_id)
        elif self.search_ui.checkBox_7.isChecked():
            c2_time = self.search_ui.lineEdit_8.text()
            sql = "select * from face_table where register_time like '%s'"
            cursor.execute(sql % (c2_time+'%'))
        else:
            sql = ""
            return 0
        ret = cursor.fetchall()
        # print(ret)
        return ret

    def r3_checkbox(self, cursor):
        if self.search_ui.checkBox_3.isChecked():#a
            c3_id = self.search_ui.lineEdit_3.text()
            if self.search_ui.checkBox_4.isChecked():#b
                c3_sex = self.search_ui.lineEdit_4.text()
                if self.search_ui.checkBox_6.isChecked():#c
                    c3_name = self.search_ui.lineEdit_5.text()
                    if self.search_ui.checkBox_5.isChecked():#d
                        c3_group = self.search_ui.lineEdit_6.text()#abcd
                        sql ="select id,user_name,sex,group_name from user_table where id = '%s' and sex = '%s' and user_name = '%s' and group_name = '%s'"
                        cursor.execute(sql % (c3_id, c3_sex, c3_name, c3_group))
                    else:#abc
                        sql = "select id,user_name,sex,group_name from user_table where id = '%s' and sex = '%s' and user_name = '%s'"
                        cursor.execute(sql % (c3_id, c3_sex, c3_name))
                elif self.search_ui.checkBox_5.isChecked():#abd
                    c3_group = self.search_ui.lineEdit_6.text()
                    sql = "select id,user_name,sex,group_name from user_table where id = '%s' and sex = '%s' and group_name = '%s'"
                    cursor.execute(sql % (c3_id, c3_sex, c3_group))
                else:#ab
                    sql = "select id,user_name,sex,group_name from user_table where id = '%s' and sex = '%s'"
                    cursor.execute(sql % (c3_id, c3_sex))
            elif self.search_ui.checkBox_6.isChecked():
                c3_name = self.search_ui.lineEdit_5.text()
                if self.search_ui.checkBox_5.isChecked():#acd
                    c3_group = self.search_ui.lineEdit_6.text()
                    sql = "select id,user_name,sex,group_name from user_table where id = '%s' and user_name = '%s' and group_name = '%s'"
                    cursor.execute(sql % (c3_id, c3_name, c3_group))
                else:#ac
                    sql = "select id,user_name,sex,group_name from user_table where id = '%s' and user_name = '%s'"
                    cursor.execute(sql % (c3_id, c3_name))
            elif self.search_ui.checkBox_5.isChecked():#ad
                c3_group = self.search_ui.lineEdit_6.text()
                sql = "select id,user_name,sex,group_name from user_table where id = '%s' and group_name = '%s'"
                cursor.execute(sql % (c3_id, c3_group))
            else:#a
                sql = "select id,user_name,sex,group_name from user_table where id = '%s'"
                cursor.execute(sql % (c3_id))
        elif self.search_ui.checkBox_4.isChecked():
            c3_sex = self.search_ui.lineEdit_4.text()
            if self.search_ui.checkBox_6.isChecked():
                c3_name = self.search_ui.lineEdit_5.text()
                if self.search_ui.checkBox_5.isChecked():#bcd
                    c3_group = self.search_ui.lineEdit_6.text()
                    sql = "select id,user_name,sex,group_name from user_table where sex = '%s' and user_name = '%s' and group_name = '%s'"
                    cursor.execute(sql % (c3_sex, c3_group))
                else:#bc
                    sql = "select id,user_name,sex,group_name from user_table where sex = '%s' and user_name = '%s'"
                    cursor.execute(sql % (c3_sex, c3_name))
            elif self.search_ui.checkBox_5.isChecked():#bd
                c3_group = self.search_ui.lineEdit_6.text()
                sql = "select id,user_name,sex,group_name from user_table where sex = '%s' and group_name = '%s'"
                cursor.execute(sql % (c3_sex, c3_group))
            else:#b
                print("查询性别"+c3_sex)
                sql = "select id,user_name,sex,group_name from user_table where sex = '%s'"
                cursor.execute(sql % (c3_sex))
        elif self.search_ui.checkBox_6.isChecked():
            c3_name = self.search_ui.lineEdit_5.text()
            if self.search_ui.checkBox_5.isChecked():#cd
                c3_group = self.search_ui.lineEdit_6.text()
                sql = "select id,user_name,sex,group_name from user_table where user_name = '%s' and group_name = '%s'"
                cursor.execute(sql % (c3_name, c3_group))
            else:#c
                sql = "select id,user_name,sex,group_name from user_table where user_name = '%s'"
                cursor.execute(sql % c3_name)
        elif self.search_ui.checkBox_5.isChecked():#d
            c3_group = self.search_ui.lineEdit_6.text()
            sql = "select id,user_name,sex,group_name from user_table where group_name = '%s'"
            cursor.execute(sql % c3_group)
        else:
            sql = ""
            return 0
        ret = cursor.fetchall()
        print(ret)
        return ret


if __name__ == '__main__':
    app = QApplication(sys.argv)
    search_win = searchWindow()

    search_win.show()
    sys.exit(app.exec_())