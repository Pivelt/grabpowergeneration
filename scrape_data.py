import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options

# 设置Chrome的选项
options = Options()
options.headless = True  # 启动无头模式，不显示浏览器界面

def open_and_scrape():
    # 初始化 WebDriver
    driver = webdriver.Chrome(options=options)

    # 打开目标网页
    driver.get("http://spi.mee.gov.cn:8081/status-monitor/#/status-monitor")
    
    # 等待网页加载，具体时间可以根据网络速度调整
    time.sleep(10)
    
    # 抓取数据，假设数据在table中
    try:
        # 找到包含数据的table
        table = driver.find_element(By.XPATH, "//table")  # 根据实际网页的结构修改XPath
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # 提取每行数据
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            data.append(cols)

        # 获取当前时间戳，作为Excel的sheet名称
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        df = pd.DataFrame(data)
        
        # 将数据保存到Excel文件，新的sheet
        with pd.ExcelWriter('data.xlsx', engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=timestamp, index=False)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

# 设置定时任务：每小时执行一次
schedule.every().hour.do(open_and_scrape)

# 循环运行任务
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次
