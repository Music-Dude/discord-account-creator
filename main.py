from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import random
import time
import os

termsize = os.get_terminal_size()[0]
left = ' '*int(termsize/4)


def write(*args, **kwargs):
    print(left, *args, **kwargs)


def ask(prompt):
    write(prompt, end='')
    return input()


def intro(text):
    text = text.split('\n')
    for t in text:
        print(f'{t : ^{termsize}}')


os.system('cls' if os.name == 'nt' else 'clear')
bars = '-'*(termsize//2)
intro(bars + '\nDiscord Account Creator\n\nMade by Music_Dude#0001\nhttps://github.com/Music-Dude\n' + bars + '\n\n')

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
    driver.execute_script(
        'setInterval(()=>{document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token=null},50),setTimeout(()=>{location.reload()},0);')
    time.sleep(2)
    driver.delete_all_cookies()


email = ask('Enter your GMAIL address: ').split('@')[0].replace('.', '')
write(
    f'That email address will be able to create {2**len(email)//2} accounts.')
numaccounts = int(
    ask('What is the maximum number of accounts you would like to generate: '))
emails = get_emails(email)

startTime = time.time()/60
with driver:
    for i in range(1, numaccounts+1):
        print('\n')
        write(f'Creating account #{i}...')

        email = next(emails) + '@gmail.com'
        password = ''.join(random.choices(pwchars, k=8))
        month = random.choice(['January', 'February', 'March', 'April', 'May',
                               'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        day = str(random.randint(1, 28))
        year = str(random.randint(1980, 2003))

        driver.get('https://discord.com/register')
        write(f'Using credentials {email}:{password}')

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
            ask('Is there a captcha? Press enter once you\'ve completed it.')
        except TimeoutException:
            pass

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url != 'https://discord.com/register')

            token = driver.execute_script(
                'location.reload();var i=document.createElement("iframe");document.body.appendChild(i);return i.contentWindow.localStorage.token').strip('"')
            write(f'Successully created account! Token: {token}\n')

            with open('accounts.txt', 'a+') as file:
                file.write(f'{email}:{password}:{token}\n')
        except TimeoutException:
            pass
        finally:
            logout(driver)

write('Results:')
write(
    f'Created {numaccounts} accounts in {time.time()/60-startTime:0.2F} minutes.')
write('Credentials are stored in the file \'accounts.txt\'.')
ask('Press enter to exit.')

driver.quit()
