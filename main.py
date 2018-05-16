# _*_coding:utf-8_*_
# author:gq
import re
import urllib2
import json



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
    print 'Downloading:', url, '\n'
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason, '\n'
        html = None
    return html


def searchCallbacksong(e):
    pass
    # for index, item in enumerate(e['data']['song']['list']):
    #     # print index
    #     print item["name"]


def parseResponse(html):
    # 解析searchCallbacksong(),括号中的内容
    result = re.findall(".*searchCallbacksong\((.*)\).*", html)
    json_str = result[0]
    print json_str

    jsonObject = json.loads(json_str)  # 转化为python dict
    # print type(jsonObject)

    # print jsonObject["data"]["song"]["list"]
    for index, item in enumerate(jsonObject['data']['song']['list']):
        media_mid = item["file"]["media_mid"]
        mid = item["mid"]
        print str(index) + " media_mid: " + media_mid + "; mid:" + mid
        get_vkey(mid,media_mid)
        break;

def get_vkey(mid,filename):
    header = {
        "authority": "c.y.qq.com",
        "method": "GET",
        "path": "/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback"
                "&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq"
                "&needNewCode=0&cid=205361747&callback=MusicJsonCallback2346403861098214&uin=0&songmid=%s"
                "&filename=C400%s.m4a&guid=5789371178"%(mid,filename),
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
          '&guid=5789371178'%(mid,filename)
    print 'Downloading vkey :', url, '\n'
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
        print html
        result = re.findall(".*MusicJsonCallback\((.*)\).*", html)
        json_str = result[0]
        print json_str
        jsonObject = json.loads(json_str)  # 转化为python dict
        filename = jsonObject["data"]["items"][0]["filename"]
        songmid = jsonObject["data"]["items"][0]["songmid"]
        vkey = jsonObject["data"]["items"][0]["vkey"]
        print filename
        print songmid
        print vkey

        download_m4a(filename,vkey)
    except urllib2.URLError as e:
        print 'vkey error:', e.reason, '\n'
        html = None
    return html


def download_m4a(filename,vkey):
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
    print 'Downloading m4a :', url, '\n'
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
        with open(filename, "wb") as code:
            code.write(html)
    except urllib2.URLError as e:
        print 'm4a error:', e.reason, '\n'
        html = None
    return html


if __name__ == "__main__":
    # song_name = raw_input(unicode('please input name:', 'utf-8'))
    # song_name = unicode(song_name, 'utf-8')

    song_name = "大约在冬季"
    # song_name = raw_input(unicode('输入歌曲名:', 'utf-8').encode('gbk'))
    # song_name = unicode(song_name, 'gbk').encode('utf-8')
    # print "输入的歌名为：" + song_name.encode("utf-8")
    html = search_music(song_name)
    print html

    # 解析方法1：这个函数会自动的执行返回的html中的searchCallbacksong这个函数
    # exec(html)

    # 解析方法2：通过将数据转化为python对象处理，转成一个dict类型
    parseResponse(html)
