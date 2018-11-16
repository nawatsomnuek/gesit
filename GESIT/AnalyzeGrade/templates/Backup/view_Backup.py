from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Kmean
import pandas as pd
from pandas import merge, read_excel
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

from .form import CountryForm

from .models import LevelEducation, CurriculumLevel, Subjects, AcademicYears, Students, Grade

# Create your views here.
# gradeFromDB = [[1, 3.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 2.0], [1, 2.0], [1, 3.0], [1, 4.0], [1, 3.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 3.0], [1, 3.5], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 1.5], [1, 2.0], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 4.0], [1, 4.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 2.5], [1, 4.0], [1, 1.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 3.5], [1, 2.5], [1, 2.0], [1, 3.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 3.5], [1, 2.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 4.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 3.5], [1, 3.0], [1, 3.5], [1, 2.0], [1, 1.5], [1, 3.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 3.5], [1, 1.5], [1, 2.0], [1, 4.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 1.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.0], [1, 2.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 4.0], [1, 3.5], [2, 3.0], [2, 4.0], [2, 1.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 2.5], [2, 0.0], [2, 3.5], [2, 3.5], [2, 4.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 3.5], [2, 1.5], [2, 1.5], [2, 2.0], [2, 1.0], [2, 4.0], [2, 2.0], [2, 2.5], [2, 0.0], [2, 1.0], [2, 3.5], [2, 0.0], [2, 2.0], [2, 3.5], [2, 2.5], [2, 4.0], [2, 3.0], [2, 1.0], [2, 2.0], [2, 1.0], [2, 1.0], [2, 1.5], [2, 2.5], [2, 2.5], [2, 3.0], [2, 2.5], [2, 1.5], [2, 3.0], [2, 4.0], [2, 4.0], [2, 3.5], [2, 1.5], [2, 4.0], [2, 3.5], [2, 2.5], [2, 1.0], [2, 4.0], [2, 1.5], [2, 2.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 0.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 2.0], [2, 4.0], [2, 3.5], [2, 1.0], [2, 2.0], [2, 1.0], [2, 0.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 3.0], [2, 4.0], [2, 4.0], [2, 1.5], [2, 4.0], [2, 2.5], [2, 4.0], [2, 2.5], [2, 0.0], [2, 2.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 1.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 3.5], [2, 2.0], [2, 0.0], [2, 1.5], [2, 4.0], [2, 1.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 2.5], [2, 1.5], [2, 2.5], [2, 2.0], [2, 2.5], [2, 4.0], [2, 1.0], [2, 4.0], [2, 4.0], [2, 2.0], [2, 2.0], [2, 0.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 3.5], [2, 2.0], [2, 1.5], [2, 3.0], [2, 3.0]]
gradeFromDBQQ = []
subjectSelected = []
numberOfGroup = []
checked = []
amountOfMenberInGroup = []
amountOfMenberInGroupC = []


# Go to page
def firstPage(request):
    return render(request, 'start.html')


def homePage(request):
    numberOfGroup.clear()
    amountOfMenberInGroup.clear()
    amountOfMenberInGroupC.clear()
    return render(request, 'Home.html')


@csrf_exempt
def loginPage(request):
    # request.session['member_id'] = None
    usernameInput = request.POST.get('username')
    usernameDB = 'admin'
    passwordInput = request.POST.get('password')
    passwordDB = 'admin'
    if usernameInput == usernameDB:
        if passwordInput == passwordDB:
            # request.session['member_id'] = usernameDB
            gradeFromDBQQ = []
            subjectSelected = []
            numberOfGroup = []
            checked = []
            amountOfMenberInGroup = []
            amountOfMenberInGroupC = []
            request.session[usernameDB] = {
                'username': usernameDB,
                'gradeFromDBQQ': gradeFromDBQQ,
                'subjectSelected': subjectSelected,
                'numberOfGroup': numberOfGroup,
                'checked': checked,
                'amountOfMenberInGroup': amountOfMenberInGroup,
                'amountOfMenberInGroupC': amountOfMenberInGroupC
            }
    if usernameDB in request.session:
        print('--- session user ---')
        print(request.session['member_id'].get('username'))
    
    

    return render(request, 'login.html')


