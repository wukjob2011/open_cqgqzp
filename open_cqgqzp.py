import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import openpyxl

if __name__ == "__main__":

    # 发起请求获取网页内容
    url = "http://gzw.cq.gov.cn/gqzp/"
    response = requests.get(url)
    content = response.content

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(content, "html.parser")

    # 定位公告列表
    notice_list = soup.select(".tab-item")
    today = datetime.date.today()

    updates = []
    # 定位公告列表
    found_updates = False
    for notice in notice_list:
        title = notice.a.text.strip()  # 提取公告标题
        link = urljoin(url, notice.a["href"])  # 提取公告超链接
        date_str = notice.span.text.strip()  # 提取公告日期
        responseDe = requests.get(link)
        content2 = responseDe.content
        flag2 = BeautifulSoup(content2, "html.parser").text.__contains__("计算机")

        # 将日期字符串转换为日期对象，并比较日期部分
        notice_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if notice_date == today and flag2:

            updates.append([title, link, date_str])
            found_updates = True

    df = pd.DataFrame(updates, columns=["标题", "超链接", "日期"])
    # 将每天更新的重庆国企招聘放到updates表中
    original_data = pd.read_excel('updates.xlsx')
    save_data = original_data._append(df)
    save_data.to_excel("updates.xlsx", index=False)

    if len(updates) > 0:
        print("已将更新信息保存到 updates.xlsx")
    else:
        print("当前无更新")
