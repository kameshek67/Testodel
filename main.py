import sys

from database_comand import database_registration, database_autorisation, database_changing_statistics, \
    check_changing_statistics, database_get_statistics, get_top_users
from database_comand import LengthError, LetterError, DigitError, UsernameError, SolvingYourTest, SolvingSolvedTest
from csv_create import create_test_csv, taking_test_lst
from os_comand import create_my_tests, create_posted_tests

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QTableWidgetItem, QListWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize

USERNAME = ''


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\registration_window.ui', self)  # Загружаем дизайн
        self.setFixedSize(790, 570)

        self.back_button.clicked.connect(self.go_back)
        self.registration_button.clicked.connect(self.registration)

    def go_back(self):
        self.close()

    def registration(self):
        name = self.name_edit.text()
        password = self.password_edit.text()
        try:
            database_registration(name, password)
            self.message_label.setText('Вы успешно зарегестрировались!')
        except UsernameError:
            self.message_label.setText('Такое имя пользователя уже сузествует, придумайте что-нибудь пооригинальней)')
        except LengthError:
            self.message_label.setText('Пароль должен состоять более чем из 8 символов!')
        except LetterError:
            self.message_label.setText('В пароле должны присутствовать заглавные и прописные буквы!')
        except DigitError:
            self.message_label.setText('В пароле должна быть цифра!')
        except Exception:
            self.message_label.setText('Регистрироваться 2 раза подряд под одним нкиом - плохая идея')


class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\authorization_window.ui', self)  # Загружаем дизайн
        self.setFixedSize(790, 550)

        self.registration_button.clicked.connect(self.go_registration)
        self.enter_button.clicked.connect(self.autorisation)

    def go_registration(self):
        self.ex = RegistrationWindow()
        self.ex.show()

    def autorisation(self):
        global username
        name = self.name_edit.text()
        password = self.password_edit.text()
        if database_autorisation(name, password):
            global USERNAME
            USERNAME = name
            self.ex = MainWindow()
            self.close()
            self.ex.show()
        else:
            self.error_label.setText('неправильное имя пользователя или пароль(')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\main_window.ui', self)  # Загружаем дизайн
        self.setFixedSize(1250, 740)

        self.create_test_button.clicked.connect(self.create_test)
        self.my_tests_but.clicked.connect(self.my_tests)
        self.posted_test_button.clicked.connect(self.posted_test)
        self.my_statistics_but.clicked.connect(self.check_statistics)
        self.top_users_but.clicked.connect(self.check_top_users)

    def create_test(self):
        test_title, ok_pressed = QInputDialog.getText(self, "название теста",
                                                      "Введите название теста")
        if ok_pressed:
            for i in test_title:
                if i in '><?:"\\|/*':
                    test_title = test_title.replace(i, '')
            count_questions, ok_pressed1 = QInputDialog.getInt(
                self, "количество вопросов", "Введите количество вопросов",
                15, 2, 30, 1)
            if ok_pressed and ok_pressed1:
                self.ex = CreateTestWindows(count_questions, test_title)
                self.ex.show()
                self.close()

    def posted_test(self):
        self.ex = PostedTest()
        self.ex.show()
        self.close()

    def my_tests(self):
        self.ex = MyTest()
        self.ex.show()
        self.close()

    def check_statistics(self):
        self.ex = StatisticsWidget()
        self.ex.show()
        self.close()

    def check_top_users(self):
        self.ex = TopUsersWindow()
        self.ex.show()
        self.close()


class CreateTestWindows(QWidget):
    def __init__(self, count_questions, test_title):
        super().__init__()
        self.initUI()
        self.count_questions = count_questions
        self.test = []
        self.test_title = test_title
        self.count = 1

    def initUI(self):
        uic.loadUi('interfaces\\create_test.ui', self)  # Загружаем дизайн
        self.setFixedSize(1250, 700)

        self.next_quest.clicked.connect(self.checked_click)

    def checked_click(self):
        edits = [self.quest_edit, self.answer1, self.answer2, self.answer3,
                 self.answer4, self.answer_right]
        edits_text = list(map(lambda x: x.text(), edits))
        if all(edits_text) and edits_text[-1] in edits_text[1:-1]:
            if self.count < self.count_questions:
                if self.count == self.count_questions - 1:
                    self.next_quest.setText('завершить создание')
                self.count += 1
                self.test.append(edits_text)
                self.number_quest.setText(f'вопрос {self.count}')
                for i in edits:
                    i.setText('')
            else:
                self.test.append(edits_text)
                self.ex = ConfirmationTestCreating(self.test, USERNAME, self.test_title)
                self.test = []
                self.ex.show()
                self.close()
        elif edits_text[-1] in edits_text[1:-1]:
            self.error_label.setText('Видимо вы неправильно написали ответ')
        else:
            self.error_label.setText('Видимо вы что-то пропустили')