@csrf_exempt
def Home_lecturerPage(request):
    # if amountOfMenberInGroup is not None:
    #     amountOfMenberInGroup.clear()
    # if amountOfMenberInGroupC is not None:
    #     amountOfMenberInGroupC.clear()
    # if subjectSelected is not None:
    #     subjectSelected.clear()
    # if numberOfGroup is not None:
    #     numberOfGroup.clear()
    return render(request, 'Home_lecturer.html')


# @csrf_exempt
# def TallSoneY55Page(request):
#     # Clear Array
#     if amountOfMenberInGroup is not None:
#         amountOfMenberInGroup.clear()
#     if amountOfMenberInGroupC is not None:
#         amountOfMenberInGroupC.clear()
#     if ll is not None:
#         ll.clear()
#     if numberOfGroup is not None:
#         numberOfGroup.clear()

#     subjectObjects = list(Subjects.objects.all().values())
#     subjects = []
#     i = 0
#     subb = {}
#     while i <= subjectObjects.__len__() - 1:
#         subjects.append(subjectObjects[i])
#         i = i + 1

#     subb = {"subjects": subjects}

#     checked = []
#     j = 0
#     while j <= subjects.__len__() - 1:
#         if request.POST.get(
#                 subjectObjects[j].get('subjectNumber')) is not None:
#             checked.append(
#                 request.POST.get(subjectObjects[j].get('subjectNumber')))
#         j = j + 1
#     if checked != []:
#         print("Hey Hello")
#         for arr in checked:
#             ll.append(arr)
#         print("------- TallSoneY55Page----------")
#         print(ll)
#         return HttpResponseRedirect('/Home/login/TallSoneY55/GraphallSoneY')
#     print(checked)

#     return render(request, 'TallSoneY55.html', subb)

@csrf_exempt
def selectSubject(request):
    # Clear Array
    # if amountOfMenberInGroup is not None:
    #     amountOfMenberInGroup.clear()
    # if amountOfMenberInGroupC is not None:
    #     amountOfMenberInGroupC.clear()
    # if ll is not None:
    #     ll.clear()
    # if numberOfGroup is not None:
    #     numberOfGroup.clear()

    # Get list Subject from Database
    subjectObjects = list(Subjects.objects.all().values())
    subjects = [] # subjects from subjectObjects
    isubjectObjects = 0
    while isubjectObjects <= subjectObjects.__len__() - 1:
        subjects.append(subjectObjects[isubjectObjects])
        isubjectObjects = isubjectObjects + 1

    # Get list year from Database
    academicYears = list(AcademicYears.objects.all().values())
    years = []
    iyears = 0
    while iyears <= academicYears.__len__() - 1:
        years.append(academicYears[iyears].get('years'))
        iyears = iyears + 1
    # Show on page
    subb = {
        "subjects": subjects,
        "years": years
    }

    # When choose subjects
    checked = []
    j = 0
    while j <= subjects.__len__() - 1:
        if request.POST.get(subjectObjects[j].get('subjectNumber')) is not None:
            checked.append(request.POST.get(subjectObjects[j].get('subjectNumber')))
        j = j + 1
    if checked != []:
        # Get data form Database
        subjectss = []
        for result in checked:
            subjectss.append({
                "subjectNumber": result,
                "gradeSubject": list(Grade.objects.filter(
                students__academicYears__years='2555', 
                subjects__subjectNumber=result).values()
                )
            })
        # Make data to equal data
        tmp = 1000000000
        for result in subjectss:
            if result.get('gradeSubject').__len__() < tmp:
                tmp = result.get('gradeSubject').__len__()
        arr = []
        for result in subjectss:
            array = result.get('gradeSubject')
            res = array.__len__() - tmp
            if res != 0:
                while res > 0:
                    array.remove(array[array.__len__()-1])
                    res = res - 1
            arr.append({
                'sub': result.get('subjectNumber'),
                'subb': array
            })

        d = {}
        subjectSelected.clear()
        for result in arr:
            ddd = []
            subjectSelected.append(result.get('sub'))
            for result1 in result.get('subb'):
                ddd.append(result1.get('grade'))
            # print(ddd)
            d.update({result.get('sub') : pd.Series(ddd)})

        df = pd.DataFrame(d)
        gradeFromDBQQ.append(df)
        print("--- df ---")
        print(df)
        print("--- subjectSelected ---")
        print()
        return HttpResponseRedirect('/Home/login/GraphallSoneY')

        # # Get data form list which from Database
        # gradee = []
        # countResult = 1
        # for result in subjectss:
        #     tmpGeade = []
        #     for result1 in result.get('gradeSubject'):
        #         tmpGeade.append(countResult)
        #         tmpGeade.append(result1.get('grade'))
        #         gradee.append(tmpGeade)
        #         if tmpGeade != None:
        #             tmpGeade = []
        #         # print(result.get('subjectNumber'))
        #         # print(result1.get('grade'))
        #     countResult = countResult + 1

        # for result in gradee:
        #     gradeFromDB.append(result)
        # return HttpResponseRedirect('/Home/login/GraphallSoneY')
        # # print(gradeFromDB)
        # # print("--- gradeFromDB ---")
        # print(gradeFromDB)
    
    return render(request, 'selectSubject.html', subb)


