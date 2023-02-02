# 以命令行进行选课/退课操作

import requests
import json

# 从浏览器中寻找本人的教务系统的登录cookie
cookies = "JSESSIONID=CDEC84D302F76E12C3F9FDC26966558F; route=eed9533f13fb04547b53b5f85861e0fc"


def add_gouwuche(cookie, p_id, xkxs):
    url = 'https://tis.sustech.edu.cn/Xsxk/addGouwuche'

    para = f'p_pylx=1&mxpylx=1&p_sfgldjr=0&p_sfredis=0&p_sfsyxkgwc=0&p_xktjz=rwtjzyx&p_chaxunxh=&p_gjz=&p_skjs=&p_xn=2022-2023&p_xq=2&p_xnxq=2022-20232&p_dqxn=2022-2023&p_dqxq=1&p_dqxnxq=2022-20231&p_xkfsdm=kzyxk&p_xiaoqu=&p_kkyx=&p_kclb=&p_xkxs={xkxs}&p_id={p_id}&p_sfhlctkc=0&p_sfhllrlkc=0&p_kxsj_xqj=&p_kxsj_ksjc=&p_kxsj_jsjc=&p_kcdm_js=&p_kcdm_cxrw=&p_kc_gjz=&p_xzcxtjz_nj=&p_xzcxtjz_yx=&p_xzcxtjz_zy=&p_xzcxtjz_zyfx=&p_xzcxtjz_bj=&p_sfxsgwckb=1&p_skyy=&p_chaxunxkfsdm=&pageNum=3&pageSize=100'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)
    obj = json.loads(response.text)
    print(obj)


def tui_ke(cookie, p_id):
    url = "https://tis.sustech.edu.cn/Xsxk/tuike"

    para = f'p_pylx=1&mxpylx=1&p_sfgldjr=0&p_sfredis=0&p_sfsyxkgwc=0&p_xktjz=rwtjzyx&p_chaxunxh=&p_gjz=&p_skjs=&p_xn=2022-2023&p_xq=2&p_xnxq=2022-20232&p_dqxn=2022-2023&p_dqxq=2&p_dqxnxq=2022-20232&p_xkfsdm=yixuan&p_xiaoqu=&p_kkyx=&p_kclb=&p_xkxs=1&p_id={p_id}&p_sfhlctkc=0&p_sfhllrlkc=0&p_kxsj_xqj=&p_kxsj_ksjc=&p_kxsj_jsjc=&p_kcdm_js=&p_kcdm_cxrw=&p_kc_gjz=&p_xzcxtjz_nj=&p_xzcxtjz_yx=&p_xzcxtjz_zy=&p_xzcxtjz_zyfx=&p_xzcxtjz_bj=&p_sfxsgwckb=1&p_skyy=&p_chaxunxkfsdm=&pageNum=1&pageSize=17'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)
    obj = json.loads(response.text)
    print(obj)


def add_gouwuche_with_para(cookie, para):
    url = 'https://tis.sustech.edu.cn/Xsxk/addGouwuche'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)
    obj = json.loads(response.text)
    print(obj)


def tui_ke_with_para(cookie, para):
    url = "https://tis.sustech.edu.cn/Xsxk/tuike"

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)
    obj = json.loads(response.text)
    print(obj)


def 选课(courseID_list, factors_list):
    for i in range(len(courseID_list)):
        add_gouwuche(cookies, courseID_list[i], factors_list[i])


def 退课(courseID_list):
    for i in range(len(courseID_list)):
        tui_ke(cookies,courseID_list[i])


# 使用前更新cookie 和 courses.txt
if __name__ == '__main__':
    courses = ['EED0F6BD1CB291B8E053CA0412ACA86A', 'ED7EEEC36C4B4AB3E053CA0412AC3AE3']
    points = [1, 1]
    选课(courses, points)
    退课(courses)
