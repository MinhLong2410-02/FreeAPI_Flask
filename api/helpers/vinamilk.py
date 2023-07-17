from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bs
import urllib

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def generate_vinamilk_img(name, left, right):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://taoanhdep.com/tao-avatar-logo-vinamilk-est-1976/')
    script = f'''
    document.querySelector('.tad-in-text1').value = '{name}';
    document.querySelector('.tad-in-text2').value = '{left}';
    document.querySelector('.tad-in-text3').value = '{right}';
    document.querySelector('#tad-taoanh').click();
    '''

    driver.execute_script(script)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "taianh")))

    script = '''
        document.querySelector('.tad-shareimg').click();
    '''
    driver.execute_script(script)
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located(
                      (By.ID, "urlShare")))

    script = '''
        return document.querySelector('#urlShare').value;
    '''
    url = driver.execute_script(script)
    driver.quit()
    return url


# print(generate_vinamilk_img("ndtd", "dungkon", "2002"))
