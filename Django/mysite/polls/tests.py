from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than  1 day."""
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)


def create_question(question_text, day):
    time = timezone.now() + datetime.timedelta(days=day)
    return Question.objects.create(question_text=question_text,pub_date=time)




class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """if no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")

    def test_past_question(self):
        """Questions with a pub_date in the  past are display"""
        question = create_question(question_text="Past question.",day=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed the index page."""
        create_question(question_text="Future question.",day=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self):
        """Even if both past and future question exist,only past questions are displayed"""
        question = create_question(question_text="past question.",day=-30)
        create_question(question_text="Future question.",day=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    def test_two_past_questions(self):
        """The questions index page may display multiple Questions."""
        question1 = create_question(question_text="Past question 1",day=-30)
        question2 = create_question(question_text="Past question 2",day=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question2,question1],)

class QuestionDetailsViewTests(TestCase):
    def test_future_question(self):
         """The detail view of a question with a question with a pub_date in the future returns a 404 not found."""
         future_question = create_question(question_text="Future question.",day=5)
         url = reverse("polls:detail",args=(future_question.id,))
         response = self.client.get(url)
         self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text="Past question",day=-5)
        url = reverse("polls:detail",args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)