# @csrf_exempt
# def cc(request):
    # i = 0
    # j = ['INT101', 'INT102', 'INT103']
    # pp = []

    # while i <= 2:
    #     check = request.POST.get(j[i])
    #     if j[i] == check:
    #         pp.append(pp)
    # print("checkk ----- checkk")
    # print(pp)
    # return render(request, 'chart.html')


# @csrf_exempt
# def listSubjects(request):
#     ll.clear()
#     subjectObjects = list(Subjects.objects.all().values())
#     subjects = []
#     i = 0
#     subb = {}

#     # print("----------- Testttt -----------")
#     # print(subjectObjects[0].get('subjectNumber'))

#     while i <= subjectObjects.__len__() - 1:
#         subjects.append(subjectObjects[i])
#         i = i + 1
#     subb = {"subjects": subjects}

#     # Choose subject(s)
#     checked = []
#     j = 0
#     while j <= subjects.__len__() - 1:
#         if request.POST.get(
#                 subjectObjects[j].get('subjectNumber')) is not None:
#             checked.append(
#                 request.POST.get(subjectObjects[j].get('subjectNumber')))
#         j = j + 1
#     print(checked)

#     return HttpResponseRedirect('/Home/login/')


# def renderForm(self, name, value, attrs=None, choices=()):
#     if value is None:
#         value = []
#     has_id = attrs and 'id' in attrs
#     final_attrs = self.build_attrs(attrs, name=name)
#     output = []
#     # Normalize to strings
#     str_values = set([force_unicode(v) for v in value])
#     for i, (option_value, option_label) in enumerate(
#             chain(self.choices, choices)):
#         # If an ID attribute was given, add a numeric index as a suffix,
#         # so that the checkboxes don't all have the same ID attribute.
#         if has_id:
#             final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
#             label_for = u' for="%s"' % final_attrs['id']
#         else:
#             label_for = ''

#         cb = widgets.CheckboxInput(
#             final_attrs, check_test=lambda value: value in str_values)
#         option_value = force_unicode(option_value)
#         rendered_cb = cb.render(name, option_value)
#         option_label = conditional_escape(force_unicode(option_label))
#         output.append(u'<label class="%s"%s>%s %s</label>' %
#                       (self.label_class, label_for, rendered_cb, option_label))
#     return mark_safe(u'\n'.join(output))

# @csrf_exempt
# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             print("34567890------------_________")
#         if form.data == "int101":
#             print("int101")
#         #     #     # process the data in form.cleaned_data as required
#         #     #     # ...
#         #     #     # redirect to a new URL:
#         # return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'chart.html', {'form': form})


def excel():
    df = pd.read_excel('55_AllSubjects.xlsx')
    return df