class ConfirmationTestCreating(QWidget):
    def __init__(self, test, user_name, test_title):
        super().__init__()
        self.ex = MainWindow()
        self.test = test
        self.user_name = user_name
        self.test_title = test_title
        self.initUI()
    def initUI(self):
        uic.loadUi('interfaces\\confirmation_creation.ui', self)  # Загружаем дизайн
        self.setFixedSize(490, 375)

        self.create_button.clicked.connect(self.create_test)
        self.cancel_button.clicked.connect(self.cancel)

    def cancel(self):
        self.close()
        self.ex.show()

    def create_test(self):
        post_test = self.post_checkBox.isChecked()
        create_test_csv(self.test, self.test_title, self.user_name, post_test)
        self.close()
        self.ex.show()


class MyTest(QWidget):
    def __init__(self):
        super().__init__()
        self.directory_lst = create_my_tests(USERNAME)
        self.count_tests = len(self.directory_lst)
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\my_tests_widget.ui', self)  # Загружаем дизайн
        self.setFixedSize(1250, 710)
        self.back_to_home.clicked.connect(self.back_home)

        for i in range(self.count_tests):
            test = self.directory_lst[i]
            item = QListWidgetItem(test[:-4])
            item.setSizeHint(QSize(400, 50))
            item.setFont(QFont('Arial', 18))
            self.my_tests_widget.addItem(item)
        self.list_items = [self.my_tests_widget.item(i).text() for i in range(self.my_tests_widget.count())]

        self.my_tests_widget.itemClicked.connect(self.open_solution_quest)
        self.search_but.clicked.connect(self.search_test)

    def open_solution_quest(self, item):
        self.ex = SolutiuonTest(item.text(), USERNAME)
        self.ex.show()
        self.close()

    def search_test(self):
        text = self.search_bar.text()
        self.my_tests_widget.clear()
        for i in self.list_items:
            if text.lower() in i.lower():
                item = QListWidgetItem(i)
                item.setSizeHint(QSize(400, 50))
                item.setFont(QFont('Arial', 18))
                self.my_tests_widget.addItem(item)
    def back_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()


class SolutiuonTest(QWidget):
    def __init__(self, test_title, author_username, posted_test=False):
        super().__init__()
        self.author_username = author_username
        self.test_title = test_title
        self.quests_lst = taking_test_lst(self.test_title, self.author_username, posted_test=posted_test)
        self.count_quests = len(self.quests_lst)
        self.question_number = 0
        self.answers = []
        self.count_right_answers = 0
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\solution_test.ui', self)  # Загружаем дизайн
        self.setFixedSize(1275, 785)

        self.back_to_home.clicked.connect(self.back_home)
        self.back_quest_but.clicked.connect(self.back)

        self.question.setText(self.quests_lst[0][0])
        self.answer1.setText(self.quests_lst[0][1])
        self.answer1.clicked.connect(self.answer)

        self.answer2.setText(self.quests_lst[0][2])
        self.answer2.clicked.connect(self.answer)

        self.answer3.setText(self.quests_lst[0][3])
        self.answer3.clicked.connect(self.answer)

        self.answer4.setText(self.quests_lst[0][4])
        self.answer4.clicked.connect(self.answer)

    def answer(self):
        answer = self.sender().text()
        self.answers.append(answer)
        if answer == self.quests_lst[self.question_number][5]:
            self.count_right_answers += 1
        if self.question_number < self.count_quests - 1:
            self.question_number += 1
            self.question.setText(self.quests_lst[self.question_number][0])
            self.answer1.setText(self.quests_lst[self.question_number][1])
            self.answer2.setText(self.quests_lst[self.question_number][2])
            self.answer3.setText(self.quests_lst[self.question_number][3])
            self.answer4.setText(self.quests_lst[self.question_number][4])
        elif self.question_number == self.count_quests - 1:
            self.ex = ResultWindow(self.count_right_answers, self.count_quests, self.test_title, self.author_username)
            self.ex.show()
            self.close()

    def back(self):
        if self.question_number > 0:
            self.question_number -= 1
            self.answers.pop()
            self.question.setText(self.quests_lst[self.question_number][0])
            self.answer1.setText(self.quests_lst[self.question_number][1])
            self.answer2.setText(self.quests_lst[self.question_number][2])
            self.answer3.setText(self.quests_lst[self.question_number][3])
            self.answer4.setText(self.quests_lst[self.question_number][4])

    def back_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()


