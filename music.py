import requests
import json
import pygame
import time

def get_spotify_oauth_token(client_id, client_secret):
    """
    获取QQ音乐API的歌曲链接。
    """
    # 输入你的QQ音乐API参数，客户端ID，客户端密钥，等等。你可能需要手动从请求头中提取这些信息。
    query = '周杰伦'
    post_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'

    # 构造请求头
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Charset": "UTF-8",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
        "Host": "u.y.qq.com"
    }
    post_data = {
        "comm": {
            "_channelid": "19",
            "_os_version": "6.2.9200-2",
            "authst": "Q_H_L_5tvGesDV1E9ywCVIuapBeYL7IYKKtbZErLj5HeBkyXeqXtjfQYhP5tg",
            "ct": "19",
            "cv": "1873",
            "guid": "B69D8BC956E47C2B65440380380B7E9A",
            "patch": "118",
            "psrf_access_token_expiresAt": 1697829214,
            "psrf_qqaccess_token": "A865B8CA3016A74B1616F8919F667B0B",
            "psrf_qqopenid": "2AEA845D18EF4BCE287B8EFEDEA1EBCA",
            "psrf_qqunionid": "6EFC814008FAA695ADD95392D7D5ADD2",
            "tmeAppID": "qqmusic",
            "tmeLoginType": 2,
            "uin": "961532186",
            "wid": "0"
        },
        "music.search.SearchCgiService": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "grp": 1,
                "num_per_page": 20,
                "page_num": 1,
                "query": query,
                "remoteplace": "txt.newclient.history",
                "search_type": 0,
                "searchid": "6254988708H54D2F969E5D1C81472A98609002"
            }
        }
    }
    
    response = requests.post(post_url, json=post_data, headers=headers)
    json_data = response.json()
    
    # 获取结果
    song_info = json_data["music.search.SearchCgiService"]["data"]["body"]["song"]["list"]
    if not song_info:
        print("未找到相关歌曲")
        return None
    
    # 选择第一首歌曲的播放链接
    song_mid = song_info[0]["mid"]
    song_url = get_mp3_data(song_mid)
    
    return song_url


def get_mp3_data(song_mid):
    """
    根据歌曲mid获取歌曲播放URL
    """
    url = f"https://i.y.qq.com/v8/playsong.html?ADTAG=ryqq.songDetail&songmid={song_mid}&songid=0&songtype=0"
    html_str = requests.get(url).text
    # 提取JSON数据
    json_str = html_str.split("window.__ssrFirstPageData__ =")[1].split("</script>")[0]
    json_data = json.loads(json_str)
    
    song_url = json_data['songList'][0]['url']  # 获取播放链接
    return song_url


def play_music(song_url):
    """
    使用pygame播放音乐
    """
    pygame.mixer.init()
    pygame.mixer.music.load(song_url)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # 保证程序继续运行，直到歌曲播放完


def main():
    # 获取歌曲播放链接
    song_url = get_spotify_oauth_token(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")
    
    if song_url:
        print("正在播放音乐...")
        play_music(song_url)
    else:
        print("未能获取到音乐URL")


if __name__ == "__main__":
    main()