def kmeamAlg():
    # df = excel()
    total = 21
    i = 2
    silh_score = []
    # ppp = ['INT102', 'INT105', 'INT302']
    # ggg = [[1, 3.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 2.0], [1, 2.0], [1, 3.0], [1, 4.0], [1, 3.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 3.0], [1, 3.5], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 1.5], [1, 2.0], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 4.0], [1, 4.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 2.5], [1, 4.0], [1, 1.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 3.5], [1, 2.5], [1, 2.0], [1, 3.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 3.5], [1, 2.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 4.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 3.5], [1, 3.0], [1, 3.5], [1, 2.0], [1, 1.5], [1, 3.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 3.5], [1, 1.5], [1, 2.0], [1, 4.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 1.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.0], [1, 2.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 4.0], [1, 3.5], [2, 3.0], [2, 4.0], [2, 1.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 2.5], [2, 0.0], [2, 3.5], [2, 3.5], [2, 4.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 3.5], [2, 1.5], [2, 1.5], [2, 2.0], [2, 1.0], [2, 4.0], [2, 2.0], [2, 2.5], [2, 0.0], [2, 1.0], [2, 3.5], [2, 0.0], [2, 2.0], [2, 3.5], [2, 2.5], [2, 4.0], [2, 3.0], [2, 1.0], [2, 2.0], [2, 1.0], [2, 1.0], [2, 1.5], [2, 2.5], [2, 2.5], [2, 3.0], [2, 2.5], [2, 1.5], [2, 3.0], [2, 4.0], [2, 4.0], [2, 3.5], [2, 1.5], [2, 4.0], [2, 3.5], [2, 2.5], [2, 1.0], [2, 4.0], [2, 1.5], [2, 2.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 0.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 2.0], [2, 4.0], [2, 3.5], [2, 1.0], [2, 2.0], [2, 1.0], [2, 0.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 3.0], [2, 4.0], [2, 4.0], [2, 1.5], [2, 4.0], [2, 2.5], [2, 4.0], [2, 2.5], [2, 0.0], [2, 2.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 1.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 3.5], [2, 2.0], [2, 0.0], [2, 1.5], [2, 4.0], [2, 1.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 2.5], [2, 1.5], [2, 2.5], [2, 2.0], [2, 2.5], [2, 4.0], [2, 1.0], [2, 4.0], [2, 4.0], [2, 2.0], [2, 2.0], [2, 0.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 3.5], [2, 2.0], [2, 1.5], [2, 3.0], [2, 3.0], [3, 4.0], [3, 2.5], [3, 3.5], [3, 1.5], [3, 3.5], [3, 2.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 3.5], [3, 2.0], [3, 4.0], [3, 4.0], [3, 4.0], [3, 2.5], [3, 4.0], [3, 1.0], [3, 4.0], [3, 3.0], [3, 3.5], [3, 1.5], [3, 3.0], [3, 4.0], [3, 1.5], [3, 4.0], [3, 4.0], [3, 3.5], [3, 2.0], [3, 3.0], [3, 2.0], [3, 2.5], [3, 4.0], [3, 2.5], [3, 4.0], [3, 4.0], [3, 1.5], [3, 2.0], [3, 2.5], [3, 2.5], [3, 2.5], [3, 4.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 3.0], [3, 3.5], [3, 4.0], [3, 4.0], [3, 3.5], [3, 4.0], [3, 4.0], [3, 4.0], [3, 3.0], [3, 2.0], [3, 4.0], [3, 2.0], [3, 3.5], [3, 4.0], [3, 1.5], [3, 3.5], [3, 4.0], [3, 3.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 4.0], [3, 4.0], [3, 3.0], [3, 3.5], [3, 4.0], [3, 2.0], [3, 3.5], [3, 3.0], [3, 3.0], [3, 4.0], [3, 2.5], [3, 2.5], [3, 3.0], [3, 4.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 3.0], [3, 4.0], [3, 4.0], [3, 4.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 3.5], [3, 3.5], [3, 3.0], [3, 3.5], [3, 4.0], [3, 3.5], [3, 3.0], [3, 3.5], [3, 4.0], [3, 3.0], [3, 4.0], [3, 4.0], [3, 3.0], [3, 4.0], [3, 3.0], [3, 2.5], [3, 3.0], [3, 4.0], [3, 4.0], [3, 3.5], [3, 3.5], [3, 3.0], [3, 3.5], [3, 3.0], [3, 2.0], [3, 4.0], [3, 4.0], [3, 2.5]]
    # print("------------- kmeamAlg ----------------")
    # ppp = ll

    # gradeFromDB = gradeFromDBQQ[['INT101', 'INT102']]
    gradeFromDB0 = gradeFromDBQQ[0]
    # gradeFromDB = gradeFromDB0[['INT101', 'INT102', 'INT103']]
    gradeFromDB = gradeFromDB0[subjectSelected]
    print("--- gradeFromDB ---")
    print(gradeFromDB)
    while i <= total:
        clf = KMeans(n_clusters=i)
        clf.fit(gradeFromDB)
        s = [i, silhouette_score(gradeFromDB, clf.labels_)]
        silh_score.append(s)
        i += 1
    return silh_score


