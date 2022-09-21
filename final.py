import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

#path to chrome web driver
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://twitter.com/login")

## credentials

cred = open('credentials.txt','rt')
context = cred.read()
context = context.split('\n')

user_name = context[0]
user_password = context[1]
# Setup the log in
sleep(3)
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys(user_name)
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

sleep(3)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys(user_password)
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

sleep(3)
profile = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/a/div[4]/div')
profile.click()

sleep(3)
follower = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div[2]/a')
follower.click()
sleep(5)
followers = driver.find_elements(By.XPATH,'//div[@aria-label="Timeline: Followers"]//a[@role="link"]/div/div[@dir="ltr"]/span')

old_followers = []
new_followers = []

filereader = csv.reader(open("followers.csv","r"),delimiter = ",")
next(filereader) # skipping the column of the csv
for row in filereader:
    old_followers.append(row[0])

for i in followers:
    rep = i.text.replace('@','')
    if rep not in old_followers:
        new_followers.append([rep,f'https://twitter.com/{rep}'])


with open('new_followers.csv','w',newline="") as file:
    write = csv.writer(file)
    write.writerows(new_followers)
    file.close()

# updating the old csv to save the new followers to the existing ones.
with open('followers.csv','r+') as file:
    file.read()
    writer = csv.writer(file)
    writer.writerows(new_followers)
    file.close()

