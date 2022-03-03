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
    all_courses = driver.find_element(By.XPATH, os.getenv('all_courses_list'))
    
    for i in range(1, len(course_choices) + 1):
        course = all_courses.find_element(By.XPATH, f'./div[{i}]{os.getenv("course_title")}')
        if args.COURSE in course.text:
            course.click()
            break
    
def complete_tutorial(driver, args):
    driver.find_element(By.XPATH, f'//*[contains(text(), \"{os.getenv("tutorial_tab")}\")]').click()
    
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