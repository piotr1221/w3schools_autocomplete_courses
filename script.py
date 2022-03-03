import argparse
import os
from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

def get_options():
    options = Options()
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.accept_untrusted_certs = True
    return options

def login(driver, args):
    driver.find_element(By.ID, os.getenv('login_email')).send_keys(args.EMAIL)
    driver.find_element(By.ID, os.getenv('login_password')).send_keys(args.PASSWORD)
    driver.find_element(By.XPATH, os.getenv('login_button')).click()

def select_course(driver, args, course_choices):
    explore_all = driver.find_element(By.XPATH, os.getenv('explore_all'))
    driver.execute_script("arguments[0].click();", explore_all)
    
    for i in range(1, len(course_choices) + 1):
        all_courses = driver.find_element(By.XPATH, os.getenv('all_courses_list'))
        possible_course_titles = all_courses.find_elements(By.XPATH, f'./div[{i}]{os.getenv("course_title_parent")}/*')
        for course_title in possible_course_titles:
            if args.COURSE in course_title.text:
                course_title.click()
                return
        
def complete_tutorial(driver, args):
    driver.find_element(By.XPATH, f'//*[contains(text(), \"{os.getenv("tutorial_tab")}\")]').click()
    nav = driver.find_element(By.ID, os.getenv('tutorial_nav'))
    home = os.getenv("home")
    nav.find_element(By.XPATH, f'./a[contains(translate(., "{home.lower()}", "{home.upper()}"), "{home.upper()}")]').click()
    
    while driver.find_elements(By.XPATH, f'//a[contains(text(), \"{os.getenv("next")}\")]'):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        #driver.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
        driver.find_element(By.XPATH, f'//a[contains(text(), \"{os.getenv("next")}\")]').click()

def main(args, course_choices):
    load_dotenv()
    with Firefox(options=get_options()) as driver:
        driver.implicitly_wait(int(os.getenv('wait_time')))
        driver.get(os.getenv('w3school_url'))

        login(driver, args)

        select_course(driver, args, course_choices)

        if args.TUTORIAL:
            complete_tutorial(driver, args)

        print('ra')
        time.sleep(10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read inverters values and push data to Neural')

    parser.add_argument('--email', action='store', dest='EMAIL', required=True, help='E-mail for login')
    parser.add_argument('--password', action='store', dest='PASSWORD', required=True, help='Password for login')
    course_choices=('HTML', 'CSS', 'JavaScript', 'Node.js', 'React', 'PHP', 'jQuery', 'AngularJS', 'XML')
    parser.add_argument('--course', action='store', dest='COURSE', required=True, choices=course_choices,
                        help='Course to scrap through')
    parser.add_argument('--tutorial', action=argparse.BooleanOptionalAction, dest='TUTORIAL', required=True,
                        help='Complete all tutorial')
    parser.add_argument('--exercise', action=argparse.BooleanOptionalAction, dest='EXERCISE', required=True,
                        help='Complete all exercises')

    args = parser.parse_args()
    main(args, course_choices)