#encoding=utf-8
'''
Created on 2019年10月24日

@author: 瞌睡蟲子
'''
import PyChromeDevTools
import errno
import os
import winreg
import win32api
import re
import base64
from time import sleep

BROWSER = None

def query_reg(hkey, regPath, arch_key):
    path = None
    try:
        key = winreg.OpenKey(hkey, regPath , 0, winreg.KEY_READ | arch_key)
        path = winreg.QueryValueEx(key, '')
        winreg.CloseKey(key)
        return path[0]
    except OSError as e:
        if e.errno == errno.ENOENT:
            # DisplayName doesn't exist in this skey
            pass
    return path

def check_arch_keys():
    proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
    proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
    
    if proc_arch == 'x86' and not proc_arch64:
        arch_keys = {0}
    elif proc_arch == 'x86' or proc_arch == 'amd64':
        arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
    else:
        raise Exception("Unhandled arch: %s" % proc_arch)
    return arch_keys

def get_browser_path(): 
    browsers ={
                "chrome.exe",
                "360chrome.exe",
                "msedge.exe",
                "2345Explorer.exe", 
            }
    arch_keys = check_arch_keys()
    path = None
    for browser in browsers:    
        regPath = "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\" + browser
        for arch_key in arch_keys:
            path = query_reg(winreg.HKEY_LOCAL_MACHINE, regPath, arch_key)
            if path:
                break
            path = query_reg(winreg.HKEY_CURRENT_USER, regPath, arch_key)
            if path:
                break
        if path:
            break
    return path

def OpenBrowser(path=None, **args):
    if not path:
        path = get_browser_path()
    if path:
        if "--remote-debugging-port" not in args.keys():
            args["--remote-debugging-port"] = 9222
        param = [k+("="+str(args[k]) if args[k] else "") for k in args]
        apps=re.findall("([^\\\\/]+)$", path)
        os.system("taskkill /IM " + apps[0]+" /F")
        win32api.ShellExecute(0, 'open', path, " ".join(param),'',1)
        return path
    else:
        return False

def BindBrowser(host='127.0.0.1', port=9222, tab=0, timeout=1, auto_connect=True):
    global BROWSER
    try:
        BROWSER = PyChromeDevTools.ChromeInterface(host, port, tab, timeout, auto_connect)
        BROWSER.DOM.enable()
        BROWSER.Runtime.enable()
        BROWSER.Network.enable()
        BROWSER.Page.enable()
    except Exception:
        BROWSER = None

def EasyBrowser():
    global BROWSER
    BROWSER=None
    while not BROWSER:
        BindBrowser()
        if not BROWSER:
            OpenBrowser()
            sleep(1)        

def CloseBrowser():
    global BROWSER
    BROWSER.Browser.close()

def GetTabs():
    global BROWSER
    tables = BROWSER.Target.getTargets()
    res = []
    for tab in tables["result"]["targetInfos"]:
        if tab["type"] == "page":
            list.append(res, tab)
    return res

def FindTab(url=None, title=None):
    tabs = getTabs()    
    tab1 = list(filter(lambda x: url and url in x["url"], tabs))
    tab2 = list(filter(lambda x: title and title in x["title"], tabs))
    if len(tab1)>0 and len(tab2)>0:
        re = []
        for tb1 in tab1:
            for tb2 in tab2:
                if tb1["targetId"] == tb2["targetId"]:
                    re.append(tb1)
        return re
    elif len(tab1)>0:
        return tab1
    else:
        return tab2
    
def CreateTab(uri="chrome://newtab/"):  
    global BROWSER
    return BROWSER.Target.createTarget(url=uri)        

def CloseTab(tabid):
    global BROWSER
    BROWSER.Target.closeTarget(targetId=tabid)

def ActiveTab(tabid):  
    global BROWSER
    BROWSER.Target.activateTarget(targetId=tabid)
    
def GetTabInfo(tabid):  
    global BROWSER
    return BROWSER.Target.getTargetInfo(targetId=tabid)

def GoUrl(uri):
    global BROWSER
    BROWSER.Page.navigate(url=uri)

def GetPageCookies():
    global BROWSER
    return BROWSER.Page.getCookies()

def ReloadPage(cache=False):
    global BROWSER
    BROWSER.Page.reload(ignoreCache=cache)

def QuerySelector(selector,nodeid=None):
    global BROWSER
    if not nodeid:
        nodeid=BROWSER.DOM.getDocument()
        nodeid=nodeid["result"]["root"]["nodeId"]
    res = BROWSER.DOM.querySelector(nodeId=nodeid,selector=selector)
    return res["result"]["nodeId"] if res["result"]["nodeId"] > 0 else None

def QuerySelectorAll(selector,nodeid=None):
    global BROWSER
    if not nodeid:
        nodeid=BROWSER.DOM.getDocument()
        nodeid=nodeid["result"]["root"]["nodeId"]
    res = BROWSER.DOM.querySelectorAll(nodeId=nodeid,selector=selector)
    return res["result"]["nodeIds"]

def SetAttribute(nodeid, name, value):
    global BROWSER
    BROWSER.DOM.setAttributeValue(nodeId=nodeid,name=name,value=value)

def GetAttributes(nodeid):
    global BROWSER
    attr=BROWSER.DOM.getAttributes(nodeId=nodeid)
    attr=attr["result"]["attributes"]
    res={}
    for i in range(0,len(attr),2):
        res[attr[i]]=attr[i+1]
    return res

def GetHTML(nodeid):
    global BROWSER
    html=BROWSER.DOM.getOuterHTML(nodeId=nodeid)
    return html["result"]["outerHTML"]    

