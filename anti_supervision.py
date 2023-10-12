import json
import utils.core as core
import time
import sys
import datetime
import config as con
import os


def anti_supervision(openid):
    con.update_anti_supervision_pid(openid, os.getpid())
    file_name = "config/" + openid + ".json"
    with open(file_name) as config_file:
        config = json.load(config_file)
    config_file.close()
    username = config['username']
    password = config['passwd']
    chaoxing = core.CX(username, password)
    count = 1
    while count <= 40:
        print(str(datetime.datetime.now()) + " " + str(username) + " 正在检查进程 " + "第" + str(count) + "次")
        if chaoxing.get_supervision_status():
            print(str(datetime.datetime.now()) + " " + str(username) + "发现被举报！，正在尝试签到")
            chaoxing.sign()
        time.sleep(180)
        count = count + 1


anti_supervision(sys.argv[1])
