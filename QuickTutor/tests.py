from django.test import TestCase
from QuickTutor.models import QTUser
from QuickTutor.models import Class, Review
# Create your tests here.

#class StudentTestCase(TestCase):
#    def setUp(self):
#        test_user = QTUser.objects.create(first_name="Carl", last_name="Spana")
#        Student.objects.create(student_user=test_user)
#    def test_student_test_addClass(self):
#        carl = Student.objects.get(first_name="Carl")
#        carl.addClass("CS2150", "5")
#        self.assertTrue(len(carl.classes_need_help) == 1)
#class TutorTestCase(TestCase):
#    def setUp(self):
#        test_user = QTUser.objects.create(first_name="Carl", last_name="Spana")
#        Tutor.objects.create(student_user=test_user)
#    def test_Tutor_addClass(self):
#        carl = Tutor.objects.get(first_name="Carl")
#        carl.addClass("CS3240","9")
#        self.assertTrue(len(carl.classes_need_help) == 1)
class ClassTestCase(TestCase):
    def setUp(self):
        Class.objects.create(class_name="ryan", dept="RYAN", course_num="1001")
    def test_Class_str1(self):
        testclass = Class.objects.get(class_name="ryan")
        print(testclass.__str__())
        self.assertTrue(testclass.__str__() == "RYAN1001 (ryan)")
    def test_Class_str2(self):
        testclass = Class.objects.create(class_name="carl", dept="CARL", course_num="1002")
        self.assertTrue(testclass.__str__() == "CARL1002 (carl)")
    def test_Class_str3(self):
        testclass = Class.objects.get(class_name="ryan")
        self.assertFalse(testclass.__str__() == "RYAN1000 (ryan)")
    def test_Class_str4(self):
        testclass = Class.objects.create(class_name="carl", dept="CARL", course_num="1002")
        self.assertFalse(testclass.__str__() == "CARL1003 (carl)")
