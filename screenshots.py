from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from PIL import Image
import PIL.ImageOps
import subprocess

def make_driver(url):
    options = Options()
    options.headless = True
    fp = webdriver.FirefoxProfile('/home/jose/.mozilla/firefox/5ud9v1om.default-release')
    driver = webdriver.Firefox(fp, options=options, executable_path="./geckodriver")
    driver.get(url)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 1120)
    
    return driver

def create_good_screenshot(left,right):
    background = Image.new('RGB', (1920, 1080), color = (255,255,255))
    background.paste(Image.open(left).resize((int(800*1.2),int(1120*1.2))))
    background.paste(Image.open(right).resize((int(800*1.2),int(1120*1.2))),(960,0))
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
    

driver_week = make_driver("https://ticktick.com/webapp/#q/all/week")
driver_tag = make_driver("https://ticktick.com/webapp/#t/b3BjaW9uYWw/tasks")
while True:
    print("saving")
    customize_page(driver_week)
    driver_week.save_screenshot("week.png")
    customize_page(driver_tag)
    driver_tag.save_screenshot("optional.png")
    create_good_screenshot("week.png","optional.png")
    update_desktop()
    