def RunJS(expression):
    global BROWSER
    res=BROWSER.Runtime.evaluate(expression=expression, returnByValue=True)
    res = res["result"]
    if "exceptionDetails" in res:
        raise Exception(res["exceptionDetails"]["exception"]["description"])
    elif "value" in res["result"]:
        res = res["result"]["value"]
    return res

def CaptureScreenshot(path):
    global BROWSER
    res=BROWSER.Page.captureScreenshot()
    if res:
        saveBase64File(path, res["result"]["data"])

def WaitMessage(timeout=None):
    global BROWSER
    message=BROWSER.wait_message(timeout)
    return message    

def WaitEvent(event="Page.frameStoppedLoading", timeout=60):
    global BROWSER
    event,messages=BROWSER.wait_event(event, timeout)
    return messages

def FilterEventOnloaded(event):
    messages = WaitEvent("Page.frameStoppedLoading")
    return list(filter(lambda x: "method" in x and x["method"] == event, messages))

def ClearBrowserCache():
    global BROWSER
    BROWSER.Network.clearBrowserCache()
    
def ClearBrowserCookies():
    global BROWSER
    BROWSER.Network.clearBrowserCookies()
    
def deleteBrowserCookies(name, url=None, domain=None, path=None):
    global BROWSER
    BROWSER.Network.deleteCookies(name=name, url=url, domain=domain, path=path)
    
def getBrowserAllCookies():
    global BROWSER
    return BROWSER.Network.getAllCookies()

def GetUrlsCookies(urls=None):
    global BROWSER
    if urls:
        return BROWSER.Network.getCookies(urls=urls)
    else:
        return BROWSER.Network.getCookies()

def GetResponseBody(requestId):
    global BROWSER
    return BROWSER.Network.getResponseBody(requestId=requestId)
        
def GetRequestPostData(requestId):
    global BROWSER
    return BROWSER.Network.getRequestPostData(requestId=requestId)

def SetCookie(name,value,url,domain=None,path=None):
    global BROWSER
    return BROWSER.Network.setCookie(name=name,value=value,url=url,domain=domain,path=path)

def SetCookies(cookies):    
    global BROWSER
    BROWSER.Network.setCookie(cookies)
    
def ChangeUserAgent(userAgent):
    global BROWSER
    BROWSER.Network.setUserAgentOverride(userAgent=userAgent)

def SaveBase64File(path, base64code):
    f = open(path, 'wb')
    f.write(base64.b64decode(base64code))
    f.close()
    return True

def FetchBrowserFileByUrl(reg, path):
    ReloadPage()
    message=FilterEventOnloaded("Network.requestWillBeSent")
    data = list(filter(lambda x: "method" in x and x["method"] == "Network.requestWillBeSent" and reg in x["params"]["request"]["url"], message))
    data = data[0]["params"]["requestId"] if len(data) > 0 else None
    if data:
        data=GetResponseBody(data)
        if "base64Encoded" in data["result"] and data["result"]["base64Encoded"]:
            return SaveBase64File(path, data["result"]["body"])
    return False
            
    
# easyBrowser()
# goUrl("https://www.baidu.com/")
# fetchBrowserFileByUrl("logo_top_86d58ae1.png","d:\\aaa.png")

# captureScreenshot("d:\\aa.png")
# searchId=BROWSER.DOM.performSearch(query="li",includeUserAgentShadowDOM=False)
# print(searchId)
# searchId=BROWSER.DOM.getSearchResults(searchId=searchId["result"]["searchId"],fromIndex=0,toIndex=searchId["result"]["resultCount"])
# print(searchId)
# searchId=BROWSER.DOM.pushNodeByPathToFrontend(path="//li/text()")
# print(searchId)
# print(get_tabs())
# go_url("https://forum.uibot.com.cn/")
# wait_event()
# bind_browser()
# go_url("https://daypc.vzsite.top/login.php")
# nodeid=querySelector("li.top_3")
# domid=runJS('''(function(){return "111"})()''')
# print(domid)
# domid=runJS('''111''')
# print(type(domid))
# print(domid)
# domid=runJS('''true''')
# print(type(domid))
# print(domid)
# domid=runJS('''"true"''')
# print(type(domid))
# print(domid)
# domid=runJS('''["1"]''')
# print(type(domid))
# print(domid)
# domid=runJS('''"{'a':1}"''')
# print(type(domid))
# print(domid)
# domid=BROWSER.DOM.getDocument()
# print(domid)
# domid=domid["result"]["root"]["nodeId"]
# print(domid)
# nodeid=BROWSER.DOM.querySelectorAll(nodeId=domid,selector="a")
# print(nodeid)
# nodeid=nodeid["result"]["nodeIds"]
# print(nodeid)
# print(nodeid)
# html=getHTML(nodeid)
# print(html)
# html=getAttributes(nodeid)
# print(html)
# BROWSER.DOM.setAttributeValue(nodeId=nodeid,name="value",value="111111")
# nodeid=BROWSER.DOM.querySelector(nodeId=domid,selector="#login_box > div:nth-child(3) > div > input")
# nodeid=BROWSER.DOM.querySelector(nodeId=domid,selector="#login_box > div:nth-child(4) > div > input")
# 
# messages = filter_event_onloaded("Page.frameStoppedLoading")
# 
# 
# print(messages)

# print(get_tab_info("5ADC94CBC4D7FC796E9C8E806FCC5E2B"))
# active_tab("7B6F61BA4B5FBC3DDF07A6D518130A91")
# close_tab("7B6F61BA4B5FBC3DDF07A6D518130A91")
# create_tab()
# create_tab("https://www.baidu.com")
# create_tab()
# go_url("https://forum.uibot.com.cn/")
# get_all_send("https://www.baidu.com")
# print(get_tabs())
# print(find_tab(title="新标签页",url="newtab"))
# close_browser()
