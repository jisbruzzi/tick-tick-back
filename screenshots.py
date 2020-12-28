from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from PIL import Image
import PIL.ImageOps
import subprocess

def make_driver():
    options = Options()
    options.headless = True
    fp = webdriver.FirefoxProfile('/home/jose/.mozilla/firefox/5ud9v1om.default-release')
    driver = webdriver.Firefox(fp, options=options, executable_path="./geckodriver")
    driver.get('https://ticktick.com/webapp/#q/all/tasks')
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 1024)
    
    return driver

def create_good_screenshot():
    background = Image.new('RGB', (1920, 1080), color = (255,255,255))
    img = Image.open("screenshot.png")
    background.paste(img)
    matrix = (
        0.6, 0, 0, 0,
        0, 0.6, 0, 0x2b,
        0, 0, 0.6, 0x36)
    modified = PIL.ImageOps.invert(background).convert("RGB",matrix)
    modified.save('wallpaper.png')

def customize_page(driver):
    driver.execute_script('document.body.style.fontFamily="monospace"')
    driver.execute_script('document.getElementById("add-task")?.remove()')
    driver.execute_script('document.getElementsByTagName("header")[0]?.remove()')
    driver.execute_script('document.getElementById("left-menu-t")?.remove()')

def update_desktop():
    subprocess.run(['feh', '--bg-scale', 'wallpaper.png'])

driver = make_driver()
while True:
    print("saving")
    customize_page(driver)
    screenshot = driver.save_screenshot('screenshot.png')
    create_good_screenshot()
    update_desktop()
    time.sleep(3)