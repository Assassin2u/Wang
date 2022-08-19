import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pymysql
import register


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = register.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.main_ui.pushButton.clicked.connect(self.convert)

    def convert(self):
        ui = self.main_ui
        id = str(ui.id.text())
        password = str(ui.password.text())
        group = str(ui.group.text())
        user_name = str(ui.user_name.text())
        sex = str(ui.sex.currentText())
        manage = str(ui.manage.currentText())
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            db="face_manage",
            port=3306,
            charset="utf8"
        )
        if id == '' or password == '' or group == '' or user_name == '':
            reply = QMessageBox.warning(self, "警告", "信息不能为空！")
            return
        cursor = conn.cursor()
        if manage == 'N':
            sql_1 = 'insert into user_table (id,pwd,group_name,user_name,sex) values (%s,%s,%s,%s,%s);'

        else:
            sql_1 = 'insert into manager_table (id,pwd,manage_group,manager_name,sex) values (%s,%s,%s,%s,%s);'

        sql_2 = "select * from user_table where id = '%s'"
        sql_3 = "select * from manager_table where id = '%s'"
        cursor.execute(sql_2 % id)
        # print(id, password, group, user_name, sex)
        ret_1 = cursor.fetchone()
        # print(ret_1)
        cursor.execute(sql_3 % id)   #确保id在用户信息表和管理员信息表中都不存在
        ret_2 = cursor.fetchone()
        # print(ret_2)

        if ret_1 or ret_2:
            reply = QMessageBox.warning(self, "注册失败", "id已存在，请输入！")
        else:
            cursor.execute(sql_1, [id, password, group, user_name, sex])
            reply = QMessageBox.warning(self, "注册成功", "注册成功!")

        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = register.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    p_win = parentWindow()

    p_win.show()
    sys.exit(app.exec_())
