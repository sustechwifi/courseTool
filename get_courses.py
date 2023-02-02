# 从选课系统爬取所有课程，保存到courses.txt中
# courses.txt中数据格式为：
# 选课ID,退课ID?name@教师名 详细信息 $(课程分类代号,课程类型)
# EC7859D84807FE18E053CA0412AC2CF7,F3AE6055F2223193E053CA0412AC0C89?CS305-计算机网络-01班-英文-2组	@主任务: 李卓钊 上课信息: 1-16周,星期三第5-6节 三教208 课内实验: 王晴 上课信息: 1-16周,星期三第7-8节 三教504机房  $(MR,selected)
# 已选择课程与可选择课程直接以 '!==!' 行隔开

import requests
import json
import re

cookies = "JSESSIONID=CDEC84D302F76E12C3F9FDC26966558F; route=eed9533f13fb04547b53b5f85861e0fc"
body = {
    "p_pylx": '1',
    "mxpylx": '1',
    "p_sfgldjr": '0',
    "p_sfredis": '0',
    "p_sfsyxkgwc": '0',
    "p_xktjz": '',
    "p_chaxunxh": '',
    "p_gjz": '',
    "p_skjs": '',
    "p_xn": "2022-2023",
    "p_xq": '2',
    "p_xnxq": '2022-20232',
    "p_dqxn": "2022-2023",
    "p_dqxq": '1',
    "p_dqxnxq": "2022-20231",
    "p_xkfsdm": 'bxxk',
    "p_xiaoqu": '',
    "p_kkyx": '',
    "p_kclb": '',
    "p_xkxs": '',
    "p_id": '',
    "p_sfhlctkc": '0',
    "p_sfhllrlkc": '0',
    "p_kxsj_xqj": '',
    "p_kxsj_ksjc": '',
    "p_kxsj_jsjc": '',
    "p_kcdm_js": '',
    "p_kcdm_cxrw": '',
    "p_kc_gjz": '',
    "p_xzcxtjz_nj": '',
    "p_xzcxtjz_yx": '',
    "p_xzcxtjz_zy": '',
    "p_xzcxtjz_zyfx": '',
    "p_xzcxtjz_bj": '',
    "p_sfxsgwckb": '1',
    "p_skyy": '',
    "p_chaxunxkfsdm": '',
    "pageNum": '1',
    "pageSize": '100'
}
kinds = ['bxxk', 'xxxk', 'kzyxk', 'zynknjxk', 'cxxk']


def format_string(xuanke_id, tuike_id, course_name, details, label, flag):
    return f'{xuanke_id},{tuike_id}?' + course_name + "\t@" + test_regex(details) + f' $({label},{flag})' + "\n"


def get_my_course(cookie):
    url = 'https://tis.sustech.edu.cn/Xsxk/queryKxrw'

    para = 'p_pylx=1&mxpylx=1&p_sfgldjr=0&p_sfredis=0&p_sfsyxkgwc=0&p_xktjz=&p_chaxunxh=&p_gjz=&p_skjs=&p_xn=2022-2023&p_xq=2&p_xnxq=2022-20232&p_dqxn=2022-2023&p_dqxq=1&p_dqxnxq=2022-20231&p_xkfsdm=bxxk&p_xiaoqu=&p_kkyx=&p_kclb=&p_xkxs=&p_id=&p_sfhlctkc=0&p_sfhllrlkc=0&p_kxsj_xqj=&p_kxsj_ksjc=&p_kxsj_jsjc=&p_kcdm_js=&p_kcdm_cxrw=&p_kc_gjz=&p_xzcxtjz_nj=&p_xzcxtjz_yx=&p_xzcxtjz_zy=&p_xzcxtjz_zyfx=&p_xzcxtjz_bj=&p_sfxsgwckb=1&p_skyy=&p_chaxunxkfsdm=&pageNum=3&pageSize=100'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)

    obj = json.loads(response.text)

    my_course = obj["yxkcList"]

    with open("courses.txt", "a") as f:
        for i in my_course:
            tmp = format_string(i['rwid'], i['id'], i['kcdm'] + '-' + i['rwmc'], i['kcxx'], i['kclbmc_en'], 'selected')
            print(tmp, end='')
            f.write(tmp)
        f.write("!==!\n")
    return my_course


