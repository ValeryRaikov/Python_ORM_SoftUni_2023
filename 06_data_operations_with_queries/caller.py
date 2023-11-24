import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create and check models
# Run and print your queries

from main_app.models import Student

def add_students():
    # method 1
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    Student.objects.create(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )

    # method 2
    student3 = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    student3.save()

    student4 = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )
    student4.save()


# add_students()
# print(Student.objects.all())

# Most complex
# def add_students():
#     STUDENTS = [
#         {
#             'student_id': '1FC5204',
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'birth_date': '1995-05-15',
#             'email': '1john.doe@university.com',
#         },
#         {
#             'student_id': '1FE0054',
#             'first_name': 'Jane',
#             'last_name': 'Smith',
#             'birth_date': None,
#             'email': '1jane.smith@university.com',
#         },
#         {
#             'student_id': '1FH2014',
#             'first_name': 'Alice',
#             'last_name': 'Johnson',
#             'birth_date': '1998-02-10',
#             'email': '1alice.johnson@university.com',
#         },
#         {
#             'student_id': '1FH2015',
#             'first_name': 'Bob',
#             'last_name': 'Wilson',
#             'birth_date': '1996-11-25',
#             'email': '1bob.wilson@university.com',
#         },
#     ]
#
#     for student in STUDENTS:
#         Student.objects.create(**student)


# add_students()
# print(Student.objects.all())


# def get_students_info():
#     students_records = []
#     for student in Student.objects.all():
#         students_records.append(f"Student №{student.student_id}: "
#                                 f"{student.first_name} {student.last_name}; "
#                                 f"Email: {student.email}")
#
#     return "\n".join(students_records)

# print(get_students_info())

# list comprehension
def get_students_info():
    students_records = [f"Student №{student.student_id}: {student.first_name} "
                        f"{student.last_name}; Email: {student.email}"
                        for student in Student.objects.all()]

    return "\n".join(students_records)

#print(get_students_info())


def update_students_emails():
    all_students = Student.objects.all()

    for student in all_students:
        new_email = student.email.replace('university.com', 'uni-students.com')
        student.email = new_email
        student.save()

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)


def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
