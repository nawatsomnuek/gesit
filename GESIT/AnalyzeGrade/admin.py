from django.contrib import admin
from .models import LevelEducation, CurriculumLevel, Subjects, AmountofGroup, StudentStatus, GradeStatus, GroupOfSubject, Students, Grade, User, UserType, SubjectYearStudy, UserStudent, GradeUserStudent


@admin.register(LevelEducation)
class LevelEducationAdmin(admin.ModelAdmin):
    pass


@admin.register(CurriculumLevel)
class CurriculumLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Subjects)
class Subjects(admin.ModelAdmin):
    pass


@admin.register(AmountofGroup)
class AmountofGroup(admin.ModelAdmin):
    pass


@admin.register(StudentStatus)
class StudentStatus(admin.ModelAdmin):
    pass


@admin.register(GroupOfSubject)
class GroupOfSubject(admin.ModelAdmin):
    pass


@admin.register(Students)
class Students(admin.ModelAdmin):
    pass


@admin.register(GradeStatus)
class GradeStatus(admin.ModelAdmin):
    pass


@admin.register(Grade)
class Grade(admin.ModelAdmin):
    pass


@admin.register(User)
class User(admin.ModelAdmin):
    pass


@admin.register(UserType)
class UserType(admin.ModelAdmin):
    pass


@admin.register(SubjectYearStudy)
class SubjectYearStudy(admin.ModelAdmin):
    pass


@admin.register(UserStudent)
class UserStudent(admin.ModelAdmin):
    pass


@admin.register(GradeUserStudent)
class GradeUserStudent(admin.ModelAdmin):
    pass