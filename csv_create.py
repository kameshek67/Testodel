import csv
import os
from time import sleep


def create_test_csv(test_list, test_title, user_name, post_test):
    if not os.path.exists(f'tests\\{user_name}'):
        os.mkdir(f'tests\\{user_name}')
        os.mkdir(f'tests\\{user_name}\\all_test')
        os.mkdir(f'tests\\{user_name}\\posted_test')
        sleep(0.1)
    if post_test:
        with open(f'tests\\{user_name}\\posted_test\\{test_title}.csv', 'w', newline='', encoding='utf8') as test:
            test_writer = csv.writer(test, delimiter=';', quotechar='"')
            test_writer.writerow(['quest', 'answer1', 'answer2', 'answer3', 'answer4', 'answer_right'])
            for i in test_list:
                test_writer.writerow(i)
    with open(f'tests\\{user_name}\\all_test\\{test_title}.csv', 'w', newline='', encoding='utf8') as test:
        test_writer = csv.writer(test, delimiter=';', quotechar='"')
        test_writer.writerow(['quest', 'answer1', 'answer2', 'answer3', 'answer4', 'answer_right'])
        for i in test_list:
            test_writer.writerow(i)


def taking_test_lst(test_title, user_name, posted_test=False):
    test_lst = []
    if not posted_test:
        test_type = 'all_test'
    else:
        test_type = 'posted_test'
    with open(f'tests\\{user_name}\\{test_type}\\{test_title}.csv', 'r', encoding='utf8') as test:
        test_reader = csv.reader(test, delimiter=';', quotechar='"')
        for i in list(test_reader)[1:]:
            test_lst.append(i)
    return test_lst