class ResultWindow(QWidget):
    def __init__(self, count_correct_answers, count_quests, test_title, author_username):
        super().__init__()
        self.test_title = test_title
        self.author_username = author_username
        self.count_quests = count_quests
        self.count_correct_answers = count_correct_answers
        self.count_incorrect_answers = self.count_quests - self.count_correct_answers
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\result_widget.ui', self)  # Загружаем дизайн
        self.setFixedSize(1250, 700)

        try:
            check_changing_statistics(USERNAME, self.author_username, self.test_title)
            database_changing_statistics(USERNAME, self.author_username, self.count_correct_answers,
                                         self.count_incorrect_answers, self.test_title)
        except SolvingYourTest:
            self.notification_label.setText('Похоже, что вы решили свой тест. Ваша статистика не будет изменена(')
        except SolvingSolvedTest:
            self.notification_label.setText(
                'Похоже, что вы решили этот тест не первый раз. Ваша статистика не будет изменена(')

        self.result_label.setText(f'вы правильно ответили на {self.count_correct_answers} из {self.count_quests}')
        self.back_to_home.clicked.connect(self.back_home)

    def back_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()


class PostedTest(QWidget):
    def __init__(self):
        super().__init__()
        self.directory_lst = create_posted_tests(USERNAME)
        self.count_tests = len(self.directory_lst)
        self.initUI()

    def initUI(self):
        uic.loadUi('interfaces\\posted_tests_widget.ui', self)  # Загружаем дизайн
        self.setFixedSize(1256, 714)

        for i in range(self.count_tests):
            test = self.directory_lst[i][0]
            username = self.directory_lst[i][1]
            item = QListWidgetItem(f'{test[:-4]}\nby {username}')
            item.setSizeHint(QSize(400, 74))
            item.setFont(QFont('Arial', 18))
            self.posted_tests_widget.addItem(item)
        self.list_items = [self.posted_tests_widget.item(i).text() for i in range(self.posted_tests_widget.count())]

        self.posted_tests_widget.itemClicked.connect(self.open_solution_quest)
        self.back_to_menu.clicked.connect(self.back_to_home)
        self.search_but.clicked.connect(self.search_test)

    def open_solution_quest(self, item):
        test_lst = item.text().split('\n')
        test_title = test_lst[0]
        author_username = test_lst[1][3:]
        self.ex = SolutiuonTest(test_title, author_username, True)
        self.ex.show()
        self.close()

    def search_test(self):
        text = self.search_bar.text()
        self.posted_tests_widget.clear()
        for i in self.list_items:
            if text.lower() in i.lower():
                item = QListWidgetItem(i)
                item.setSizeHint(QSize(400, 74))
                item.setFont(QFont('Arial', 18))
                self.posted_tests_widget.addItem(item)

    def back_to_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()


class StatisticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stat_lst = database_get_statistics(USERNAME)
        self.solved_tests = self.stat_lst[0]
        self.correct_answers = self.stat_lst[1]
        self.incorrect_answers = self.stat_lst[2]
        self.user_solved_test = self.stat_lst[3]
        self.answers = self.incorrect_answers + self.correct_answers
        if self.answers != 0:
            self.correct_answers_kd = int(round(self.correct_answers / (self.answers * 0.01), 0))
        else:
            self.correct_answers_kd = 0
        self.InitUI()

    def InitUI(self):
        uic.loadUi('interfaces\\satatistics_widget.ui', self)  # Загружаем дизай
        self.setFixedSize(1270, 810)

        self.back_to_menu.clicked.connect(self.back_to_home)

        self.solved_tests_label.setText(str(self.solved_tests))
        self.answers_label.setText(str(self.answers))
        self.correct_answers_label.setText(str(self.correct_answers))
        self.incorrect_answers_label.setText(str(self.incorrect_answers))
        self.progressBar.setValue(self.correct_answers_kd)
        self.completed_test_label.setText(str(self.user_solved_test))

    def back_to_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()


class TopUsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.top_table = get_top_users()
        self.InitUI()

    def InitUI(self):
        uic.loadUi('interfaces\\top_users_window.ui', self)
        self.setFixedSize(1250, 745)

        for i, row in enumerate(self.top_table):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.back_to_menu.clicked.connect(self.back_to_home)

    def back_to_home(self):
        self.ex = MainWindow()
        self.ex.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuthorizationWindow()
    ex.show()
    sys.exit(app.exec())
