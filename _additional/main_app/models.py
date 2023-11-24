from django.db import models
from django.core import validators


# Create your models here.
class BaseStudent(models.Model):
    first_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2, "First name cannot be less than 2 symbols!"),
            validators.MaxLengthValidator(100, "First name cannot be moe than 100 symbols!")
        ]
    )

    last_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2, "Last name cannot be less than 2 symbols!"),
            validators.MaxLengthValidator(100, "Last name cannot be moe than 100 symbols!")
        ]
    )

    identifier_number = models.CharField(
        max_length=10,
        validators=[
            validators.RegexValidator(r'^\d{9}$', "Identifier must contain exactly 9 digits!"),
        ]
    )

    final_grade = models.DecimalField(
        max_digits=1,
        decimal_places=1,
        validators=[
            validators.MinValueValidator(2.00, "Grade cannot be less than 2.00!"),
            validators.MaxValueValidator(6.00, "Grade cannot be greater than 6.00!")
        ]
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        ...


class SchoolStudent(BaseStudent):
    class SubjectsAvailable(models.TextChoices):
        F_E_M_I = 'French, English, Maths, Informatics',
        F_E_M_G = 'French, English, Maths, Geography',
        F_E_B_H = 'French, English, Bulgarian, History',
        F_E_C_B = 'French, English, Chemistry, Biology',

    age = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(7, "Age for school student cannot be less than 7 years!"),
            validators.MaxValueValidator(20, "Age for school students cannot be more than 60 years!"),
        ]
    )

    school_year = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(8, "School year cannot be less than 8!"),
            validators.MaxValueValidator(12, "School year cannot be more than 12!"),
        ]
    )

    subjects = models.CharField(
        max_length=100,
        choices=SubjectsAvailable.choices,
    )

    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'School Student'
        verbose_name_plural = 'School Students'
        db_table = 'school_student'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} is a school student in {self.school_year} grade."


class UniversityStudent(BaseStudent):
    class UniSpecialties(models.TextChoices):
        SE = 'Software Engineering',
        CS = 'Computer Science',
        IT = 'Information Technologies',
        I = 'Informatics',

    class UniDisciplines(models.TextChoices):
        Python_P = 'Python programming',
        C_P = 'C programming',
        J_P = 'Java programming',
        CS_P = 'C# programming',
        CPP_P = 'C++ programming',

    age = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(18, "Age for university student cannot be less than 18 years!"),
            validators.MaxValueValidator(60, "Age for university students cannot be more than 60 years!"),
        ]
    )

    uni_year = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1, "University year cannot be less than 1!"),
            validators.MaxValueValidator(6, "University year cannot be more than 6!"),
        ]
    )

    specialty = models.CharField(
        max_length=100,
        choices=UniSpecialties.choices,
    )

    disciplines = models.CharField(
        max_length=100,
        choices=UniDisciplines.choices,
    )

    class Meta:
        verbose_name = 'University Student'
        verbose_name_plural = 'University Students'
        db_table = 'uni_student'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} is a university student in {self.uni_year} course."
