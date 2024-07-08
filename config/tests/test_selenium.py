import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd


class TestCalBond(unittest.TestCase):

    def setUp(self):
        chrome_driver_path = 'C:\\work\\tools\\chrome_driver\\chromedriver-win64\\chromedriver.exe'
        chrome_service = Service(chrome_driver_path)
        chrome_options = Options()
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.get('file:///C:/Users/hwkim/PycharmProjects/Cal_Bond_V001/config/templates/config/main.html')

    def test_calculation(self):
        driver = self.driver

        # 엑셀 파일에서 입력 데이터 로드
        input_data = pd.read_excel('input_data.xlsx')

        for index, row in input_data.iterrows():
            # 각 입력 필드를 찾고 값을 설정합니다.
            driver.find_element(By.ID, '발행일').send_keys(row['발행일'].strftime('%Y-%m-%d'))
            driver.find_element(By.ID, '만기일').send_keys(row['만기일'].strftime('%Y-%m-%d'))
            driver.find_element(By.ID, '오늘날짜').send_keys(row['오늘날짜'].strftime('%Y-%m-%d'))
            driver.find_element(By.ID, '현재가격').clear()
            driver.find_element(By.ID, '현재가격').send_keys(str(row['현재가격']))
            driver.find_element(By.ID, '표면금리').send_keys(str(row['표면금리']))
            driver.find_element(By.ID, '만기수익률').send_keys(str(row['만기수익률']))
            driver.find_element(By.ID, '이자지급주기').send_keys(str(row['이자지급주기']))

            # 폼을 제출합니다.
            driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

            # 결과를 확인하기 위해 잠시 대기합니다.
            time.sleep(2)  # 계산 결과가 나타날 시간을 줍니다.

            # 결과를 확인합니다.
            total_interest = driver.find_element(By.ID, 'totalInterest').text
            investment_period = driver.find_element(By.ID, 'investmentPeriod').text
            interest_payment_count = driver.find_element(By.ID, 'interestPaymentCount').text

            # 데이터를 엑셀 파일로 저장합니다.
            data = {
                "total_interest": [total_interest],
                "investment_period": [investment_period],
                "interest_payment_count": [interest_payment_count]
            }
            df = pd.DataFrame(data)
            df.to_excel('bond_interest_summary.xlsx', index=False)

            # 결과를 텍스트 파일로 저장합니다.
            with open('bond_interest_summary.txt', 'w') as file:
                file.write(f"채권이자 합계: {total_interest}\n")
                file.write(f"투자 기간: {investment_period}\n")
                file.write(f"이자가 지급되는 횟수: {interest_payment_count}\n")

            # 기대하는 결과와 비교합니다 (여기서는 예시로 일부 문자열이 포함되었는지 확인).
            self.assertIn('채권이자 합계:', total_interest)
            self.assertIn('투자 기간:', investment_period)
            self.assertIn('이자가 지급되는 횟수:', interest_payment_count)

            # 여러 행의 데이터를 처리할 경우 브라우저를 초기 상태로 되돌립니다.
            driver.get('file:///C:/Users/hwkim/PycharmProjects/Cal_Bond_V001/config/templates/config/main.html')

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
