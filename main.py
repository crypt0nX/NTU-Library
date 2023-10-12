# -*- coding: utf-8 -*-
import os
import util.hitokoto as hitokoto
import subprocess
from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

# set token or get from environments
import config
import time
import check_if_banned

APPSERECT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TOKEN = os.getenv("WECHAT_TOKEN", "XXXXXXXXXXXX")
AES_KEY = os.getenv("WECHAT_AES_KEY", "")
APPID = os.getenv("WECHAT_APPID", "XXXXXXXXXXXXXXXXXXX")

app = Flask(__name__)

PUBLIC_MESSAGE = "\n\n【公告】\n近期后台发现数起情侣👫利用本公众号共同占座事件🤮🤮🤮，\n这种行为既违反了使用说明中的规定，也不是本公众号的初衷。\n\n我依据规定赠送相关账号飞机票一张👊。"

@app.route("/")
def index():
    host = request.url_root
    return render_template("index.html", host=host)


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        openid = msg.source
        if msg.content[:4] == "设置账号":
            try:
                data = msg.content.split(" ")
                username = data[1]
                passwd = data[2]
                config.update_username_passwd(username=username, passwd=passwd, openid=openid)
                reply = create_reply("您的账号密码信息已经成功更新😏", msg)
            except Exception as e:
                print(e)
                reply = create_reply("请按照格式输入账号密码😤", msg)
        elif msg.content[:4] == "设置座位":
            try:
                data = msg.content.split(" ")
                seatNum = data[1]
                config.update_seatNum(seatNum=seatNum, openid=openid)
                reply = create_reply("您的座位信息已经成功更新🤓", msg)
            except Exception as e:
                print(e)
                reply = create_reply("请按照格式输入座位😥", msg)
        elif msg.content[:4] == "设置场馆":
            try:
                data = msg.content.split(" ")
                roomId = data[1]
                config.update_roomId(roomId=roomId, openid=openid)
                reply = create_reply("您的场馆信息已经成功更新！", msg)
            except Exception as e:
                print(e)
                reply = create_reply("请按照格式输入场馆😟", msg)

        elif msg.content[:4] == "设置时间":
            try:
                data = msg.content.split(" ")
                startTime = data[1]
                time.strptime(startTime, "%H:%M")
                endTime = data[2]
                time.strptime(endTime, "%H:%M")
                config.update_startTime(startTime=startTime, openid=openid)
                config.update_endTime(endTime=endTime, openid=openid)
                reply = create_reply("您的时间信息已经成功更新🤤", msg)
            except Exception as e:
                print(e)
                reply = create_reply("请按照格式输入时间😠，注意使用英文冒号", msg)

        elif msg.content[:6] == "设置抢座时间":
            try:
                data = msg.content.split(" ")
                reserve_time = data[1]
                time.strptime(reserve_time, "%H:%M:%S")
                config.update_reserve_time(openid=openid, reserve_time=reserve_time)
                reply = create_reply("您的抢座时间信息已经成功更新😜", msg)
            except Exception as e:
                print(e)
                reply = create_reply("请按照格式输入抢座时间😢，注意使用英文冒号", msg)

        elif msg.content[:4] == "别举报我":
            try:
                if not check_if_banned.check(openid):
                    if config.verify_anti_supervision_Pid(openid):
                        cmd = "python3 anti_supervision.py " + openid
                        p = subprocess.Popen(cmd, shell=True)
                        reply = create_reply("反举报保护已开启😎，持续时间为二小时！" + PUBLIC_MESSAGE, msg)
                    else:
                        reply = create_reply("您已经开启反举报保护了，无法开启另一个🤣", msg)
                else:
                    pid = config.get_pid(openid)
                    os.system("sudo kill -9 " + str(pid))
                    reply = create_reply("🈲🈲🈲\n您目前因为违反相关使用规定被暂停账号使用功能\n如觉误封号，请联系我", msg)
            except Exception as e:
                 print(e)
                 reply = create_reply("出错了🤣", msg)

        elif msg.content[:2] == "开始":
            try:
                if not check_if_banned.check(openid):
                    if config.verifyPid(openid):
                        cmd = "python3 reserve.py " + openid
                        p = subprocess.Popen(cmd, shell=True)
                        reply = create_reply("您的抢座已经成功开始🥳" + PUBLIC_MESSAGE, msg)
                    else:
                        reply = create_reply("您已经有一个抢座进程了，无法开始另一个😫", msg)
                else:
                    pid = config.get_pid(openid)
                    os.system("sudo kill -9 " + str(pid))
                    reply = create_reply("🈲🈲🈲\n您目前因为违反相关使用规定被暂停账号使用功能\n如觉误封号，请联系我", msg)
            except Exception as e:
                reply = create_reply("出现错误，请检查账号密码☹️", msg)
        elif msg.content[:2] == "签到":
            try:
                if not check_if_banned.check(openid):
                    config.sign(openid=openid)
                    reply = create_reply("已经成功签到😝" + PUBLIC_MESSAGE, msg)
                else:
                    pid = config.get_pid(openid)
                    os.system("sudo kill -9 " + str(pid))
                    reply = create_reply("🈲🈲🈲\n您目前因为违反相关使用规定被暂停账号使用功能\n如觉误封号，请联系我", msg)
            except Exception as e:
                reply = create_reply("Sorry, can not handle this for now", msg)
        elif msg.content[:3] == "场馆表":
            try:
                message = config.get_all_room_and_seat(openid)
                reply = create_reply(message + PUBLIC_MESSAGE, msg)
            except Exception as e:
                reply = create_reply("请检查账号密码是否正确😡", msg)

        elif msg.content[:2] == "停止":
            try:
                pid = config.get_pid(openid)
                os.system("sudo kill -9 " + str(pid))
                reply = create_reply("停止成功😇", msg)
            except Exception as e:
                reply = create_reply("Sorry, can not handle this for now", msg)

        elif msg.content[:4] == "结束保护":
            try:
                pid = config.get_anti_supervision_pid(openid)
                os.system("sudo kill -9 " + str(pid))
                reply = create_reply("座位保护结束成功😇", msg)
            except Exception as e:
                reply = create_reply("Sorry, can not handle this for now", msg)

        elif msg.content[:2] == "查询":
            if not check_if_banned.check(openid):
                try:
                    message = config.get_info(openid)
                    if msg:
                        reply = create_reply(message + PUBLIC_MESSAGE, msg)
                    else:
                        reply = create_reply("请检查账号密码以及先前设置是否正确🤮", msg)

                except Exception as e:
                    reply = create_reply("请检查账号密码以及先前设置是否正确🤮", msg)
            else:
                pid = config.get_pid(openid)
                os.system("sudo kill -9 " + str(pid))
                reply = create_reply("🈲🈲🈲\n您目前因为违反相关使用规定被暂停账号使用功能\n如觉误封号，请联系我", msg)
        else:
            reply = create_reply(hitokoto.hitokoto(), msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == "text":
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply("Sorry, can not handle this for now", msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=True)
