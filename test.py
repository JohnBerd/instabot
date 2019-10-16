#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import random
import json

insta_user = ""
insta_password = ""
hashtag_file = "hashtags.txt"
number_followers = 50
max_abos = 200
nb_days_to_unfollow = 7

today = datetime.now()
today_str = today.strftime("%Y-%m-%d")

dateformat = "%Y-%m-%d"
today = datetime.now()

# check if there is someone to unfollow


def datecmp(date_input):
    d = datetime.strptime(date_input, dateformat)
    nd = today - d
    return nd.days >= nb_days_to_unfollow


def follow(url):
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button").click()
    time.sleep(1)

def unfollow(url):
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]").click()
    sleep(1)


def scroll_randomly():
    rand = random.randint(0, 2000)
    for i in range(0, rand, 2):
        driver.execute_script("window.scrollBy(0, 2);")
    for i in range(0, rand, 2):
        driver.execute_script("window.scrollBy(0, -2);")


def check_unfollow():
    with open('magic_book.json') as json_file:
        data = json.load(json_file)
        print(data)
        i = 0
        while i < len(data['following']):
            if datecmp(data['following'][i]['date']):
                print(data['following'][i]['url'] + "is unfollowed")
                del data['following'][i]
                i -= 1
            i += 1

    with open('tt', 'w') as outfile:
        json.dump(data, outfile)

# Parsing hashtag file

try:
    with open(hashtag_file) as f:
        hashtags = f.read().splitlines()
except:
    print("Hashtag file not found! Put your hashtags line by line in " + hashtag_file)
    exit(1)

print(hashtags)

# Open Firefox

driver = webdriver.Firefox()
driver.get("https://www.instagram.com/accounts/login/?hl=fr&source=auth_switcher")
time.sleep(2)
scroll_randomly()

# Login Page

username = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
password = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
login_btn = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]')

username.send_keys(insta_user)
password.send_keys(insta_password)
login_btn.click();
time.sleep(2)
driver.implicitly_wait(5)
# Main Page
check_unfollow()

search_bar = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')

search_bar.send_keys("#" + hashtags[0])
time.sleep(2)
search_bar.send_keys(Keys.ENTER)
search_bar.send_keys(Keys.ENTER)

driver.implicitly_wait(5)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/main/article/div[2]/div/div[1]/div[1]"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/main/article/div[2]/div/div[1]/div[1]"))).click()

driver.implicitly_wait(5)
next_button = driver.find_element_by_css_selector(".coreSpriteRightPaginationArrow")


potential_targets = set()


while len(potential_targets) < number_followers:
    name = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a")
    potential_targets.add(name.get_attribute("href"))
    driver.implicitly_wait(5)
    time.sleep(3)
    next_button.click()

print(potential_targets)

driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

to_follow = list()

for x in potential_targets:
    page = driver.get(x)
    time.sleep(1)
    abo_str = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    abo = int(abo_str.replace(',', ''))
    driver.implicitly_wait(5)
    rand = random.randint(0, 5)
    #driver.execute_script("window.scrollBy(0,"+str(random.randint(0, 1000))+");")
    time.sleep(1)
    #driver.execute_script("window.scrollBy(0,"+str(random.randint(0, 1000))+");")
    time.sleep(1)
    #driver.execute_script("window.scrollBy(0);")
    print(x)
    if (abo < max_abos):
        print("Je m'abonne")
        to_follow.append(x)
        data['following'].append({
                'date': today_str,
                'url': x
            })
    else:
        print("Je m'abonne pas")

with open('magic_book.json', 'w') as outfile:
    json.dump(data, outfile)

for x in to_follow:
    follow(x)
