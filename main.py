import argparse
import os
from dotenv import load_dotenv
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from html import unescape
import time
from utilities.find_answers import find_answers

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
    courses = driver.find_elements(By.XPATH, f"{os.getenv('all_courses_list')}/*")

    for course in courses:
        element = course.find_element(By.XPATH, f'.{os.getenv("course_title")}')
        if args.COURSE in element.text:
            element.click()
            return driver.current_url
        
def complete_tutorial(driver, args, course_url):
    if not args.TUTORIAL:
        return
    driver.find_element(By.XPATH, f'//*[contains(text(), \"{os.getenv("tutorial_tab")}\")]').click()
    # xpath = f'./a[contains(translate(., "{os.getenv("first_lesson").lower()}", \
    #                                     "{os.getenv("first_lesson").upper()}"), \
    #                                     "{os.getenv("first_lesson").upper()}")]'
    # driver.find_element(By.ID, os.getenv('tutorial_nav')) \
    #         .find_element(By.XPATH, xpath) \
    #         .click()

    visited_links = set()
    while driver.find_elements(By.XPATH, f'//a[contains(text(), \"{os.getenv("next")}\")]'):
        if driver.current_url in visited_links \
            or driver.find_element(By.ID, os.getenv('main')) \
            .find_element(By.XPATH, './h1').text == f'W3Schools {args.COURSE} Certificate':
            print('xdxdxd')
            break
        visited_links.add(driver.current_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, f'//a[contains(text(), \"{os.getenv("next")}\")]').click()
    
    print(f'Tutorial for {args.COURSE} course completed')
    driver.get(course_url)

def complete_exercises(driver, args, course_url):
    if not args.EXERCISE:
        return
    try:
        driver.find_element(By.CLASS_NAME, os.getenv("exercise_tab")).click()

        while driver.find_elements(By.ID, os.getenv('submit_ans')):

            inputs = driver.find_element(By.ID, os.getenv('empty_assignment')) \
                                .find_elements(By.XPATH, "./input")

            empty_ans = unescape(driver.find_element(By.ID, os.getenv('empty_assignment')) \
                                        .text
                            ).split()

            template_code = unescape(driver.find_element(By.XPATH,
                                            f'//*[contains(@id, \"{os.getenv("template_code")}\")]') \
                                            .get_attribute('innerHTML')
                                    )

            correct_code = unescape(driver.find_element(By.XPATH,
                                            f'//*[contains(@id, \"{os.getenv("correct_code")}\")]') \
                                            .get_attribute('innerHTML')
                                    )

            exercise_url = driver.current_url
            
            correct_answers = find_answers(template_code, correct_code)

            for input, ans in zip(inputs, correct_answers):
                input.send_keys(ans)

            time.sleep(0.3)
            try:
                driver.find_element(By.ID, os.getenv('submit_ans')).click()
                driver.find_element(By.ID, os.getenv('submit_ans')).click()
            except:
                print(f'Exercises for {args.COURSE} course completed')
                driver.get(course_url)
                return

    except Exception as e:
        print('This course doesn\'t have exercises')
        return


def main(args, course_choices):
    load_dotenv()
    if not args.PATH: 
        driver = Firefox(options=get_options()) 
    else:
        driver = Firefox(options=get_options(), executable_path=args.PATH)

    with driver as driver:
        driver.implicitly_wait(int(os.getenv('wait_time')))
        driver.get(os.getenv('w3school_url'))

        login(driver, args)

        course_url = select_course(driver, args, course_choices)

        complete_tutorial(driver, args, course_url)

        complete_exercises(driver, args, course_url)

        print('ra')
        time.sleep(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read data to complete the courses')

    parser.add_argument('--email', action='store', dest='EMAIL', required=True, help='E-mail for login')
    parser.add_argument('--password', action='store', dest='PASSWORD', help='Password for login')
    course_choices=('HTML', 'CSS', 'JavaScript', 'Node.js', 'React', 'PHP', 'jQuery', 'AngularJS', 'XML', 'MySQL', 'SQL')
    parser.add_argument('--course', action='store', dest='COURSE', required=True, choices=course_choices,
                        help='Course to scrap through')
    parser.add_argument('--tutorial', action=argparse.BooleanOptionalAction, dest='TUTORIAL', required=True,
                        help='Complete all tutorial')
    parser.add_argument('--exercise', action=argparse.BooleanOptionalAction, dest='EXERCISE', required=True,
                        help='Complete all exercises')
    parser.add_argument('--path', action='store', dest='PATH', required=False, help='Path to geckodriver')                    
    args = parser.parse_args()
    main(args, course_choices)