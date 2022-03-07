import json
import time
import util
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from multiprocessing.dummy import Pool as ThreadPool
import config
import sys
from dateutil import parser
from datetime import datetime, timedelta
import split_time

args = {"username": "", "password": "", "roomId": "", "seatNum": "", "startTime": "", "endTime": ""}


def reserve_seat(args_dict):
    chaoxing_object = args_dict['chaoxing_object']
    roomId = args_dict['roomId']
    seatNum = args_dict['seatNum']
    startTime = args_dict['startTime']
    endTime = args_dict['endTime']
    main_try_times = 4
    #  chaoxing = util.CX(username, password)
    #  time.sleep(9)
    print("开始抢座")
    try:
        for i in range(10):
            print("第" + str(i + 1) + "次尝试")
            if main_try_times > 0:
                if chaoxing_object.submit(roomId=roomId, seatNum=seatNum, day=time.strftime("%Y-%m-%d"),
                                          startTime=startTime,
                                          endTime=endTime):
                    print("预约成功")
                    break
                else:
                    main_try_times = main_try_times - 1
                    time.sleep(0.2)
            else:
                pass  # 这里是抢不到随机的函数


    except Exception as e:
        print("出错" + str(e))


def reserve_mutil_time(username, password, roomId, seatNum, startTime, endTime):
    time_list = split_time.split_time_ranges(startTime, endTime, 60 * 60 * 6)
    args_list = []
    chaoxing = util.CX(username, password)

    for each_time in time_list:
        print(each_time)
        args['chaoxing_object'] = chaoxing
        args['username'] = username
        args['password'] = password
        args['roomId'] = roomId
        args['seatNum'] = seatNum
        args['startTime'] = each_time[0]
        args['endTime'] = each_time[1]
        args_list.append(args)

    pool = ThreadPool()
    pool.map(reserve_seat, args_list)
    pool.close()
    pool.join()


def startJobs(openid, start_reserve_time, username, password, roomId, seatNum, startTime, endTime):
    print("抢座计划开始")
    start_reserve_time = parser.parse(start_reserve_time)
    start_reserve_time = start_reserve_time + timedelta(seconds=-10)
    start_reserve_time = start_reserve_time.strftime("%H:%M:%S")
    config.update_pid(openid, os.getpid())
    hour = start_reserve_time.split(':')[0]
    min = start_reserve_time.split(':')[1]
    sec = start_reserve_time.split(':')[2]
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(reserve_seat, 'cron', hour=hour, minute=min, second=sec,
                      args=[username, password, roomId, seatNum, startTime, endTime])
    scheduler.start()


def startReserve(openid):
    file_name = "config/" + openid + ".json"
    with open(file_name) as config_file:
        config = json.load(config_file)

    config_file.close()
    startJobs(openid=openid, start_reserve_time=config['start_reserve_time'], username=config['username'],
              password=config['passwd'], roomId=config['roomId'], seatNum=config['seatNum'],
              startTime=config['startTime'], endTime=config['endTime'])

startReserve(sys.argv[1])
