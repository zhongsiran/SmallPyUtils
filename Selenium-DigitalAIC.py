from selenium import webdriver
import pyautogui as auto
import time

auto.PAUSE = 2
auto.FAILSAFE = False

driver = webdriver.Ie()

driver.get('http://10.21.2.28:9080/gzaic/')
frame = driver.find_element_by_name('topframe')
driver.switch_to.frame(frame)
login_btn = driver.find_element_by_id('btnLogin')
login_btn.click()

time.sleep(5)

auto.press('enter')

if len(driver.window_handles) == 2 and driver.window_handles[1] != driver.current_window_handle:
    # 需要修改成以Title判断
    driver.switch_to.window(driver.window_handles[1])
    zong_he_zhi_fa = driver.find_element_by_css_selector("div[node-id='1268141136125']")
    zong_he_zhi_fa.click()
    zong_he_zhi_fa.click()

    print(driver.title)
elif len(driver.window_handles) != 2:
    print(len(driver.window_handles))
    print('转入新页面过慢')
else:
    print(driver.current_window_handle)
