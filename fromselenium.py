from selenium.webdriver.support.select import Select
from selenium import webdriver
from time import sleep
from PIL import Image
import time
from selenium.webdriver.common.by import By
import platform
from ocr import baidu_orc
import operation

def get_real_resolution():
    from win32 import win32api, win32gui, win32print
    from win32.lib import win32con

    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    from win32.win32api import GetSystemMetrics
    """获取缩放后的分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h

def get_window_scale():

    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)

    return screen_scale_rate

def get_system():
    if platform.system() == 'Windows':
        return True
    else:
        return False

def save_web_screenshot(driver, img_doc):
    now = time.strftime('%Y-%m-%d %H-%M')
    filename = ("{}_{}.png".format(img_doc, now))
    try:
        driver.save_screenshot(filename)
        # MyLog().info("网页截图成功，保存在：{}".format(Open.screenshots() + filename))
        return filename
    except:
        raise

def get_captcha_pic(driver, loc, filename):
    if get_system():
        rate = get_window_scale()
    else:
        rate = 1

    # 获取指定元素位置
    element = driver.find_element(*loc)
    left = int(element.location['x']) * rate
    top = int(element.location['y']) * rate
    right = int(element.location['x'] + element.size['width']) * rate
    bottom = int(element.location['y'] + element.size['height']) * rate

    # 通过Image处理图像
    # dir = Open.screenshots()
    im = Image.open(filename)
    im = im.crop((left, top, right, bottom))
    filepath = 'capcha.png'
    im.save(filepath)

    return filepath

def get_capchat_result(driver, description, loc):
    all_page_pic = save_web_screenshot(driver, description + 'whole_page')
    capcha_pic = get_captcha_pic(driver, loc, all_page_pic)
    a = baidu_orc()
    result = a.get_captcha(capcha_pic)

    return result

if __name__ == '__main__':

    url = 'https://he.122.gov.cn/#/vehxhhdpub'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    sleep(1.5)


    x =''
    while x == '':
        opt = driver.find_element_by_name('glbm')
        Select(opt).select_by_value('130900000400')

        sleep(1.2)

        search = driver.find_element_by_id('btnSearch')
        search.click()

        sleep(1.2)

        picture = (By.XPATH, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[2]/td[2]/div/span/img')

        result = get_capchat_result(driver, 'abc', picture)

        capcha_value = operation.opearation_result(result)

        driver.find_element_by_id('csessionid').send_keys(capcha_value)
        sleep(1.2)

        driver.find_element_by_xpath(
            '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]').click()

        try:
            a = driver.switch_to_alert()
            print(a.text)
            a.accept()

        except:
            content = '/html/body/div[3]/div/div/div/div/div/div[4]/div/table/tbody'
            all_text = driver.find_element_by_xpath(content).text

            print(all_text)
            x = 'no'
