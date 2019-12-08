


# 引用扩展库
import requests



# 全局定义
G_LastError = ""

EasyMode_Cookies = {}
EasyMode_Headers = {}
EasyMode_Session = requests


# 设置 Cookies
def SetCookies(dictCookies = {}):
    global EasyMode_Cookies
    EasyMode_Cookies = dictCookies

# 设置 Headers
def SetHeaders(dictHeaders = {}):
    global EasyMode_Headers
    EasyMode_Headers = dictHeaders

# 设置指定 Cookie 的值
def SetCookie(sKey, sVal = None):
    global EasyMode_Cookies
    try:
        EasyMode_Cookies[sKey] = sVal
    except:
        return

# 设置指定 Header 的值
def SetHeader(sKey, sVal = None):
    global EasyMode_Headers
    try:
        EasyMode_Headers[sKey] = sVal
    except:
        return

# 获取错误描述
def GetLastError():
    global G_LastError
    return G_LastError

# GET
def Get(sURL, dictForm = {}, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.get(sURL, params = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""

# POST
def Post(sURL, dictForm = {}, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.post(sURL, data = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""

# POST Json
def PostJson(sURL, dictForm = {}, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.post(sURL, json = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""

# 下载文件
def GetFile(sURL, sFile, dictForm = {}, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.get(sURL, params = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        with open(sFile, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        G_LastError = e
        return False

# 提交文件
def PostFile(sURL, dictFile = {}, dictForm = {}, iTimeout = 60000):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 处理文件列表
        for k, v in dictFile.items():
            dictFile[k] = open(v, 'rb')
        # 提交请求
        r = EasyMode_Session.post(sURL, files = dictFile, data = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""

# Head
def Head(sURL, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.head(sURL, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.headers
    except Exception as e:
        G_LastError = e
        return {}

# Put
def Put(sURL, dictForm = {}, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.put(sURL, data = dictForm, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""

# Delete
def Delete(sURL, iTimeout = None):
    global G_LastError
    global EasyMode_Cookies
    global EasyMode_Headers
    global EasyMode_Session
    try:
        # 超时时间参数修正
        if type(iTimeout) == int:
            if iTimeout <= 0:
                iTimeout = None
            else:
                iTimeout = iTimeout / 1000
        else:
            iTimeout = None
        # 提交请求
        r = EasyMode_Session.delete(sURL, timeout = iTimeout, cookies = EasyMode_Cookies, headers = EasyMode_Headers)
        return r.text
    except Exception as e:
        G_LastError = e
        return ""



# 创建 Session
def Session_Create():
    global EasyMode_Session
    EasyMode_Session = requests.session()
    return 0

# 删除 Session
def Session_Free():
    global EasyMode_Session
    EasyMode_Session = requests
    return 0

# 设置 Headers
def Session_SetHeaders(dictHeaders = {}):
    global EasyMode_Session
    try:
        EasyMode_Session.headers.update(dictHeaders) 
    except:
        return 

# 设置指定 Cookies 的值
def Session_SetCookies(dictCookies = {}):
    global EasyMode_Session
    try:
        EasyMode_Session.cookies.update(dictCookies)
    except:
        return

# 设置指定 Cookie 的值
def Session_SetCookie(sKey, sVal = None):
    global EasyMode_Session
    try:
        EasyMode_Session.cookies.update({sKey: sVal})
    except:
        return

# 设置指定 Header 的值
def Session_SetHeader(sKey, sVal = None):
    global EasyMode_Headers
    try:
        EasyMode_Session.headers.update({sKey: sVal})  
    except:
        return

# 获取 Cookies 的值
def Session_GetCookies():
    global EasyMode_Session
    try:
        return requests.utils.dict_from_cookiejar(EasyMode_Session.cookies)
    except:
        return {}

# 测试代码
if __name__ == '__main__':
    print("Get :", Get("http://www.uibot.com.cn"))
    print("Post :", Post("https://open.ucpaas.com/ol/sms/sendsms", '{"sid":"39467b989d087c2d92c6132184a365d8","token":"23f757bad208226ec301e117e40006ed","appid":"2d92c6132139467b989d087c84a365d8","templateid":"154501","param":"87828,3","mobile":"18011984299","uid":"2d92c6132139467b989d087c84a365d8"}'))
    print("GetLastError :", GetLastError())
    print("GetFile :", GetFile("http://www.uibot.com.cn", "d:\\1.htm"))
    print("Head :", Head("http://www.uibot.com.cn"))
