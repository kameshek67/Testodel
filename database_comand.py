import sqlite3


class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class UsernameError(Exception):
    pass


class StatisticError(Exception):
    pass


class SolvingYourTest(StatisticError):
    pass


class SolvingSolvedTest(StatisticError):
    pass


# функция, проверяющая уникальность имени пользователя
def check_name(name):
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    names = cursor.execute(f'''
    SELECT username FROM users WHERE username = '{name}'
    ''').fetchone()
    return not bool(names)


# функция, которая заносит пользователя в базу данных
def database_registration(name, password):
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    if not check_name(name):
        raise UsernameError()
    elif len(password) < 9:
        raise LengthError()
    elif not (any(filter(lambda x: x.isupper(), password)) and any(filter(lambda x: x.islower(), password))):
        raise LetterError()
    elif not (any(filter(lambda x: x.isdigit(), password))):
        raise DigitError()
    else:
        cursor.execute(f'''
                INSERT INTO users (username, password)
                VALUES ("{name}", "{password}")
                ''')
        cursor.execute(f'''
                INSERT INTO statistics (username, solved_tests, correct_answers, incorrect_answers, user_solved_tests, completed_tests)
                VALUES ("{name}", 0, 0, 0, 0, "")
                        ''')
        connection.commit()
        connection.close()


def database_autorisation(name, password):
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    table = cursor.execute(f'''
    SELECT username FROM users WHERE username = "{name}" AND password = "{password}"
''').fetchone()
    return bool(table)


def database_changing_statistics(username, author_username, count_correct_answers, count_incorrect_answers, test_title):
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    completed_tests = cursor.execute(f'''
            SELECT completed_tests FROM statistics
            WHERE username = "{username}" 
                                        ''').fetchone()
    completed_tests = ';;;'.join(completed_tests[0].split(';;;') + [test_title])
    cursor.execute(f'''
            UPDATE statistics
            SET completed_tests = "{completed_tests}"
            WHERE username = "{username}" 
                                        ''').fetchone()
    cursor.execute(f'''
            UPDATE Statistics
            SET solved_tests = solved_tests + 1,
            correct_answers = correct_answers + {count_correct_answers},
            incorrect_answers = incorrect_answers + {count_incorrect_answers}
            WHERE username = "{username}"
                                        ''')
    cursor.execute(f'''
            UPDATE Statistics
            SET user_solved_tests = user_solved_tests + 1
            WHERE username = "{author_username}"
                                       ''')

    connection.commit()
    connection.close()


def check_changing_statistics(username, author_username, test_title):
    if username == author_username:
        raise SolvingYourTest
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    completed_tests = cursor.execute(f'''
                SELECT completed_tests FROM statistics
                WHERE username = "{username}" ''').fetchone()
    if test_title in completed_tests[0].split(';;;'):
        raise SolvingSolvedTest
    return True


def get_top_users():
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    res = cursor.execute('''SELECT username, correct_answers, incorrect_answers FROM statistics
                      ORDER BY correct_answers DESC, incorrect_answers ASC''').fetchmany(100)
    return res


def database_get_statistics(username):
    connection = sqlite3.connect('main_database.db')
    cursor = connection.cursor()
    completed_tests = cursor.execute(f'''
                    SELECT solved_tests, correct_answers, incorrect_answers, user_solved_tests FROM statistics
                    WHERE username = "{username}" ''').fetchone()
    return completed_tests