import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pymysql
import main_ui
import r_ui
import face_re
import set_id


class mainswindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.login_ui = main_ui.Ui_MainWindow()
        self.login_ui.setupUi(self)
        self.login_ui.pushButton.clicked.connect(self.user_login)
        self.r_win = r_ui.parentWindow()
        self.login_ui.pushButton_2.clicked.connect(self.r_win.show)

    def user_login(self):
        ui = self.login_ui
        conn = pymysql.connect(
            # 数据库的IP地址
            host="127.0.0.1",  # 数据库用户名称
            user="root",  # 数据库用户密码
            password="123456",  # 数据库名称
            db="face_manage",  # 数据库端口名称
            port=3306,  # 数据库的编码方式 注意是utf8
            charset="utf8"
        )
        id = str(ui.lineEdit.text())
        pwd = str(ui.lineEdit_2.text())
        # print(id, pwd)
        # global new_id
        # new_id = id
        if id == "" or pwd == "":
            reply = QMessageBox.warning(self, "警告", "账号密码不能为空，请输入！")
            return
        set_id.set_id(id)
        # print(type(set_id.get_id()))
        cursor = conn.cursor()
        sql_1 = "select * from user_table where id = '%s' and pwd = '%s' "
        sql_2 = "select * from manager_table where id = '%s' and pwd = '%s'"
        cursor.execute(sql_1 % (id, pwd))
        ret = cursor.fetchall()
        # print(ret)
        cursor.execute(sql_2 % (id, pwd))
        ret = ret+cursor.fetchall()
        if ret:
            face_win.show()
            self.close()
        else:
            reply = QMessageBox.warning(self, "注意", "账号或密码不正确，请重新输入！")
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = register.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    main_win = mainswindow()
    face_win = face_re.faceWindow()

    main_win.show()
    sys.exit(app.exec_())