def get_courses_by_page(cookie, pageNum, pageSize, type):
    url = 'https://tis.sustech.edu.cn/Xsxk/queryKxrw'

    para = f'p_pylx=1&mxpylx=1&p_sfgldjr=0&p_sfredis=0&p_sfsyxkgwc=0&p_xktjz=&p_chaxunxh=&p_gjz=&p_skjs=&p_xn=2022-2023&p_xq=2&p_xnxq=2022-20232&p_dqxn=2022-2023&p_dqxq=1&p_dqxnxq=2022-20231&p_xkfsdm={type}&p_xiaoqu=&p_kkyx=&p_kclb=&p_xkxs=&p_id=&p_sfhlctkc=0&p_sfhllrlkc=0&p_kxsj_xqj=&p_kxsj_ksjc=&p_kxsj_jsjc=&p_kcdm_js=&p_kcdm_cxrw=&p_kc_gjz=&p_xzcxtjz_nj=&p_xzcxtjz_yx=&p_xzcxtjz_zy=&p_xzcxtjz_zyfx=&p_xzcxtjz_bj=&p_sfxsgwckb=1&p_skyy=&p_chaxunxkfsdm=&pageNum={pageNum}&pageSize={pageSize}'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }
    response = requests.post(url=url, params=para, headers=header)
    obj = json.loads(response.text)
    courses_info = obj["kxrwList"]
    return courses_info["list"]


def get_all_course(cookie, pageSize, type):
    url = 'https://tis.sustech.edu.cn/Xsxk/queryKxrw'

    para = f'p_pylx=1&mxpylx=1&p_sfgldjr=0&p_sfredis=0&p_sfsyxkgwc=0&p_xktjz=&p_chaxunxh=&p_gjz=&p_skjs=&p_xn=2022-2023&p_xq=2&p_xnxq=2022-20232&p_dqxn=2022-2023&p_dqxq=1&p_dqxnxq=2022-20231&p_xkfsdm={type}&p_xiaoqu=&p_kkyx=&p_kclb=&p_xkxs=&p_id=&p_sfhlctkc=0&p_sfhllrlkc=0&p_kxsj_xqj=&p_kxsj_ksjc=&p_kxsj_jsjc=&p_kcdm_js=&p_kcdm_cxrw=&p_kc_gjz=&p_xzcxtjz_nj=&p_xzcxtjz_yx=&p_xzcxtjz_zy=&p_xzcxtjz_zyfx=&p_xzcxtjz_bj=&p_sfxsgwckb=1&p_skyy=&p_chaxunxkfsdm=&pageNum=3&pageSize=100'

    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        "cookie": cookie
    }

    response = requests.post(url=url, params=para, headers=header)

    obj = json.loads(response.text)
    courses_info = obj["kxrwList"]
    cnt = courses_info["total"]

    print(f"total course: {cnt}")
    with open("courses.txt", "a") as f:
        for j in range(int(cnt / pageSize) + 1):
            course_list = get_courses_by_page(cookie, j + 1, pageSize, type)
            for i in course_list:
                tmp = format_string(i['id'], 'null', i['kcdm'] + '-' + i['rwmc'], i['kcxx'], i['kclbmc_en'], type)
                print(tmp, end='')
                f.write(tmp)


def run():
    with open("courses.txt", "w") as f:
        f.write('')
    get_my_course(cookies)
    for i in kinds:
        get_all_course(cookies, 100, i)


def test_regex(str):
    patten = re.compile(">(?![<\s]).*?</")
    res = patten.findall(str)
    ans = ''
    for i in res:
        ans += i[1:len(i) - 2] + " "
    return ans


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run()
