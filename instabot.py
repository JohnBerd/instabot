#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from termcolor import colored
import time
import random
import json

# todo:
# function well_followed
# click on random post
# check_my_account
# go to my page, get number followers, following, get 0.1 followers, get number followed today, get number to follow

###########################################################

insta_user = "lecunffxavier@gmail.com"
insta_password = "Chatillon92320"
hashtag_file = "hashtags.txt"
number_followers = 10
max_abos = 200
nb_days_to_unfollow = 2
comments = ["wow!", "\u1F4AF", "\u1F4AA"]

############################################################


def json_parser():
    parsed = list()
    for x in followed['followed']:
        parsed.append(x['url'])
    return parsed


today = datetime.now()
today_str = today.strftime("%Y-%m-%d")

dateformat = "%Y-%m-%d"
today = datetime.now()

followed = json.load(open('res/followed.json'))
json_file = open('magic_book.json')
following = json.load(open('magic_book.json'))
p = json_parser()
nb_followed = 0
nb_unfollowed = 0

username = ""
my_followers = 0
my_followings = 0

# check if there is someone to unfollow

def chill():
    r = 10 + random.randint(0, 15)
    print("Chill man! I'm not a bot, I will watch stories for exactly", str(r), "seconds!")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/main/section/div[3]/div[2]/div[1]/a/div"))).click()
    time.sleep(r)
    driver.find_element_by_xpath("/html/body/span/section/div/div/section/div[2]/button[3]").click()
    time.sleep(2)


def conclusion():
    print()
    print("Number of account followed: " + colored(nb_followed, 'red'))
    print("Number of account unfollowed: " + colored(nb_unfollowed, 'green'))


def check_account():
    global my_followers
    global my_followings
    global username
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]"))).click()
    b = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/h1")
    username = b.text
    my_followers = int(driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', ''))
    my_followings = int(driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[3]/a/span").text.replace(',', ''))
    print("Hello", username, "!")
    print("followers: " + str(my_followers))
    print("following: " + str(my_followings))


def is_followed(x):
    return x in p


def datecmp(date_input):
    d = datetime.strptime(date_input, dateformat)
    nd = today - d
    return nd.days >= nb_days_to_unfollow

def like_and_comment():
        driver.implicitly_wait(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/main/div/div[2]/article/div/div/div[1]/div[1]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/span/section/main/div/div[2]/article/div/div/div[1]/div[1]"))).click()
        driver.implicitly_wait(5)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys("wow")
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/button").click()


def follow(url):
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(1)
    scroll_randomly()
    if not is_followed(url):
        driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button").click()
        followed['followed'].append({
            "url": url
        })
        print("user " + url + " followed")
        global nb_followed
        nb_followed = nb_followed + 1
    else:
        print("user " + url + " has already been followed, skiping...")
    time.sleep(1)


def unfollow(url):
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(1)
    try:
        b = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button")
    except:
        b = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/button")
    if b.text == "Follow Back" or b.text == "Follow":
        print("Who the fuck is that guy? I wasn't following him!")
    else:
        b.click()
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]").click()
        print("user " + url + " unfollowed, bye bye!")
    global nb_unfollowed
    nb_unfollowed = nb_unfollowed + 1
    time.sleep(1)


def scroll_randomly():
    rand = random.randint(0, 2000)
    for i in range(0, rand, 2):
        driver.execute_script("window.scrollBy(0, 2);")
    for i in range(0, rand, 2):
        driver.execute_script("window.scrollBy(0, -2);")


def check_unfollow():
    i = 0
    while i < len(following['following']):
        if datecmp(following['following'][i]['date']):
            unfollow(following['following'][i]['url'])
            del following['following'][i]
            with open('magic_book.json', 'w') as outfile:
                json.dump(following, outfile)
            i -= 1
        i += 1


def connect():
    print("Connection to Instagram...")
    driver.get("https://www.instagram.com/accounts/login/?hl=fr&source=auth_switcher")
    time.sleep(1)
    scroll_randomly()
    username = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
    password = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
    login_btn = driver.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]')

    username.send_keys(insta_user)
    password.send_keys(insta_password)
    login_btn.click();
    time.sleep(3)
    driver.implicitly_wait(5)
    print("Connected!")

def open_brower():
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox()
    return driver


# Parsing hashtag file


try:
    with open(hashtag_file) as f:
        hashtags = f.read().splitlines()
except:
    print("Hashtag file not found! Put your hashtags line by line in " + hashtag_file)
    exit(1)

driver = open_brower()
connect()
# driver.get("https://www.instagram.com/john_berd/")
# like_and_comment()
chill()
check_account()

# Main Page
check_unfollow()

following = json.load(open('magic_book.json'))
search_bar = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')

for hashtag in hashtags:
    following = json.load(open('magic_book.json'))
    search_bar = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
    print("searching for #" + hashtag)
    search_bar.send_keys("#" + hashtag)

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
        time.sleep(3 + random.random() * 2)
        next_button.click()

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

    to_follow = list()

    for x in potential_targets:
        page = driver.get(x)
        time.sleep(1)
        scroll_randomly()
        abo_str = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
        abo = int(abo_str.replace(',', ''))
        driver.implicitly_wait(5)
        rand = random.randint(0, 5)
        time.sleep(1)
        time.sleep(1)
        print(x)
        if (abo < max_abos):
            print("I follow, that account has just " + str(abo) + " followers", colored("<3", 'red'))
            to_follow.append(x)
            following['following'].append({
                'date': today_str,
                'url': x
                })
        else:
            print("I don't follow, that account has " + str(abo) + " followers!")

    with open('magic_book.json', 'w') as outfile:
        json.dump(following, outfile)

    for x in to_follow:
        follow(x)

    with open('res/followed.json', 'w') as outfile:
        json.dump(followed, outfile)
    driver.get("https://www.instagram.com/")

conclusion()
