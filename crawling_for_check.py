import time
from datetime import datetime
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def crawl_comments(keyword):
    """
    종목명을 검색해서 토스증권 커뮤니티 탭 댓글을 수집하여 콘솔에 출력합니다.
    """
    # 1. 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 ... Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    # 2. 토스증권 메인 페이지 접속
    driver.get("https://tossinvest.com/")
    time.sleep(1)

    # 3. 검색창 버튼 클릭
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.u09klc0")))
    search_button.click()
    time.sleep(1)

    # 4. 종목명 입력 → ENTER
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input._1x1gpvi6")))
    search_input.send_keys(keyword)
    time.sleep(1)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)

    # 5. 종목 코드 추출
    current_url = driver.current_url
    stock_code = current_url.split("/")[-1]
    company_name = keyword
    print(f"🔍 종목 코드 추출: {stock_code}")

    # 6. 커뮤니티 탭 클릭 (수정된 안정적 방식)
    community_tab = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[id*='trigger-community']")
    ))
    community_tab.click()
    time.sleep(2)

    # 7. 댓글 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # ✅ 실제 댓글 span 태그 확인됨
    comments = soup.select("span[class*='tw-'][class*='1sihfl60']")

    print(f"\n📋 {company_name} ({stock_code}) 댓글 수집 결과:")
    for i, c in enumerate(comments, start=1):
        text = c.get_text(strip=True)
        print(f"{i:02d}. {text}")

    driver.quit()


# ✅ 실행
crawl_comments("삼성전자")
