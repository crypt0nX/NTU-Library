import json
import os
import util
import psutil


def get_pid(openid):
    file_name = "config/" + openid + ".json"
    with open(file_name) as config_file:
        config = json.load(config_file)
    return config['pid']


def check_before_update(openid):
    file_name = "config/" + openid + ".json"
    example_data = {"openid": "user_config_example", "start_reserve_time": "07:00:00", "username": "", "passwd": "",
                    "roomId": "", "seatNum": "",
                    "startTime": "", "endTime": "", "pid": ""}
    if not os.path.exists(file_name):
        print("文件不存在")
        with open(file_name, "w") as jsonFile:
            json.dump(example_data, jsonFile, ensure_ascii=False)
        jsonFile.close()


def update_username_passwd(openid, username, passwd):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()

    data["openid"] = openid
    data["username"] = username
    data["passwd"] = passwd

    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_roomId(openid, roomId):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["roomId"] = roomId
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_seatNum(openid, seatNum):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["seatNum"] = seatNum
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_startTime(openid, startTime):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["startTime"] = startTime
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_endTime(openid, endTime):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["endTime"] = endTime
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_pid(openid, pid):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["pid"] = pid
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def update_reserve_time(openid, reserve_time):
    check_before_update(openid)
    file_name = "config/" + openid + ".json"
    with open(file_name, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    data["start_reserve_time"] = reserve_time
    with open(file_name, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=False)
    jsonFile.close()


def sign(openid):
    file_name = "config/" + openid + ".json"
    with open(file_name) as config_file:
        config = json.load(config_file)
    config_file.close()
    username = config['username']
    password = config['passwd']
    chaoxing = util.CX(username, password)
    chaoxing.sign()


def verifyPid(openid):
    file_name = "config/" + openid + ".json"
    with open(file_name) as config_file:
        config = json.load(config_file)
    config_file.close()
    pid = config['pid']
    if pid:
        try:
            s = psutil.Process(pid)
            if s.status() == "sleeping":
                print(s.status())
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return True
    else:
        return False
