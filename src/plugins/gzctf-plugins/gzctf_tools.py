import requests
import json
import pytz
from datetime import datetime, timezone
from dateutil import parser
from nonebot import get_driver
from nonebot.adapters import Bot
from .config import Config

CONFIG=Config.parse_obj(get_driver().config)
BASECONFIG = CONFIG.BASECONFIG
BASEURL=BASECONFIG['BASEURL'].rstrip('/')
HEADERS={"Content-Type": "application/json"}
LOGINDATA="{"+f'"userName": "{BASECONFIG["GZCTF_USER"]}", "password": "{BASECONFIG["GZCTF_USER_PASS"]}"'+"}"
WEBSESSION=requests.session()
UTC_TIMEZONE = pytz.timezone('UTC')
UTC_PLUS_8_TIMEZONE = pytz.timezone('Asia/Shanghai')

def getContestInfo():
    """
        *** 获取 gzctf 所有比赛详细信息 ***
    """
    global WEBSESSION, HEADERS
    API_CONTEST_URL = BASEURL+f'/api/game/'
    try:
        res = WEBSESSION.get(API_CONTEST_URL, headers=HEADERS)
    except:
        return []
    contestInfo = json.loads(res.text)
    return contestInfo

def checkConfig(config: dict):
    """
        *** 判断 BASECONFIG 是否成立 ***
    """
    return True if config.get("WHITE_LIST") and config.get("ENDPOINT") else False

def parseTime(strTime):
    """
        *** 解析通过 gzctf 平台获取的时间串 ***
    """
    global UTC_TIMEZONE, UTC_PLUS_8_TIMEZONE

    # 如果传入的是整数或长整型（如 1741861800000）
    if isinstance(strTime, (int, float)):
        # 毫秒转秒
        timestamp = strTime / 1000
        date = datetime.fromtimestamp(timestamp, tz=UTC_TIMEZONE)
    else:
        # 字符串形式如 "2025-04-12T12:00:00"
        date = datetime.fromisoformat(strTime[:19])
        date = UTC_TIMEZONE.localize(date)

    date = date.astimezone(UTC_PLUS_8_TIMEZONE)

    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    hour = f"{date.hour:02d}"
    minute = f"{date.minute:02d}"
    second = f"{date.second:02d}"
    nowTime = (year, month, day, hour, minute, second)
    return nowTime

def parse_time_flexibly(time_input):
    if isinstance(time_input, (int, float)):
        # 毫秒转秒，然后加上 UTC 时区
        return datetime.fromtimestamp(time_input / 1000, tz=timezone.utc)
    elif isinstance(time_input, str):
        # 解析 ISO 格式字符串
        return parser.isoparse(time_input)
    else:
        raise ValueError("不支持的时间格式")

def getLogin():
    """
        *** 使用gzctf暴露的api进行登录 ***
    """
    global LOGINDATA, HEADERS, WEBSESSION, BASEURL
    API_LOGIN_URL = BASEURL+"/api/account/login"
    loginRespose=WEBSESSION.post(url=API_LOGIN_URL,data=LOGINDATA,headers=HEADERS)
    # return loginRespose.cookies if loginRespose.ok == True else None

def checkCookieExpired():
    """
        *** 判断会话的cookie有没有到期,如果到期则返回False,否则True ***
    """
    global WEBSESSION
    for cookie in WEBSESSION.cookies:
        if cookie is not None and cookie.name == "GZCTF_Token":
            expire = datetime.fromtimestamp(cookie.expires)
            nowTime = datetime.now()
            if nowTime > expire:
                return False
    return True

def getNoticeById(GAME_ID:str):
    """
        *** 获取gzctf某场比赛的notices消息 ***
    """
    global WEBSESSION, HEADERS, BASEURL
    API_NOTICE_URL = BASEURL+f"/api/game/{GAME_ID}/notices"
    # request = requests.session()
    try:
        res = WEBSESSION.get(API_NOTICE_URL, headers=HEADERS)
    except:
        return []
    allList = json.loads(res.text)
    return allList

def getChallengesById(GAME_ID:str):
    """
        *** 获取gzctf某场比赛中的所有题目, 需要admin权限 ***
    """
    global WEBSESSION, HEADERS, BASEURL
    API_CHALLENGE_URL = BASEURL+f'/api/edit/games/{GAME_ID}/challenges'
    if not checkCookieExpired():
        getLogin()
    try:
        challengeResponse=WEBSESSION.get(url=API_CHALLENGE_URL,headers=HEADERS)
    except:
        return []
    return json.loads(challengeResponse.text)

async def sendMessageTo(bot:Bot, type:str, id:str, message:str):
    """
        *** 直接利用 bot API 发送消息到 '某人/某群' ***
    """
    if type == "user_id" or type == "user":
        try:
            await bot.call_api('send_msg',user_id=id,message=message)
        except Exception as e:
            print(e)
            return False
    elif type == "group_id" or type == "group":
        try:
            await bot.call_api('send_msg',group_id=id,message=message)
        except Exception as e:
            print(e)
            return False
    return True

def getGameMonitored():
    """
        *** 获取被监视比赛的信息 ***
    """
    global CONFIG,BASECONFIG
    CONTESTINFOS=getContestInfo()
    GAMEMONITORED=BASECONFIG.get('GAMEMONITORED') if BASECONFIG.get('GAMEMONITORED') else []
    if GAMEMONITORED:
        GAMEMONITOREDTMP=[]
        for gameId in GAMEMONITORED:
            gameAllowed = [gameInfo for gameInfo in CONTESTINFOS if gameInfo.get("title") == gameId]
            for gameInfo in gameAllowed:
                GAMEMONITOREDTMP.append(gameInfo)
        GAMEMONITORED=GAMEMONITOREDTMP
    else:
        GAMEMONITORED = CONTESTINFOS
    return GAMEMONITORED

def getNowNoticeList(gamemonitored: dict):
    """
        *** 获取被监视比赛的notice ***
    """
    NOWNOTICEDICT={}
    for gameInfo in gamemonitored['data']:
        NOWNOTICEDICT[f"{gameInfo['id']}"]=getNoticeById(f"{gameInfo['id']}")
    return NOWNOTICEDICT