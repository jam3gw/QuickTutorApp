from django.test import TestCase
from QuickTutor.models import QTUser
from QuickTutor.models import Class, Review, Session, ClassNeedsHelp, TutorableClass
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
        Class.objects.create(class_name="ryan", dept="RYAN", course_num="1001", full_id="ryanRYAN1001")
        Class.objects.create(class_name="carl", dept="CARL", course_num="1002", full_id="carlCARL1002")
    def test_Class_str1(self):
        testclass = Class.objects.get(class_name="ryan")
        self.assertTrue(testclass.__str__() == "RYAN1001 (ryan)")
    def test_Class_str2(self):
        testclass = Class.objects.get(class_name="carl")
        self.assertTrue(testclass.__str__() == "CARL1002 (carl)")
    def test_Class_str3(self):
        testclass = Class.objects.get(class_name="ryan")
        self.assertFalse(testclass.__str__() == "RYAN1000 (ryan)")
    def test_Class_str4(self):
        testclass = Class.objects.get(class_name="carl")
        self.assertFalse(testclass.__str__() == "CARL1003 (carl)")
class QTUserTestCase(TestCase):
    def setUp(self):
        QTUser.objects.create(first_name="carlcarlcarlcarlcarlc", last_name="spanaspanaspanaspanaspanaspana", year=4, username="barl")
    def test_str_1(self):
        testUser = QTUser.objects.get(first_name="carlcarlcarlcarlcarlc")
        self.assertTrue(testUser.username == "barl")
    def test_str_2(self):
        testUser = QTUser.objects.get(first_name="carlcarlcarlcarlcarlc")
        self.assertFalse(testUser.username == "carlcarlcarlcarlcarlc")
class SessionTestCase(TestCase):
    def setUp(self):
        QTUser.objects.create(first_name="student", last_name="student", username="test")
        #testTutor = QTUser.objects.create(first_name="tutor", last_name="tutor")
        Class.objects.create(class_name="testClass", dept="TEST", course_num="1001", full_id="testClassTEST1001")
    def test_str_1(self):
        testStudent = QTUser.objects.get(first_name="student")
        testClass = Class.objects.get(class_name="testClass")
        testSession = Session.objects.create(student=testStudent, tutor=testStudent, subject_in_regards_to=testClass)
        self.assertTrue("test (student student) is having a session with test (student student) in TEST1001 (testClass)" in testSession.__str__())
    def test_str_2(self):
        testStudent = QTUser.objects.get(first_name="student")
        testClass = Class.objects.get(class_name="testClass")
        testSession = Session.objects.create(student=testStudent, tutor=testStudent, subject_in_regards_to=testClass)
        self.assertFalse("test is having a session with test in TEST1000 (testClass)" in testSession.__str__())
class ClassNeedsHelpTestCase(TestCase):
    def setUp(self):
        QTUser.objects.create(first_name="student", last_name="student", username="Ryan")
        Class.objects.create(class_name="Algorithms", dept="CS", course_num="4102", full_id="AlgorithmsCS4102_1")
    def test_str_1(self):
        testUser = QTUser.objects.get(first_name="student")
        testClass = Class.objects.get(class_name="Algorithms")
        testHelp = ClassNeedsHelp(user=testUser, class_id=testClass, elaboration="Jake help me pls")
        self.assertTrue(testHelp.__str__() == "Ryan (student student) needs help in CS4102 (Algorithms)")
    def test_str_2(self):
        testUser = QTUser.objects.get(first_name="student")
        testClass = Class.objects.get(class_name="Algorithms")
        testHelp = ClassNeedsHelp(user=testUser, class_id=testClass, elaboration="Jake help me pls")
        self.assertFalse(testHelp.__str__() == "Jake needs help in CS4102 (Algorithms)")
class TutorableClassTestCase(TestCase):
    def setUp(self):
        QTUser.objects.create(first_name="Jake", last_name="Moses", username="Jake")
        Class.objects.create(class_name="Algorithms", dept="CS", course_num="4102", full_id="AlgorithmsCS4102_2")
    def test_str_1(self):
        testUser = QTUser.objects.get(first_name="Jake")
        testClass = Class.objects.get(class_name="Algorithms")
        testTutorable = TutorableClass(user=testUser, class_id=testClass, Former_TA="TRUE", experience="")
        self.assertTrue(testTutorable.__str__() == "Jake (Jake Moses) can tutor in CS4102 (Algorithms) and they are a former TA.")
    def test_str_2(self):
        testUser = QTUser.objects.get(first_name="Jake")
        testClass = Class.objects.get(class_name="Algorithms")
        testTutorable = TutorableClass(user=testUser, class_id=testClass, Former_TA="FALSE", experience="")
        self.assertFalse(testTutorable.__str__() == "Carl can tutor in CS4102 (Algorithms)")