def findMaxSilhScore():
    silh_score = kmeamAlg()
    numberOfGroup.append(silh_score)
    j = 0
    max_value = 0
    maxx = []
    while j <= silh_score.__len__() - 1:
        if silh_score[j][1] > max_value:
            max_value = silh_score[j][1]
            maxx = silh_score[j]
        j += 1
    return maxx[0]


def clusterCenterWhenGetMaxValue():
    maxValue = findMaxSilhScore()
    checked.append(maxValue)
    gradeFromDB0 = gradeFromDBQQ[0]
    gradeFromDB = gradeFromDB0[subjectSelected]
    clf = KMeans(n_clusters=maxValue)
    clf.fit(gradeFromDB)

    amountOfMenber = {
        i: np.where(clf.labels_ == i)[0]
        for i in range(maxValue)
    }
    iinwhile = 0
    amount = 0

    while iinwhile < amountOfMenber.__len__():
        for i in amountOfMenber.get(iinwhile):
            amount = amount + 1
        amountOfMenberInGroup.append([iinwhile + 1, amount])
        amount = 0
        iinwhile = iinwhile + 1
    return clf.cluster_centers_.tolist()
    # return np.array2string(clf.cluster_centers_)


def chooseGroup(group):
    clf = KMeans(n_clusters=group)
    checked.clear()
    checked.append(group)
    gradeFromDB0 = gradeFromDBQQ[0]
    gradeFromDB = gradeFromDB0[subjectSelected]
    clf.fit(gradeFromDB)
    amountOfMenber = {i: np.where(clf.labels_ == i)[0] for i in range(group)}
    iinwhile = 0
    while iinwhile < amountOfMenber.__len__():
        amount = 0
        for i in amountOfMenber.get(iinwhile):
            amount = amount + 1
        amountOfMenberInGroupC.append([iinwhile + 1, amount])
        iinwhile = iinwhile + 1

    return clf.cluster_centers_.tolist()


@csrf_exempt
def showGeaphOfCluster(request):
    cluterCenterFromKmeans = clusterCenterWhenGetMaxValue()

    # Find number of group and values
    p = 0
    numGroup = []
    valueGroup = []
    while p < numberOfGroup[0].__len__():
        numGroup.append(numberOfGroup[0][p][0])
        valueGroup.append(numberOfGroup[0][p][1])
        p = p + 1
    
    # Number of member in each group
    eachGroup = []
    amountMem = []
    for result in amountOfMenberInGroup:
        eachGroup.append(result[0])
        amountMem.append(result[1])

    data = {
       "labels": subjectSelected,
       "data": cluterCenterFromKmeans,
       "checked": checked[0],
       "numGroup": numGroup,
       "valueGroup": valueGroup,
       "group": eachGroup,
       "numOfMember": amountMem
    }

    if request.POST.get('group') is not None:
        # Clear value amountOfMenberInGroupC
        amountOfMenberInGroupC.clear()

        # Call chooseGroup when select group by self
        choose = chooseGroup(int(request.POST.get('group')))

        # Number of member in each group at another time
        eachGroup = []
        amountMem = []
        for result in amountOfMenberInGroupC:
            eachGroup.append(result[0])
            amountMem.append(result[1])

        data = {
            "labels": subjectSelected,
            "data": choose,
            "checked": checked[0],
            "numGroup": numGroup,
            "valueGroup": valueGroup,
            "group": eachGroup,
            "numOfMember": amountMem
        }
        return render(request, 'GraphallSoneY.html', data)
    return render(request, 'GraphallSoneY.html', data)


