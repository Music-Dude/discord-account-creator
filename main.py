from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
from os import get_terminal_size
import random
import time

termsize = get_terminal_size()[0]
def printcenter(text):
    print(f'''{text : ^{termsize}}''')

bars = '-'*(termsize//2-2)
printcenter(bars)
printcenter('Discord Account Creator\n')
printcenter('Made by Music_Dude#0001')
printcenter('https://github.com/Music-Dude')
printcenter(bars + '\n\n')

driver = uc.Chrome()
pwchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def get_emails(username):
    if len(username) < 2:
        yield username
    else:
        head = username[0]
        tail = username[1:]

        for item in get_emails(tail):
            yield head + item
            yield head + '.' + item


def logout(driver: uc.Chrome):
    """Log out of Discord to create another account"""
    driver.execute_script('setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=null},50),setTimeout(()=>{location.reload()},2500);')
    driver.delete_all_cookies()

EMAIL = input('    Enter your GMAIL address: ').split('@')[0].replace('.', '')
print(f'    That email address will be able to create {2**len(EMAIL)//2} accounts.')
NUMACCOUNTS = int(
    input('    What is the maximum number of accounts you would like to generate: '))
emails = get_emails(EMAIL)

startTime = time.time()/60
with driver:
    for i in range(1, NUMACCOUNTS+1):
        printcenter(f'Creating account #{i}...')

        email = next(emails) + '@gmail.com'
        password = ''.join(random.choices(pwchars, k=8))
        month = random.choice(['January', 'February', 'March', 'April', 'May',
                               'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        day = str(random.randint(1, 28))
        year = str(random.randint(1980, 2003))

        driver.get('https://discord.com/register')
        print(f'Using credentials {email}:{password}')

        elems = driver.find_elements_by_tag_name('input')
        keys = (email, password, password, month+'\ue004', day, year)

        for text, elem in zip(keys, elems):
            elem.send_keys(text)
            time.sleep(0.05)

        try:
            driver.find_element_by_css_selector(
                'input[type="checkbox"]').click()
        except:
            pass

        driver.find_elements_by_tag_name('button')[0].click()

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
            input('    Is there a captcha? Press enter once you\'ve completed it.')
        except TimeoutException:
            pass

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url != 'https://discord.com/register')

            token = driver.execute_script(
                'location.reload();var i=document.createElement("iframe");document.body.appendChild(i);return i.contentWindow.localStorage.token').strip('"')
            printcenter(f'Successully created account! Token: {token}\n')

            with open('accounts.txt', 'a+') as file:
                file.write(f'{email}:{password}:{token}\n')
        except:
            pass
        finally:
            logout(driver)

input(f'    Results:\n    Created {NUMACCOUNTS} accounts in {time.time()/60-startTime} minutes.\n    Credentials are stored in the file \'accounts.txt\'.\n\n    Press enter to exit.')
driver.quit()
