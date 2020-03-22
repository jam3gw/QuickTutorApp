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
        Class.objects.create(class_name="ryan", dept="RYAN", course_num="0001")
    def test_Class_str1(self):
        testclass = Class.objects.get(class_name="ryan")
        self.assertTrue(testclass.__str__() == "ryan")
    def test_Class_str2(self):
        testclass = Class.objects.create(class_name="carl", dept="CARL", course_num="0002")
        self.assertTrue(testclass.__str__() == "carl")
    def test_Class_str3(self):
        testclass = Class.objects.get(class_name="ryan")
        self.assertFalse(testclass.__str__() == "ryan2")
    def test_Class_str4(self):
        testclass = Class.objects.create(class_name="carl", course_num="0002")
        self.assertFalse(testclass.__str__() == "0002")
