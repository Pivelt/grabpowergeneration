import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import schedule
import time

def fetch_data():
    url = 'http://spi.mee.gov.cn:8081/status-monitor/#/status-monitor'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.prettify()  # 或者根据需要提取特定数据
    
    # 将数据保存到 Excel 文件
    wb = Workbook()
    ws = wb.active
    ws.append([data])
    wb.save('data.xlsx')

schedule.every().day.at("10:30").do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
