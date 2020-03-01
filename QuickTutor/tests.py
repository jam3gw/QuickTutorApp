from django.test import TestCase
from QuickTutor.models import QTUser
from QuickTutor.models import Student
# Create your tests here.

class StudentTestCase(TestCase):
    def setUp(self):
        test_user = QTUser.objects.create(first_name="Carl", last_name="Spana")
        Student.objects.create(student_user=test_user)
    def test_student_test_addClass(self):
        carl = Student.objects.get(first_name="Carl")
        carl.addClass("CS2150", "5")
        self.assertTrue(len(carl.classes_need_help) == 1)
class TutorTestCase(TestCase):
    def setUp(self):
        test_user = QTUser.objects.create(first_name="Carl", last_name="Spana")
        Tutor.objects.create(student_user=test_user)
    def test_Tutor_addClass(self):
        carl = Tutor.objects.get(first_name="Carl")
        carl.addClass("CS3240","9")
        self.assertTrue(len(carl.classes_need_help) == 1)
        

    
    