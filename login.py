from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import time

# 1. ChromeDriver 자동 설치 + 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2. 네이버 로그인 페이지 접속
driver.get("https://nid.naver.com/nidlogin.login")

# 3. ID 입력창 나타날 때까지 최대 10초 대기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "id"))
)

# 4. 클립보드에 ID 복사
pyperclip.copy("pmy98")

# 5. ID 입력창 클릭
id_box = driver.find_element(By.ID, "id")
id_box.click()
time.sleep(0.5)  # 클릭 후 잠깐 기다리기

# 6. Ctrl + V로 붙여넣기
id_box.send_keys(Keys.CONTROL, 'v')
time.sleep(0.5)

# 7. 클립보드에 PW 복사
pyperclip.copy("leopold05#@!")

# 8. PW 입력창 클릭
pw_box = driver.find_element(By.ID, "pw")
pw_box.click()
time.sleep(0.5)

# 9. Ctrl + V로 붙여넣기
pw_box.send_keys(Keys.CONTROL, 'v')
time.sleep(0.5)

# 10. 로그인 버튼 클릭 가능할 때까지 기다림
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "log.login"))
)
# 11. 로그인 버튼 클릭
driver.find_element(By.ID, "log.login").click()

# 12. 수동 캡챠 풀기
input("캡챠를 풀고 엔터를 누르세요.")

# 13. (캡챠 다 풀었으면) 이후에 필요한 작업 진행
time.sleep(2)

# 예시) 브라우저 종료 안함
# driver.quit()


# 12. 로그인 후 2초 대기
time.sleep(2)

# 13. 브라우저 종료는 하지 않음 (driver.quit() 없음)