# def index(request, *args, **kwargs):
@csrf_exempt
def index(request, *args, **kwargs):
    # Find in first time
    amountOfMenberInGroup.clear()
    cluterCenterFromKmeans = clusterCenterWhenGetMaxValue()
    pu = 0
    numGroup = []
    valueGroup = []
    while pu < numberOfGroup[0].__len__():
        numGroup.append(numberOfGroup[0][pu][0])
        valueGroup.append(numberOfGroup[0][pu][1])
        pu = pu + 1

    string = ""
    array = []
    array2 = []
    dataInArray = []
    for i in cluterCenterFromKmeans:
        if (i != "["):
            if (i == "1" or i == "2" or i == "3" or i == "4" or i == "5"
                    or i == "6" or i == "7" or i == "8" or i == "9" or i == "0"
                    or i == "."):
                string = string + i
            elif (i == " "):
                array.append(string)
                string = ""
            elif (i == "]"):
                array.append(string)
                string = ""
                for j in array:
                    if (j != "" and j != "]" and j != "["):
                        inn = float(j)
                        array2.append(inn)
                        array = []
                if (len(array2) != 0):
                    dataInArray.append(array2)
                    array2 = []

    # Number of Member in each group
    print("-------------- amountOfMenberInGroup ----------------")
    print(amountOfMenberInGroup)
    eachGroup = []
    amountMem = []
    for result in amountOfMenberInGroup:
        eachGroup.append(result[0])
        amountMem.append(result[1])

    data = {
        "labels": ll,
        "data": dataInArray,
        "numGroup": numGroup,
        "valueGroup": valueGroup,
        "group": eachGroup,
        "numOfMember": amountMem
    }

    # Find another time
    if request.POST.get('group') is not None:
        # print("----- request.POST.get('group') is not None -----")
        # print(type(int(request.POST.get('group'))))
        amountOfMenberInGroupC.clear()
        choose = chooseGroup(int(request.POST.get('group')))
        # print("------ -------- choose ----------")
        # print(choose)

        # Number of Member in each group at times
        eachGroup = []
        amountMem = []
        for result in amountOfMenberInGroupC:
            eachGroup.append(result[0])
            amountMem.append(result[1])

        data = {
            "labels": ll,
            "data": choose,
            "numGroup": numGroup,
            "valueGroup": valueGroup,
            "group": eachGroup,
            "numOfMember": amountMem
        }
        return render(request, 'GraphallSoneY.html', data)

    return render(request, 'GraphallSoneY.html', data)


def get_data(request, *args, **kwargs):

    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]

    levels = LevelEducation.objects.all().values()
    s = ['INT101', 'INT102']
    curriculums = []
    for result in s:
        curriculums.append({
            "sub": result,
            "subb": list(Grade.objects.filter(
            students__academicYears__years='2555', 
            subjects__subjectNumber=result).values()
            )
        })
    
    gradee = []
    for result in curriculums:
        ddd = []
        countResult = 1
        for result1 in result.get('subb'):
            ddd.append(countResult)
            ddd.append(result1.get('grade'))
            gradee.append(ddd)
            if ddd != None:
                ddd = []
            # print(countResult)
            # print(result1.get('grade'))
            countResult = countResult + 1
    print("--- geadeee ---")
    print(gradee)
    d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),}

    subjects = list(Subjects.objects.all().values())

    data = {
        # "labels": labels,
        # "defaultData": [1, 2, 3, 4, 5, 6],
        # "level": list(levels),
        "curriculums": curriculums,
        # "subject": subjects
    }
    return JsonResponse(data)