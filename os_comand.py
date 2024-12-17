import os
from random import shuffle

def create_my_tests(username):
    test_lst = []
    try:
        test_lst = os.listdir(fr'tests\{username}\all_test')
    except FileNotFoundError:
        pass
    return test_lst


def create_posted_tests(username):
    test_lst = []
    users_lst = os.listdir(fr'tests')
    if username in users_lst:
        users_lst.remove(username)
    for user in users_lst:
        user_test_lst = os.listdir(fr'tests\{user}\posted_test')
        for test in user_test_lst:
            test_lst.append((test, user))
    shuffle(test_lst)
    return test_lst

