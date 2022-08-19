import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pwd_change
import pymysql

class pwdWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.pwd_ui = pwd_change.Ui_MainWindow()
        self.pwd_ui.setupUi(self)
        self.pwd_ui.lineEdit_4.setPlaceholderText("不进行修改，置空")
        self.pwd_ui.lineEdit_6.setPlaceholderText("同上")
        self.pwd_ui.pushButton.clicked.connect(self.change_pwd)

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

    def change_pwd(self):
        user_id = self.pwd_ui.lineEdit.text()
        old_pwd = self.pwd_ui.lineEdit_2.text()
        new_pwd = self.pwd_ui.lineEdit_3.text()
        name = self.pwd_ui.lineEdit_4.text()
        groups = self.pwd_ui.lineEdit_6.text()
        repeat = self.pwd_ui.lineEdit_5.text()
        # print(new_pwd, groups, type(name))
        if user_id == '' or old_pwd == '' or new_pwd == '' or repeat == '':
            reply = QMessageBox.warning(self, "警告", "信息不能为空")
            return
        if new_pwd != repeat:
            reply = QMessageBox.warning(self, "警告", "两次密码输入不一致！")
            return
        conn, cursor = self.link_database()
        sql_1 = "select * from user_table where id = %s"
        sql_2 = "select * from manager_table where id = %s"
        cursor.execute(sql_1 % user_id)
        ret = cursor.fetchone()
        #judge判断用户信息，2为管理员，1为普通用户
        judge = 1
        if ret == None:
            cursor.execute(sql_2 % user_id)
            ret = cursor.fetchone()
            judge = 2
            if ret == None:
                reply = QMessageBox.warning(self, "提示", "信息错误")
                return
        if name == '':
            if groups == '':
                try:
                    sql_1 = "update user_table set pwd = %s where id = %s and pwd = %s"
                    sql_2 = "update manager_table set pwd = %s where id = %s and pwd = %s"
                    if judge == 1:
                        cursor.execute(sql_1, [new_pwd, user_id, old_pwd])
                    else:
                        cursor.execute(sql_2, [new_pwd, user_id, old_pwd])
                    if cursor.rowcount == 0:
                        reply = QMessageBox.warning(self, "提示", "密码错误！")
                        return
                except Exception as e:
                    conn.rollback()
                    print(e)
                    reply = QMessageBox.warning(self, "提示", "密码错误！")
            else:
                try:
                    sql_1 = "update user_table set pwd = %s , group_name = %s where id = %s and pwd = %s"
                    sql_2 = "update manager_table set pwd = %s , manage_group = %s where id = %s and pwd = %s"
                    if judge == 1:
                        cursor.execute(sql_1, [new_pwd, groups, user_id, old_pwd])
                    else:
                        cursor.execute(sql_2, [new_pwd, groups, user_id, old_pwd])
                    if cursor.rowcount == 0:
                        reply = QMessageBox.warning(self, "提示", "密码错误！")
                        return
                except Exception as e:
                    conn.rollback()
                    print(e)
                    reply = QMessageBox.warning(self, "提示", "密码错误！")
        elif groups == '':
            try:
                sql_1 = "update user_table set pwd = %s , user_name = %s where id = %s and pwd = %s"
                sql_2 = "update manager_table set pwd = %s , manager_name = %s where id = %s and pwd = %s"
                if judge == 1:
                    cursor.execute(sql_1, [new_pwd, name, user_id, old_pwd])
                else:
                    cursor.execute(sql_2, [new_pwd, name, user_id, old_pwd])
                if cursor.rowcount == 0:
                    reply = QMessageBox.warning(self, "提示", "密码错误！")
                    return
                if cursor.rowcount == 0:
                    reply = QMessageBox.warning(self, "提示", "密码错误！")
                    return
            except Exception as e:
                conn.rollback()
                print(e)
        else:
            try:
                sql_1 = "update user_table set pwd = %s , user_name = %s , group_name = %s where id = %s and pwd = %s"
                sql_2 = "update manager_table set pwd = %s , manager_name = %s , manage_group = %s where id = %s and pwd = %s"
                if judge == 1:
                    cursor.execute(sql_1, [new_pwd, name, groups, user_id, old_pwd])
                else:
                    cursor.execute(sql_2, [new_pwd, name, groups, user_id, old_pwd])
                if cursor.rowcount == 0:
                    reply = QMessageBox.warning(self, "提示", "密码错误！")
                    return
            except Exception as e:
                conn.rollback()
                print(e)
                reply = QMessageBox.warning(self, "提示", "密码错误！")
        reply = QMessageBox.warning(self, "提示", "修改成功！")
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pwd_win = pwdWindow()

    pwd_win.show()
    sys.exit(app.exec_())