import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# 定义打开网页、获取数据和保存到Excel的功能

def open_and_scrape():
    # 初始化 WebDriver
    driver = webdriver.Chrome()

    # 打开目标网页
    driver.get("http://spi.mee.gov.cn:8081/status-monitor/#/status-monitor")
    
    # 等待网页加载，具体时间可以根据网络速度调整
    time.sleep(10)
    
    # 这里模拟复制网页上的数据。你可能需要根据网页的结构来调整定位方式。
    # 示例：假设网页上有一个table，数据保存在table的tr标签中。
    
    try:
        table = driver.find_element(By.XPATH, "//table")  # 需要根据实际网页调整
        rows = table.find_elements(By.TAG_NAME, "tr")

        # 提取数据并存储在列表中
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            data.append(cols)

        # 将数据保存到Excel文件
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())  # 使用当前时间戳创建sheet名称
        df = pd.DataFrame(data)
        
        # 保存数据到Excel，添加新sheet
        with pd.ExcelWriter('data.xlsx', engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=timestamp, index=False)

    except Exception as e:
        print("错误:", e)

    finally:
        driver.quit()

# 设置定时任务：每天定时运行
schedule.every().day.at("09:00").do(open_and_scrape)  # 每天上午9点执行

# 循环运行任务
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次
