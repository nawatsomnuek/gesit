from django.db import models


# Create your models here.
class LevelEducation(models.Model):
    level = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'{self.id}) {self.level}'


class CurriculumLevel(models.Model):
    curriculum = models.CharField(max_length=100, default="")
    levelEdu = models.ForeignKey(
        'AnalyzeGrade.LevelEducation',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.curriculum} ({self.levelEdu})'

class GroupOfSubject(models.Model):
    groupOfSubject = models.CharField(max_length=100, default="Programming")

    def __str__(self):
        return f'{self.id}) {self.groupOfSubject}'

class Subjects(models.Model):
    subjectNumber = models.CharField(max_length=100, default="")
    subjectName = models.CharField(max_length=100, default="")
    credit = models.IntegerField(default="")
    curriculumLevel = models.ForeignKey(
        'AnalyzeGrade.CurriculumLevel',
        on_delete=models.CASCADE,
    )
    groupOfSubject = models.ForeignKey(
        'AnalyzeGrade.GroupOfSubject',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.subjectNumber}'


class AmountofGroup(models.Model):
    amountofGroup = models.IntegerField(default="")

    def __str__(self):
        return f'{self.id}) {self.amountofGroup}'


class StudentStatus(models.Model):
    studentStatus = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'{self.id}) {self.studentStatus}'


class AcademicYears(models.Model):
    years = models.CharField(max_length=10, default="")

    def __str__(self):
        return f'{self.id}, {self.years}'


class Students(models.Model):
    gender = models.CharField(max_length=10, default="")
    studentsId = models.CharField(primary_key=True, max_length=20, default="")
    studentStatus = models.ForeignKey(
        'AnalyzeGrade.StudentStatus',
        on_delete=models.CASCADE,
    )
    academicYears = models.ForeignKey(
        'AnalyzeGrade.AcademicYears', on_delete=models.CASCADE, default="")

    def __str__(self):
        return f'{self.gender} {self.studentsId} {self.studentStatus} {self.academicYears}'


class GradeStatus(models.Model):
    gradestatus = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'{self.id}) {self.gradestatus}'


class Grade(models.Model):
    grade = models.FloatField(max_length=10, default="")
    description = models.CharField(max_length=100, default="")
    groups = models.IntegerField()
    students = models.ForeignKey(
        'AnalyzeGrade.Students',
        on_delete=models.CASCADE,
    )
    subjects = models.ForeignKey(
        'AnalyzeGrade.Subjects',
        on_delete=models.CASCADE,
    )
    gradestatus = models.ForeignKey(
        'AnalyzeGrade.GradeStatus',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f'{self.id}) {self.grade} {self.description} {self.groups} {self.students} {self.subjects} {self.idgradestatus}'


class UserType(models.Model):
    userType = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'{self.id}) {self.userType}'

class User(models.Model):
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    userType = models.ForeignKey(
        'AnalyzeGrade.UserType',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.id}) {self.username} {self.password} {self.userType}'


class SubjectYearStudy(models.Model):
    subject = models.ForeignKey(
        'AnalyzeGrade.Subjects',
        on_delete=models.CASCADE,
    )
    years = models.ForeignKey(
        'AnalyzeGrade.AcademicYears',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.id}) {self.subject} {self.years}'


class UserStudent(models.Model):
    firstname = models.CharField(max_length=100, default="")
    lastname = models.CharField(max_length=100, default="")
    studentID = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=100, default="")
    academicYear = models.CharField(max_length=100, default="")
    department = models.CharField(max_length=100, default="")
    username = models.ForeignKey(
        'AnalyzeGrade.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.id}) {self.username} {self.password} {self.userType}'


class GradeUserStudent(models.Model):
    grade = models.FloatField(max_length=10, default="")
    subject = models.ForeignKey(
        'AnalyzeGrade.Subjects',
        on_delete=models.CASCADE,
    )
    userStudent = models.ForeignKey(
        'AnalyzeGrade.UserStudent',
        on_delete=models.CASCADE,
    )