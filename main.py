# _*_coding:utf-8_*_
# author:gq
import re
import urllib2
import json
import sys
import os
import LogUtil

# 运行配置
TOP_DOWNLOAD_NUMBER = 2  # 搜索下载排名多少的歌曲，2就下载前两个,最大只能设置20
SEARCH_KEYWORDS = [
    "刘德华",
]

def search_music(song_name):
    # print "搜索的歌名：" + song_name.encode("utf-8")
    header = {
        "authority": "c.y.qq.com",
        "method": "GET",
        "path": "/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song"
                "&searchid=62072551069125820&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=%s"
                "&g_tk=5381&jsonpCallback=searchCallbacksong2143&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8"
                "&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0" % song_name,
        "scheme": 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    # url地址可以浏览器分析获取，主要是&w参数
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song' \
          '&searchid=62072551069125820&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=%s' \
          '&g_tk=5381&jsonpCallback=searchCallbacksong&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8' \
          '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' % song_name
    LogUtil.i('Searching:' + url + '\n')
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason, '\n'
        html = None
    return html


def parseResponse(html):
    # 解析searchCallbacksong(),括号中的内容
    result = re.findall(".*searchCallbacksong\((.*)\).*", html)
    json_str = result[0]
    LogUtil.d("reponse解析的json字符串：".decode("gbk").encode("utf-8") + json_str)

    jsonObject = json.loads(json_str)  # 转化为python dict
    # print type(jsonObject)

    # print jsonObject["data"]["song"]["list"]
    for index, item in enumerate(jsonObject['data']['song']['list']):
        if ((index + 1) > TOP_DOWNLOAD_NUMBER):
            LogUtil.d("设置最大下载的数量为：".decode("gbk").encode("utf-8") + str(TOP_DOWNLOAD_NUMBER))
            break;
        elif(TOP_DOWNLOAD_NUMBER>=1):
            media_mid = item["file"]["media_mid"]
            mid = item["mid"]
            if TOP_DOWNLOAD_NUMBER == 1 :
                save_filename = item["name"] + ".m4a"
            else:
                save_filename = item["name"] + "-" + str(index + 1) + ".m4a"
            LogUtil.d(str(index) + " media_mid: " + media_mid + "; mid:" + mid + "; name:" + save_filename)
            get_vkey(mid, media_mid, save_filename)


def get_vkey(mid, media_mid, save_filename):
    header = {
        "authority": "c.y.qq.com",
        "method": "GET",
        "path": "/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback"
                "&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq"
                "&needNewCode=0&cid=205361747&callback=MusicJsonCallback2346403861098214&uin=0&songmid=%s"
                "&filename=C400%s.m4a&guid=5789371178" % (mid, media_mid),
        "scheme": 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        "referer": "https://y.qq.com/portal/player.html",
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    # url地址可以浏览器分析获取，主要是&w参数
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback' \
          '&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' \
          '&cid=205361747&callback=MusicJsonCallback&uin=0&songmid=%s&filename=C400%s.m4a' \
          '&guid=5789371178' % (mid, media_mid)

    LogUtil.i('get vkey :' + url + '\n')
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
        result = re.findall(".*MusicJsonCallback\((.*)\).*", html)
        json_str = result[0]
        LogUtil.d("get_vkey解析的字符串为：".decode("gbk").encode("utf-8") + json_str)

        jsonObject = json.loads(json_str)  # 转化为python dict
        filename = jsonObject["data"]["items"][0]["filename"]
        songmid = jsonObject["data"]["items"][0]["songmid"]
        vkey = jsonObject["data"]["items"][0]["vkey"]
        LogUtil.d("filename=" + filename + "  ;songmid:" + songmid + "   ;vkey:" + vkey)

        download_m4a(filename, vkey, save_filename)
    except urllib2.URLError as e:
        print 'vkey error:', e.reason, '\n'
        html = None
    return html


def download_m4a(filename, vkey, save_filename):
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'cache-control': 'max-age=0',
        "Host": "dl.stream.qqmusic.qq.com",
        "Range": "bytes=0-",
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    # url地址可以浏览器分析获取，主要是&w参数
    url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=5789371178&uin=0&fromtag=66' % (filename, vkey)
    LogUtil.i('Downloading m4a :' + url + '\n')
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
        write_file(save_filename, html)
    except urllib2.URLError as e:
        print 'm4a error:', e.reason, '\n'
        html = None
    return html


def write_file(save_filename, data):
    if not os.path.exists(path):
        os.makedirs(path)

    save_filename = path + save_filename
    with open(save_filename, "wb") as code:
        code.write(data)

path = sys.path[0] + os.sep + "Music" + os.sep
if __name__ == "__main__":
    for keyword in SEARCH_KEYWORDS:
        keyword = keyword.decode("gbk").encode("utf-8")
        html = search_music(keyword)
        parseResponse(html)

    print "完成!文件的保存路径：".decode("gbk").encode("utf-8") + path