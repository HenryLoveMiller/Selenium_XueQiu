import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

def scrape_xueqiu_posts():
    print("--- Starting scrape_xueqiu_posts function ---")
    driver = None
    try:
        print("Initializing undetected Chrome options...")
        options = uc.ChromeOptions()
        # options.add_argument('--headless')  # 可选，如需无头模式可打开
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"')

        print("Attempting to start undetected_chromedriver.Chrome...")
        driver = uc.Chrome(options=options)
        print("--- Undetected Chrome webdriver started successfully! ---")

        driver.set_window_size(1920, 1080)
        initial_url = "https://xueqiu.com/u/8740756364"
        all_posts = []

        print(f"Navigating to initial URL: {initial_url}")
        driver.get(initial_url)

        # 等待页面跳转完成
        time.sleep(5)  # 等待5秒以确保页面跳转完成
        final_url = driver.current_url
        print(f"Final URL after redirection: {final_url}")

        # 检查最终页面的结构
        print("Waiting for timeline item to be present...")
        wait = WebDriverWait(driver, 30)  # 增加等待时间
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "timeline__item")))
        print("Timeline item found. Waiting a bit more for dynamic content.")
        time.sleep(3)  # 等待动态内容加载

        # 增加滚动操作
        for i in range(5):  # 增加滚动次数
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Executing scroll down #{i+1}...")
            time.sleep(random.uniform(2, 4))  # 增加随机等待时间

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')
        timeline_items = soup.find_all('article', class_='timeline__item')
        print(f"Successfully located {len(timeline_items)} posts.")

        for item in timeline_items[:3]:
            content_element = item.select_one('.timeline__item__content .content--description > div')
            content = content_element.get_text(strip=True, separator='\n') if content_element else "N/A"
            time_element = item.find('a', class_='date-and-source')
            timestamp = time_element.get_text(strip=True) if time_element else "N/A"
            link = "https://xueqiu.com" + time_element['href'] if time_element and time_element.has_attr('href') else "N/A"

            post_data = {'content': content, 'timestamp': timestamp, 'link': link}
            all_posts.append(post_data)

        return all_posts

    except TimeoutException as e:
        error_message = f"TimeoutException: The element was not found in time. Details: {e.msg}"
        print(error_message)
        return {"error": "A TimeoutException occurred", "details": e.msg}
    except WebDriverException as e:
        error_message = f"WebDriverException: An error occurred with the browser or driver. Details: {e.msg}"
        print(error_message)
        return {"error": "A WebDriverException occurred", "details": e.msg}
    except Exception as e:
        error_message = f"An unexpected error occurred: {type(e).__name__} - {str(e)}"
        print(error_message)
        return {"error": "An unexpected error occurred", "details": str(e)}
    finally:
        if driver:
            print("Closing webdriver.")
            driver.quit()

# 示例调用
if __name__ == '__main__':
    data = scrape_xueqiu_posts()
    print(data)
