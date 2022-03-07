import requests
import re
import execjs


def login_authserver_ntu(uname, pwd):
    sess = requests.session()
    login_url = 'http://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas/ntu' \
                '/index '
    get_login = sess.get(login_url)
    get_login.encoding = 'utf-8'
    lt = re.search('name="lt" value="(.*?)"', get_login.text).group(1)
    salt = re.search('id="pwdDefaultEncryptSalt" value="(.*?)"', get_login.text).group(1)
    execution = re.search('name="execution" value="(.*?)"', get_login.text).group(1)
    encrypt_script_url = 'http://authserver.ntu.edu.cn/authserver/custom/js/encrypt.js'
    js = requests.get(encrypt_script_url).text
    ctx = execjs.compile(js)
    password = ctx.call('_ep', pwd, salt)

    login_post_url = 'http://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas' \
                     '/ntu/index '
    personal_info = {'username': uname,
                     'password': password,
                     'lt': lt,
                     'dllt': 'userNamePasswordLogin',
                     'execution': execution,
                     '_eventId': 'submit',
                     'rmShown': '1'}
    post_login = sess.post(login_post_url, personal_info, allow_redirects=False)
    post_login.encoding = 'utf-8'
    ticket = post_login.headers['SET-COOKIE'].split(';')[0][7:]
    print(ticket)
    return ticket

