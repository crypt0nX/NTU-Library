def check(openid):
    with open("utils/banned") as file:
        file = file.readlines()
        file = [i.strip('\n') for i in file]
    if openid in file:
        return True
    else:
        return False
