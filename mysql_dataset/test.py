from MyDataBase_Final import MyDataBase

host = "10.18.146.53"
user = "root"
password = "root"
port = 3306
db = "test"
charset = "utf8"

mb = MyDataBase(host, user, password, port, db)
mb.connect()
mb.addWith("output", input="'《赛博朋克测试测试》'", output="'游戏'")
mb.showAll("output")
mb.close()



