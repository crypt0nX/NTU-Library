import json
import time
import util.core as core
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from multiprocessing.dummy import Pool as ThreadPool
import util.config as config
import sys
from dateutil import parser
from datetime import datetime, timedelta
import util.split_time as split_time


def reserve_seat(args_dict):
    chaoxing_object = args_dict['chaoxing_object']
    roomId = args_dict['roomId']
    seatNum = args_dict['seatNum']
    startTime = args_dict['startTime']
    endTime = args_dict['endTime']
    main_try_times = 0
    print("开始抢座")
    try:
        while main_try_times < 15:
            if main_try_times > 10:
                time.sleep(0.2)
            #  print(datetime.now())
            main_try_times = main_try_times + 1
            #    print(args_dict['username'] + '  ' + str(datetime.now()) + "  " + "第" + str(main_try_times) + "次尝试")
            status = chaoxing_object.submit(roomId=roomId, seatNum=seatNum, day=time.strftime("%Y-%m-%d"),
                                            startTime=startTime,
                                            endTime=endTime, try_times=main_try_times)
            if status == "成功":
                print("预约成功")
                break
            elif status == "被占用":
                print("被占用")


    except Exception as e:
        print("出错" + str(e))


def reserve_mutil_time(username, password, roomId, seatNum, startTime, endTime):
    time_list = split_time.split_time_ranges(startTime, endTime, 60 * 60 * 6)
    chaoxing = core.CX(username, password)

    args_list = []
    for each_time in time_list[:2]:
        print(each_time)
        args = {"username": "", "password": "", "roomId": "", "seatNum": "", "startTime": "", "endTime": ""}
        args['chaoxing_object'] = chaoxing
        args['username'] = username
        args['password'] = password
        args['roomId'] = roomId
        args['seatNum'] = seatNum
        args['startTime'] = each_time[0]
        args['endTime'] = each_time[1]
        args_list.append(args)
    time.sleep(9)

    pool = ThreadPool()
    pool.map(reserve_seat, args_list)
    pool.close()
    pool.join()


def startJobs(openid, start_reserve_time, username, password, roomId, seatNum, startTime, endTime):
    print("抢座计划开始")
    start_reserve_time = parser.parse(start_reserve_time)
    start_reserve_time = start_reserve_time + timedelta(seconds=-10)
    start_reserve_time = start_reserve_time.strftime("%H:%M:%S")
    #  print(start_reserve_time)
    config.update_pid(openid, os.getpid())
    hour = start_reserve_time.split(':')[0]
    min = start_reserve_time.split(':')[1]
    sec = start_reserve_time.split(':')[2]
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(reserve_mutil_time, 'cron', hour=hour, minute=min, second=sec,
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
