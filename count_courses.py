# 可视化操作选课

import json
import re
import eel
import requests

url = "courses.txt"
cookies = "JSESSIONID=CDEC84D302F76E12C3F9FDC26966558F; route=eed9533f13fb04547b53b5f85861e0fc"

arr = []


class Course:
    def __init__(self, xuanke_id, tuike_id, name, details, arr, kind, flag):
        self.xuanke_id = xuanke_id
        self.tuike_id = tuike_id
        self.name = name
        self.arr = arr
        self.detail = details
        self.kind = kind
        self.flag = flag

    def check_time(self, day, time):
        return self.arr[day][time] == 1

    def to_string(self):
        print(f'选课id={self.xuanke_id}, 退课id={self.tuike_id}, name={self.name}, details={self.detail}')


def get_date_info(detail, dates_arr):
    patten = re.compile("星期[一二三四五六]第\d+-\d+节")
    s = patten.findall(detail)

    def func(str_):
        if str_ == '一':
            return 1
        elif str_ == '二':
            return 2
        elif str_ == '三':
            return 3
        elif str_ == '四':
            return 4
        elif str_ == '五':
            return 5
        elif str_ == '六':
            return 6

    for k in s:
        day = func(re.compile("[一二三四五六]").findall(k)[0])
        tmp = re.compile("\d+-\d+").findall(k)[0]
        inx = tmp.index('-')
        (begin, end) = (tmp[:inx], tmp[inx + 1:])
        for i in range(int(begin), int(end) + 1):
            dates_arr[day][i] = 1


def find_course_from_time(day, time, courses):
    res = ""
    for i in courses:
        if i.check_time(day, time):
            res += i.name + '\n'
    return res


def get_time_from_course(course_name, courses, date):
    flag = False
    for c in courses:
        if c.name.strip() == course_name.strip():
            flag = True
            array_ = c.arr
            x = []
            y = []
            for i in range(len(array_)):
                for j in range(len(array_[i])):
                    if array_[i][j] == 1:
                        if date[i][j] == 1:
                            return False
                        x.append(i)
                        y.append(j)
            for i in range(len(x)):
                date[x[i]][y[i]] = 1
    return flag


def get_course_by_type(kind, flag, courses):
    res = []
    for course in courses:
        if (course.kind == kind or kind == 'all') and (course.flag == flag or flag == 'all' or flag == 'selected'):
            res.append(course)
    return res


def read_file(url):
    courses = []
    with open(url, "r") as f:
        for line in f:
            if line == '!==!\n':
                continue
            id_flag = line.find("?")
            ids = line[:id_flag].split(',')
            idx = line.find("$")
            temp = line[idx + 1:]
            flag = temp[1:temp.find(',')]
            kind = temp[temp.find(',') + 1:len(temp) - 2]
            line = line[id_flag + 1:idx]
            line = ' '.join(line.split())
            name = line[0:line.find('@')]
            details = line[len(name): len(line)]
            date = [[] for i in range(7)]
            for i in date:
                for j in range(12):
                    i.append(0)
            get_date_info(details, date)
            course = Course(ids[0], ids[1], name, details, date, kind, flag)
            courses.append(course)
            course.to_string()
    return courses


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
    return obj


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
    return obj


Courses = read_file(url)


@eel.expose
def test1(row, col, kind, flag):
    courses = get_course_by_type(kind, flag, Courses)
    return find_course_from_time(row, col, courses)


@eel.expose
def test2(course_list):
    courses = course_list.split(',')
    valid = []
    date = [[] for i in range(7)]
    for i in date:
        for j in range(12):
            i.append(0)

    for c in courses:
        if get_time_from_course(c, Courses, date):
            valid.append(c)
    data = {
        'valid': valid,
        'date': date
    }
    return data


@eel.expose
def add_courses(course_list):
    courses = course_list.split(',')
    res = []
    for c in courses:
        idx = c.find('?')
        (name, xkxs) = (c[:idx], c[idx + 1:])
        print(name, xkxs)
        for cc in Courses:
            if cc.name.strip() == name.strip():
                res.append(add_gouwuche(cookies, cc.xuanke_id, int(xkxs.strip())))
    return res


@eel.expose
def remove_courses(course_list):
    courses = course_list.split(',')
    res = []
    for c in courses:
        for cc in Courses:
            if cc.name.strip() == c.strip():
                res.append(tui_ke(cookies, cc.tuike_id))
    return res


if __name__ == '__main__':
    eel.init('page')
    eel.start('page.html')
