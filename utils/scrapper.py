from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import json
import time
import pandas as pd

# config
CAFE_URL = 'https://cafe.naver.com/mbticafe/'
LOGIN_URL = 'https://nid.naver.com/nidlogin.login'
AUTOSAVE = 100
SAVE_PATH = '../data/raw_data/'

# 저장된 로그인 정보 로드
with open('login.json') as f: login_info = json.load(f)
ID, PW = login_info['id'], login_info['pw']

# 메인 함수
def main(auto_start=True, start_idx=0, num_target=10**6):

    # 수집한 데이터를 파일로 저장
    def save(data):
        data = pd.DataFrame(data, columns=['nickname', 'contents', 'is_article', 'idx'])
        data.to_csv(SAVE_PATH + f'data_{start_idx:06}_{current_idx:06}.csv', index=False)

    # 자동 시작 옵션 선택 시 시작 지점 탐색
    if auto_start: 
        files = os.listdir(SAVE_PATH)
        start_idx = 0 if not files else int(files[-1][-10:-4])

    # 크롬 브라우저를 창에 띄우지 않고 작업 실행
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("headless")
    driver = webdriver.Chrome(options=driver_options)

    # 로그인
    driver.get(LOGIN_URL)
    driver.implicitly_wait(2)
    driver.execute_script('document.getElementsByName("id")[0].value=\"' + ID + '\"')
    driver.execute_script('document.getElementsByName("pw")[0].value=\"' + PW + '\"')
    driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
    time.sleep(2)

    # 데이터 저장할 배열
    data = []

    for num in range(num_target):

        # 게시물 접속
        current_idx = start_idx + num
        url = CAFE_URL + str(current_idx)
        driver.get(url)
        time.sleep(1)

        try:
            result = driver.switch_to.alert
            result.accept()

        except:
            driver.switch_to.frame('cafe_main')

            try:
                # 게시글 작성자 닉네임 및 게시글 내용 수집
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                soup_r = soup.find(class_='ContentRenderer')
                soup_n = soup.select('.profile_info > div > button')
                nickname = soup_n[0].text.strip()
                data.append([nickname, soup_r.text, 1, current_idx])

            except: pass

            else:
                # 댓글 작성자 닉네임 및 댓글 내용 수집
                soup_d = soup.find_all(class_='comment_nick_info')
                soup_ct = soup.find_all(class_='text_comment')

                for cnt_cm in range(len(soup_d)):
                    data.append([soup_d[cnt_cm].text.strip(), soup_ct[cnt_cm].text, 0, current_idx])

        # 자동 저장
        if AUTOSAVE*num and not num % AUTOSAVE: 
            save(data)
            data = []

        print(f'\r{num+1}/{num_target} Completed.', end='')

    # 데이터 수집 종료 시 저장
    save(data)


if __name__ == '__main__':
    # 실행 옵션 입력
    auto_start, start_idx, num_target = int(input('0-수동, 1-자동 : ')), 0, 10**6

    # 수동 탐색 시 시작 지점 및 탐색할 게시글 수 입력
    if not auto_start: start_idx, num_target = int(input('시작 지점 : ')), int(input('게시글 수 : '))

    # 수집 실행
    main(auto_start, start_idx, num_target)
