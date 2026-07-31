import time
import os
from utils import Appium_DockerAndroidQuiz_WriteResult
from pages.quiz_page import QuizPage


class TestAnswerQuestion:
    def test_answer_question(self, driver):
        start = time.time()

        run_type = "jenkins" if "var/lib/jenkins/workspace" in os.getcwd() else "manual"
        results_log_path = (
            os.getcwd() + "/Appium_DockerAndroidQuiz.txt" if run_type == "jenkins"
            else "/home/brent-ubuntu-26-04/AppiumProjects/Appium_DockerAndroidQuiz/Appium_DockerAndroidQuiz.txt"
        )

        quiz_page = QuizPage(driver)
        quiz_page.wait_for_question_loaded()

        correct_answer = False
        while not correct_answer:
            correct_answer = quiz_page.answer_with_random_choice("Brent")
            if not correct_answer:
                quiz_page.go_back_to_question()
                quiz_page.wait_for_question_loaded()

        duration = time.time() - start
        with open(results_log_path, "w") as results_log:
            Appium_DockerAndroidQuiz_WriteResult.init(
                results_log, "Answer_Question", "Pass", str(duration), run_type
            )

        assert correct_answer, "Never found the correct answer"