from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

# Kmean
import pandas as pd
from pandas import merge, read_excel
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

import scipy
from scipy.stats.stats import pearsonr

from .form import CountryForm

from .models import LevelEducation, CurriculumLevel, Subjects, AcademicYears, Students, Grade, User, SubjectYearStudy, UserStudent, GradeUserStudent
# Create your views here.
# gradeFromDB = [[1, 3.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 2.0], [1, 2.0], [1, 3.0], [1, 4.0], [1, 3.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 3.0], [1, 3.5], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 1.5], [1, 2.0], [1, 3.5], [1, 3.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 4.0], [1, 4.0], [1, 4.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 2.5], [1, 4.0], [1, 1.5], [1, 4.0], [1, 1.5], [1, 2.5], [1, 3.5], [1, 2.5], [1, 2.0], [1, 3.0], [1, 3.5], [1, 3.5], [1, 4.0], [1, 3.5], [1, 3.5], [1, 2.5], [1, 4.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 4.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 3.5], [1, 3.0], [1, 3.5], [1, 2.0], [1, 1.5], [1, 3.0], [1, 2.5], [1, 3.0], [1, 3.0], [1, 3.0], [1, 2.5], [1, 2.0], [1, 2.5], [1, 4.0], [1, 3.5], [1, 4.0], [1, 3.5], [1, 1.5], [1, 2.0], [1, 4.0], [1, 2.0], [1, 2.5], [1, 2.5], [1, 2.5], [1, 2.5], [1, 1.0], [1, 2.5], [1, 2.5], [1, 3.0], [1, 4.0], [1, 2.0], [1, 2.0], [1, 2.5], [1, 3.5], [1, 4.0], [1, 4.0], [1, 3.5], [2, 3.0], [2, 4.0], [2, 1.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 2.5], [2, 0.0], [2, 3.5], [2, 3.5], [2, 4.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 3.5], [2, 1.5], [2, 1.5], [2, 2.0], [2, 1.0], [2, 4.0], [2, 2.0], [2, 2.5], [2, 0.0], [2, 1.0], [2, 3.5], [2, 0.0], [2, 2.0], [2, 3.5], [2, 2.5], [2, 4.0], [2, 3.0], [2, 1.0], [2, 2.0], [2, 1.0], [2, 1.0], [2, 1.5], [2, 2.5], [2, 2.5], [2, 3.0], [2, 2.5], [2, 1.5], [2, 3.0], [2, 4.0], [2, 4.0], [2, 3.5], [2, 1.5], [2, 4.0], [2, 3.5], [2, 2.5], [2, 1.0], [2, 4.0], [2, 1.5], [2, 2.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 0.0], [2, 1.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 2.0], [2, 4.0], [2, 3.5], [2, 1.0], [2, 2.0], [2, 1.0], [2, 0.0], [2, 2.0], [2, 2.0], [2, 4.0], [2, 3.0], [2, 4.0], [2, 4.0], [2, 1.5], [2, 4.0], [2, 2.5], [2, 4.0], [2, 2.5], [2, 0.0], [2, 2.0], [2, 1.5], [2, 2.0], [2, 4.0], [2, 1.0], [2, 4.0], [2, 3.5], [2, 4.0], [2, 2.0], [2, 3.5], [2, 2.0], [2, 0.0], [2, 1.5], [2, 4.0], [2, 1.5], [2, 3.0], [2, 3.5], [2, 2.5], [2, 2.5], [2, 1.5], [2, 2.5], [2, 2.0], [2, 2.5], [2, 4.0], [2, 1.0], [2, 4.0], [2, 4.0], [2, 2.0], [2, 2.0], [2, 0.0], [2, 2.0], [2, 1.0], [2, 1.5], [2, 3.5], [2, 2.0], [2, 1.5], [2, 3.0], [2, 3.0]]
selectYearKmeann = []
gradeFromDBQQ = []
subjectSelected = []
numberOfGroup = []
checked = []
amountOfMenberInGroup = []
amountOfMenberInGroupC = []
# Pearson
gradeFromDBForPearson = []
selectYearPearsonn = []
subjectSelectedForPearson = []
subYearStudyPearson = []
allPearsonValue = []

# Predict
historySubject = []
historySubjectToPredict = []
historysGradeToPredictArr = []
gradeUsrArr = []
subjectsUsrArr = []
subjectChooseUsrArr = []
editSubjectToPredictGrade = []
detailPredicted = []


class page():

    # Go to page
    def firstPage(request):
        return render(request, 'start.html')

    def homePage(request):
        numberOfGroup.clear()
        amountOfMenberInGroup.clear()
        amountOfMenberInGroupC.clear()
        if 'name' in request.session:
            user = {
                'username': request.session['name'].get('usrname'),
                'userType': request.session['name'].get('userType')
            }
            return render(request, 'home.html', user)
        return render(request, 'home.html')

    @csrf_exempt
    def loginPage(request):
        if 'name' in request.session:
            return HttpResponseRedirect('/lecturer')
        return render(request, 'login.html')

    def gra(request):
        return render(request, 'showSubject.html')

    @csrf_exempt
    def register(request):
        print('--- inputUsername ---')
        print(request.POST.get('inputUsername'))
        if request.POST.get('inputUsername') is not None:
            usr = list(User.objects.filter(username = request.POST.get('inputUsername')).values())
            print('--- usr ---')
            print(usr)
            usrStd = list(UserStudent.objects.filter(studentID = request.POST.get('inputStudentID')).values())
            if usr == []:
                if usrStd == []:
                    addUsrName = User(
                        username = request.POST.get('inputUsername'), 
                        password = request.POST.get('inputPassword'),
                        userType_id = 2,
                    )
                    addUsrName.save()

                    usr = list(User.objects.filter(username = request.POST.get('inputUsername')).values())

                    addUsr = UserStudent(
                        username_id = usr[0].get('id'),
                        firstname = request.POST.get('inputFirstName'),
                        lastname = request.POST.get('inputLastName'),
                        studentID = request.POST.get('inputStudentID'),
                        gender = request.POST.get('gender'),
                        academicYear = request.POST.get('Academicyears'),
                        department = request.POST.get('Department'),
                    )
                    addUsr.save()
                    return HttpResponseRedirect('/regisSuccess')
                else:
                    resultCheckStdId = 'This student ID have been registered'
                    data = {
                        'resultCheckStdId': resultCheckStdId
                    }
                    render(request, 'register.html', data)
        resultCheckStdId = ''
        data = {
            'resultCheckStdId': resultCheckStdId
        }
        return render(request, 'register.html', data)


    @csrf_exempt    
    def regisSuccess(request):
        
        return render(request, 'Sucessful_register.html')


                # addGrade = GradeUserStudent(grade=request.POST.get(result.get('subjectNumber')), subject_id=result.get(
                #     'id'), userStudent_id=request.session['name'].get('userID'))
                # addGrade.save()


    @csrf_exempt
    def login(request):
        usernameInput = request.POST.get('username')
        passwordInput = request.POST.get('password')
        if usernameInput is not None and passwordInput is not None:
            usr = list(User.objects.all().values())
            for resultUsr in usr:
                if usernameInput == resultUsr.get('username'):
                    if passwordInput == resultUsr.get('password'):
                        # print('--- username ---')
                        # print(resultUsr.get('username'))
                        if resultUsr.get('userType_id') == 1:
                            request.session['name'] = {
                                'usrname': resultUsr.get('username'),
                                'userType': 'lecturer'
                            }
                        if resultUsr.get('userType_id') == 2:
                            usrStudent = list(UserStudent.objects.filter(
                                username__username=resultUsr.get('username')).values())
                            # print('--- usrStudent ---')
                            # print(usrStudent)
                            request.session['name'] = {
                                'usrname': resultUsr.get('username'),
                                'userType': 'student',
                                'userID': usrStudent[0].get('id'),
                                'firstname': usrStudent[0].get('firstname'),
                                'lastname': usrStudent[0].get('lastname'),
                                'studentID': usrStudent[0].get('studentID'),
                                'gender': usrStudent[0].get('gender'),
                                'academicYear': usrStudent[0].get('academicYear'),
                                'department': usrStudent[0].get('department'),
                            }
            if 'name' in request.session:
                # print("--- name ---")
                # print(request.session['name'])
                if request.session['name'].get('userType') == 'student':
                    return HttpResponseRedirect('/student')
                if request.session['name'].get('userType') == 'lecturer':
                    return HttpResponseRedirect('/lecturer')
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
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                user = {
                    'username': request.session['name'].get('usrname'),
                    'userType': request.session['name'].get('userType')
                }
                return render(request, 'Home_lecturer.html', user)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return render(request, 'login.html')

    @csrf_exempt
    def selectSubject(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                # Clear all
                checked = []
                gradeFromDBQQ.clear()
                subjectSelected.clear()
                numberOfGroup.clear()
                checked.clear()
                amountOfMenberInGroup.clear()
                amountOfMenberInGroupC.clear()

                subjects = []  # subjects from subjectObjects
                # Get list Subject from Database all subject
                if request.POST.get('GroupSubject') is None:
                    yearr = selectYearKmeann
                    y = []
                    for result in yearr:
                        yearOfSubject0 = list(SubjectYearStudy.objects.filter(
                            years__years=result).values())
                        y.append({
                            'year': result,
                            'subject': yearOfSubject0
                        })
                    te = []
                    first = []
                    for result in y:
                        print(result.get('year'))
                        # print(result.get('subject'))
                        for res in result.get('subject'):
                            print(res.get('subject_id'))
                        if first != []:
                            for res in result.get('subject'):
                                for a in first:
                                    if res.get('subject_id') == a:
                                        first.remove(a)
                                        first.append(a)
                        else:
                            for res in result.get('subject'):
                                first.append(res.get('subject_id'))

                    subjectObjects = []
                    for result in first:
                        idOfSubject = int(result)
                        sub = list(Subjects.objects.filter(
                            id=idOfSubject).values())
                        subjectObjects.append(sub[0])
                    # subjectObjects = list(Subjects.objects.all().values())
                    isubjectObjects = 0
                    while isubjectObjects <= subjectObjects.__len__() - 1:
                        tmp = subjectObjects[isubjectObjects].get(
                            'groupOfSubject_id')
                        if tmp == 1:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Programming'
                        if tmp == 2:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Database'
                        if tmp == 3:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Network'
                        if tmp == 4:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Management'
                        if tmp == 5:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Math'
                        if tmp == 6:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Other'
                        subjects.append(subjectObjects[isubjectObjects])
                        isubjectObjects = isubjectObjects + 1
                if request.POST.get('GroupSubject') is not None:
                    # Get list Subject from Database select group subject
                    # if request.POST.get('GroupSubject') is not None and request.POST.get('GroupSubject') != 'AllSubject':
                    #     # subjectObjects = list(Subjects.objects.filter(
                    #     #     groupOfSubject__groupOfSubject=request.POST.get('GroupSubject')).values())
                    #     isubjectObjects = 0
                    #     while isubjectObjects <= subjectObjects.__len__() - 1:
                    #         tmp = subjectObjects[isubjectObjects].get('groupOfSubject_id')
                    #         if tmp == 1:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Programming'
                    #         if tmp == 2:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Database'
                    #         if tmp == 3:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Network'
                    #         if tmp == 4:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Management'
                    #         if tmp == 5:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Math'
                    #         if tmp == 6:
                    #             subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Other'
                    #         subjects.append(subjectObjects[isubjectObjects])
                    #         isubjectObjects = isubjectObjects + 1

                    yearr = selectYearKmeann
                    y = []
                    for result in yearr:
                        yearOfSubject0 = list(SubjectYearStudy.objects.filter(
                            years__years=result).values())
                        y.append({
                            'year': result,
                            'subject': yearOfSubject0
                        })
                    te = []
                    first = []
                    for result in y:
                        # print(result.get('year'))
                        # print(result.get('subject'))
                        # for res in result.get('subject'):
                            # print(res.get('subject_id'))
                        if first != []:
                            for res in result.get('subject'):
                                for a in first:
                                    if res.get('subject_id') == a:
                                        first.remove(a)
                                        first.append(a)
                        else:
                            for res in result.get('subject'):
                                first.append(res.get('subject_id'))

                    subjectObjects = []
                    for result in first:
                        idOfSubject = int(result)
                        sub = list(Subjects.objects.filter(
                            id=idOfSubject).values())
                        subjectObjects.append(sub[0])
                    # subjectObjects = list(Subjects.objects.all().values())
                    isubjectObjects = 0
                    while isubjectObjects <= subjectObjects.__len__() - 1:
                        tmp = subjectObjects[isubjectObjects].get(
                            'groupOfSubject_id')
                        if tmp == 1:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Programming'
                        if tmp == 2:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Database'
                        if tmp == 3:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Network'
                        if tmp == 4:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Management'
                        if tmp == 5:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Math'
                        if tmp == 6:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Other'
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
                group = ''
                if request.POST.get('GroupSubject') is not None:
                    group = request.POST.get('GroupSubject')
                if request.POST.get('GroupSubject') is not None and request.POST.get('GroupSubject') == 'AllSubject':
                    group = ''              
                subb = {
                    "subjects": subjects,
                    "years": yearr,
                    'username': request.session['name'].get('usrname'),
                    'group': group
                }
                print('--- group ---')
                print(group)
                # When choose subjects
                # checked = []
                j = 0
                if request.POST.get('GroupSubject') is None:
                    while j <= subjects.__len__() - 1:
                        if request.POST.get(subjectObjects[j].get('subjectNumber')) is not None:
                            checked.append(request.POST.get(
                                subjectObjects[j].get('subjectNumber')))
                        j = j + 1
                if checked != []:
                    # Get data form Database
                    print('--- selectYearKmeann ---')
                    print(selectYearKmeann)
                    subjectss = []
                    for result in checked:
                        subjectss.append({
                            "subjectNumber": result,
                            "gradeSubject": list(Grade.objects.filter(
                                students__academicYears__years=selectYearKmeann[0],
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
                        d.update({result.get('sub'): pd.Series(ddd)})

                    df = pd.DataFrame(d)
                    gradeFromDBQQ.append(df)
                    # print("--- df ---")
                    # print(type(df))
                    # print(df)
                    # print(gradeData())
                    # print("--- subjectSelected ---")
                    # print(type(request.session['name'].get('gradeFromDBQQ')))
                    # print(request.session['name'].get('gradeFromDBQQ'))
                    return HttpResponseRedirect('/selectYearKmean/selectSubject/showGraphKmean')

                return render(request, 'showSubject.html', subb)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    def kmeamAlg(self):
        total = 21
        i = 2
        silh_score = []

        gradeFromDB0 = gradeFromDBQQ[0]
        # print('--- request.session ---')
        # print(request.session['name'].get('gradeFromDBQQ'))
        # gradeFromDB0 = request.session['name'].get('gradeFromDBQQ')
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

    def findMaxSilhScore(self):
        silh_score = page().kmeamAlg()
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

    def clusterCenterWhenGetMaxValue(self):
        maxValue = page().findMaxSilhScore()
        checked.clear()
        checked.append(maxValue)
        gradeFromDB0 = gradeFromDBQQ[0]
        # gradeFromDB0 = request.session['name'].get('gradeFromDBQQ')[0]
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

    def chooseGroup(self, group):
        clf = KMeans(n_clusters=group)
        # Clear value amountOfMenberInGroupC
        amountOfMenberInGroupC.append('None')
        amountOfMenberInGroupC.clear()
        checked.clear()
        checked.append(group)
        gradeFromDB0 = gradeFromDBQQ[0]
        gradeFromDB = gradeFromDB0[subjectSelected]
        clf.fit(gradeFromDB)
        amountOfMenber = {i: np.where(clf.labels_ == i)[
            0] for i in range(group)}
        iinwhile = 0
        while iinwhile < amountOfMenber.__len__():
            amount = 0
            for i in amountOfMenber.get(iinwhile):
                amount = amount + 1
            amountOfMenberInGroupC.append([iinwhile + 1, amount])
            iinwhile = iinwhile + 1

        return clf.cluster_centers_.tolist()

    def myformat(self, x):
        return ('%.4f' % x).rstrip('.')

    @csrf_exempt
    def showGeaphOfCluster(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                amountOfMenberInGroup.clear()
                cluterCenterFromKmeans0 = page()
                if request.POST.get('group') is None:
                    cluterCenterFromKmeans = cluterCenterFromKmeans0.clusterCenterWhenGetMaxValue()

                    # Find number of group and values
                    p = 0
                    numGroup = []
                    valueGroup = []
                    while p < numberOfGroup[0].__len__():
                        numGroup.append(numberOfGroup[0][p][0])
                        valueGroup.append(page().myformat(numberOfGroup[0][p][1]))
                        p = p + 1

                    # Number of member in each group
                    # eachGroup = []
                    # amountMem = []
                    groupAndAmountMem = []
                    for result in amountOfMenberInGroup:
                        groupAndAmountMem.append({
                            'eachGroup': result[0],
                            'amountMem': result[1]
                        })
                        # eachGroup.append(result[0])
                        # amountMem.append(result[1])

                    data = {
                        "labels": subjectSelected,
                        "data": cluterCenterFromKmeans,
                        "checked": checked[0],
                        "numGroup": numGroup,
                        "valueGroup": valueGroup,
                        "groupAndAmountMem": groupAndAmountMem,
                        # "group": eachGroup,
                        # "numOfMember": amountMem,
                        "selectYearKmeann": selectYearKmeann,
                        'username': request.session['name'].get('usrname')
                    }
                    return render(request, 'GraphallSoneY.html', data)
                if request.POST.get('group') is not None:
                    # Find number of group and values
                    p = 0
                    numGroup = []
                    valueGroup = []
                    while p < numberOfGroup[0].__len__():
                        numGroup.append(numberOfGroup[0][p][0])
                        valueGroup.append(page().myformat(numberOfGroup[0][p][1]))
                        p = p + 1

                    # Call chooseGroup when select group by self
                    choose = page().chooseGroup(int(request.POST.get('group')))

                    # Number of member in each group at another time
                    # eachGroup = []
                    # amountMem = []
                    groupAndAmountMem = []
                    for result in amountOfMenberInGroupC:
                        groupAndAmountMem.append({
                            'eachGroup': result[0],
                            'amountMem': result[1]
                        })
                    # eachGroup.append(result[0])
                    # amountMem.append(result[1])

                    data = {
                        "labels": subjectSelected,
                        "data": choose,
                        "checked": checked[0],
                        "numGroup": numGroup,
                        "valueGroup": valueGroup,
                        "groupAndAmountMem": groupAndAmountMem,
                        # "group": eachGroup,
                        # "numOfMember": amountMem,
                        "selectYearKmeann": selectYearKmeann,
                        'username': request.session['name'].get('usrname')
                    }
                    return render(request, 'GraphallSoneY.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    def get_data(request, *args, **kwargs):

        # labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]

        # levels = LevelEducation.objects.all().values()
        # s = ['INT101', 'INT102']
        # curriculums = []
        # for result in s:
        #     curriculums.append({
        #         "sub": result,
        #         "subb": list(Grade.objects.filter(
        #             students__academicYears__years='2555',
        #             subjects__subjectNumber=result).values()
        #         )
        #     })

        # gradee = []
        # for result in curriculums:
        #     ddd = []
        #     countResult = 1
        #     for result1 in result.get('subb'):
        #         ddd.append(countResult)
        #         ddd.append(result1.get('grade'))
        #         gradee.append(ddd)
        #         if ddd != None:
        #             ddd = []
        #         # print(countResult)
        #         # print(result1.get('grade'))
        #         countResult = countResult + 1
        # print("--- geadeee ---")
        # print(gradee)
        # d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']), }

        # subjects = list(Subjects.objects.all().values())

        # data = {
        #     # "labels": labels,
        #     # "defaultData": [1, 2, 3, 4, 5, 6],
        #     # "level": list(levels),
        #     "curriculums": curriculums,
        #     # "subject": subjects
        # }

        # Peason

        # if True:
        #     # Get data form Database
        #     checked = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
        #     subjectss = []
        #     for result in checked:
        #         subjectss.append({
        #             "subjectNumber": result,
        #             "gradeSubject": list(Grade.objects.filter(
        #                 students__academicYears__years='2555',
        #                 subjects__subjectNumber=result).values()
        #             )
        #         })
        #     # Make data to equal data
        #     tmp = 1000000000
        #     for result in subjectss:
        #         if result.get('gradeSubject').__len__() < tmp:
        #             tmp = result.get('gradeSubject').__len__()
        #     arr = []
        #     for result in subjectss:
        #         array = result.get('gradeSubject')
        #         res = array.__len__() - tmp
        #         if res != 0:
        #             while res > 0:
        #                 array.remove(array[array.__len__()-1])
        #                 res = res - 1
        #         arr.append({
        #             'sub': result.get('subjectNumber'),
        #             'subb': array
        #         })

        #     d = {}
        #     subjectSelected.clear()
        #     for result in arr:
        #         ddd = []
        #         subjectSelected.append(result.get('sub'))
        #         for result1 in result.get('subb'):
        #             ddd.append(result1.get('grade'))
        #         # print(ddd)
        #         d.update({result.get('sub'): pd.Series(ddd)})

        #     df = pd.DataFrame(d)
        #     # gradeFromDBQQ.append(df)
        #     print("--- df ---")
        #     print(type(df))
        #     print(df)

        #     subSelect = 'INT101'
        #     sub = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
        #     re = []
        #     for result in sub:
        #         pearsonr_coefficient, p_value = pearsonr(df[subSelect], df[result])
        #         if pearsonr_coefficient.item() >= 0.1 and pearsonr_coefficient.item() != 1:
        #             re.append({
        #                 'subject1': subSelect,
        #                 'subject2': result,
        #                 'value': pearsonr_coefficient.item()
        #             })
        #     print(re)

        #     data = {
        #         # "labels": labels,
        #         # "defaultData": [1, 2, 3, 4, 5, 6],
        #         # "level": list(levels),
        #         "curriculums": re,
        #         # "subject": subjects
        #     }

        yearr = ['2555', '2559']
        y = []
        for result in yearr:
            yearOfSubject0 = list(SubjectYearStudy.objects.filter(
                years__years=result).values())
            y.append({
                'year': result,
                'subject': yearOfSubject0
            })
        te = []
        first = []
        for result in y:
            print(result.get('year'))
            # print(result.get('subject'))
            for res in result.get('subject'):
                print(res.get('subject_id'))
            if first != []:
                for res in result.get('subject'):
                    for a in first:
                        if res.get('subject_id') == a:
                            first.remove(a)
                            first.append(a)
            else:
                for res in result.get('subject'):
                    first.append(res.get('subject_id'))

                # if te == []:
                #     # print('if te is None:')
                #     te.append(res.get('subject_id'))
                # else:

                #     # print('if te is not None:')
                #     for ress in te:
                #         print('------')
                #         if ress != res.get('subject_id'):
                #             te.append(res.get('subject_id'))

        print(first)

        data = {
            "yearOfSubject0": y
        }
        return JsonResponse(data)

    @csrf_exempt
    def selectYearPreason(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                if request.POST.get('year') is not None:
                    gradeFromDBForPearson.clear()
                    selectYearPearsonn.clear()
                    subjectSelectedForPearson.clear()
                    subYearStudyPearson.clear()
                    selectYearPearsonn.append(request.POST.get('year'))
                    return HttpResponseRedirect('/selectYearPreason/selectSubjectPreason')
                subb = {
                    'username': request.session['name'].get('usrname')
                }
                return render(request, 'chooseYear_pearson.html', subb)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/login')

    @csrf_exempt
    def selectYearKmean(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':            
                # if 'name' in request.session:
                selectYearKmeann.clear()
                yr = ['2555', '2556', '2557', '2558', '2559', '2560', '2561']
                # for result in yr:
                #     if request.POST.get(result) is not None:
                #         selectYearKmeann.append(request.POST.get(result))

                if request.POST.get('yearrr') is not None:
                    selectYearKmeann.append(request.POST.get('yearrr'))

                if selectYearKmeann != []:
                    return HttpResponseRedirect('/selectYearKmean/selectSubject')

                subb = {
                    'username': request.session['name'].get('usrname'),
                    # 'username': "Nawat"
                }
                # print(selectYearKmeann)
                return render(request, 'chooseYear_kmean.html', subb)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/login')

    @csrf_exempt
    def selectSubjectPreason(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                if request.POST.get('subj') is None:
                    gradeFromDBForPearson.clear()
                    subjectSelectedForPearson.clear()
                    subYearStudyPearson.clear()
                    year = selectYearPearsonn[0]
                    # subjectObjects = list(Subjects.objects.raw('SELECT * FROM AnalyzeGrade_subjects JOIN AnalyzeGrade_subjectyearstudy'))
                    yearOfSubject = list(SubjectYearStudy.objects.filter(
                        years__years=year).values())
                    subjectObjects = []
                    for result in yearOfSubject:
                        idOfSubject = int(result.get('subject_id'))
                        sub = list(Subjects.objects.filter(
                            id=idOfSubject).values())
                        subjectObjects.append(sub[0])
                    isubjectObjects = 0
                    subjects = []
                    while isubjectObjects <= subjectObjects.__len__() - 1:
                        tmp = subjectObjects[isubjectObjects].get(
                            'groupOfSubject_id')
                        if tmp == 1:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Programming'
                        if tmp == 2:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Network'
                        if tmp == 3:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Database'
                        if tmp == 4:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Management'
                        if tmp == 5:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Math'
                        if tmp == 6:
                            subjectObjects[isubjectObjects]['groupOfSubject_id'] = 'Other'
                        subjects.append(subjectObjects[isubjectObjects])
                        isubjectObjects = isubjectObjects + 1

                    # Put subject that study into subYearStudyPearson
                    subYearStudyPearson.clear()
                    for result in subjects:
                        subYearStudyPearson.append(result.get('subjectNumber'))
                    print('--- subjects ---')
                    print(subYearStudyPearson)
                    # print(type(subYearStudyPearson[0]))

                    group = ''
                    if request.POST.get('GroupSubject') is not None:
                        if request.POST.get('GroupSubject') != 'AllSubject':
                            group = request.POST.get('GroupSubject')

                    subb = {
                        "subjects": subjects,
                        "years": year,
                        'username': request.session['name'].get('usrname'),
                        'group': group,
                        'selectYearPearsonn': selectYearPearsonn[0]
                    }
                    return render(request, 'ChooseSubjects_pearson.html', subb)
                if request.POST.get('subj') is not None:
                    # subYearStudyPearson.append(subjects[])
                    subjectSelectedForPearson.append(request.POST.get('subj'))
                    return HttpResponseRedirect('/selectYearPreason/selectSubjectPreason/showGraphPearson')
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/login')

    @csrf_exempt
    def showGraphPearson(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                
                # Get data form Database
                subYearStudy = subYearStudyPearson
                # subYearStudy = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
                subjectss = []
                for result in subYearStudy:
                    subjectss.append({
                        "subjectNumber": result,
                        "gradeSubject": list(Grade.objects.filter(
                            students__academicYears__years=selectYearPearsonn[0],
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
                # Make data frame
                d = {}
                for result in arr:
                    ddd = []
                    for result1 in result.get('subb'):
                        ddd.append(result1.get('grade'))
                    d.update({result.get('sub'): pd.Series(ddd)})
                df = pd.DataFrame(d)
                gradeFromDBForPearson.append(df)

                # Find Pearson
                subSelect = subjectSelectedForPearson[0]
                # sub = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
                res = []
                gradeFromDBForPearsonSelf = gradeFromDBForPearson[0]
                allPearsonValue.clear()
                for result in subYearStudy:
                    pearsonr_coefficient, p_value = pearsonr(
                        gradeFromDBForPearsonSelf[subSelect], gradeFromDBForPearsonSelf[result])
                    if pearsonr_coefficient.item() >= 0.1 and pearsonr_coefficient.item() != 1:
                        res.append({
                            'subject1': subSelect,
                            'subject2': result,
                            'value': pearsonr_coefficient.item()
                        })
                    allPearsonValue.append({
                        'subject1': subSelect,
                        'subject2': result,
                        'value': page().myformatForpearson(pearsonr_coefficient.item())
                    })
                subject1 = []
                subject2 = []
                value = []
                for result in res:
                    subject1.append(result.get('subject1'))
                    subject2.append(result.get('subject2'))
                    value.append(result.get('value'))
                # print("--- print(re) ---")
                # print(re)

                sentToGraph = {
                    'labels': subject2,
                    'value': value,
                    'subject1': subject1[0],
                    'username': request.session['name'].get('usrname'),
                }

                print('--- allPearsonValue ---')
                print(allPearsonValue)
                return render(request, 'GraphPearson.html', sentToGraph)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/login')
        
    
    def myformatForpearson(self, x):
        return ('%.4f' % x).rstrip('.')


    def showAllPearson(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'lecturer':
                data = {
                    'allpearson': allPearsonValue
                }
                return render(request, 'showAllPearson.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    def ggg(request):
        return render(request, 'GraphPearson.html')

    def logout(request):
        if 'name' in request.session:
            del request.session['name']
        else:
            return HttpResponseRedirect('/Home/')
        return HttpResponseRedirect('/Home/')

    # Predict

    def profileStu(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                usrbInDB = list(UserStudent.objects.filter(username__username=request.session['name'].get('usrname')).values())
                user = {
                    'username': request.session['name'].get('usrname'),
                    'firstname':usrbInDB[0].get('firstname'),
                    'lastname':usrbInDB[0].get('lastname'),
                    'studentID':usrbInDB[0].get('studentID'),
                    'gender':usrbInDB[0].get('gender'),
                    'academicYear':usrbInDB[0].get('academicYear'),
                    'department':usrbInDB[0].get('department'),
                }
                return render(request, 'profileStudent.html', user)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    def Home_studentPage(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                user = {
                    'username': request.session['name'].get('usrname')
                }
                return render(request, 'Home_student.html', user)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    def historyGrade(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                gradeUserStudent = list(GradeUserStudent.objects.filter(
                    userStudent__username__username=request.session['name'].get('usrname')).values())
                # print('--- gradeUserStudent ---')
                # print(gradeUserStudent)
                historySubject.clear()
                datas = []
                for result in gradeUserStudent:
                    subInDB = list(Subjects.objects.filter(
                        id=result.get('subject_id')).values())
                    historySubject.append(subInDB[0].get('subjectNumber'))
                    
                    gradeStr = ''
                    if result.get('grade') == 4:
                        gradeStr = 'A'
                    if result.get('grade') == 3.5:
                        gradeStr = 'B+'
                    if result.get('grade') == 3:
                        gradeStr = 'B'
                    if result.get('grade') == 2.5:
                        gradeStr = 'C+'
                    if result.get('grade') == 2:
                        gradeStr = 'C'
                    if result.get('grade') == 1.5:
                        gradeStr = 'D+'
                    if result.get('grade') == 1:
                        gradeStr = 'D'
                    if result.get('grade') == 0:
                        gradeStr = 'F'

                    data = {
                        # 'grade': result.get('grade'),
                        'grade': gradeStr,
                        'subjectNumber': subInDB[0].get('subjectNumber'),
                        'subjectName': subInDB[0].get('subjectName'),
                        'credit': subInDB[0].get('credit'),
                    }
                    datas.append(data)

                showData = {
                    'username': request.session['name'].get('usrname'),
                    'datas': datas
                }
                return render(request, 'historysGrade.html', showData)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    @csrf_exempt
    def insertSubject(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                historySubjectSelf = historySubject
                subjects = list(Subjects.objects.all().values())

                for result in historySubjectSelf:
                    for result1 in subjects:
                        if result == result1.get('subjectNumber'):
                            subjects.remove(result1)

                data = {
                    'username': request.session['name'].get('usrname'),
                    'subjects': subjects
                }

                subj = []
                for result in subjects:
                    if request.POST.get(result.get('subjectNumber')) is not None and request.POST.get(result.get('subjectName')) == 'on' and request.POST.get(result.get('subjectNumber')) != "5":
                        request.POST.get(result.get('subjectNumber'))
                        subj.append({
                            'grade': request.POST.get(result.get('subjectNumber')),
                            'subject_id': result.get('id'),
                            'userStudent_id': request.session['name'].get('userID'),
                        })

                    if request.POST.get(result.get('subjectNumber')) is not None and request.POST.get(result.get('subjectName')) == 'on' and request.POST.get(result.get('subjectNumber')) == "5":
                        data = {
                            'username': request.session['name'].get('usrname'), 
                            'subjects': subjects,
                            'error': "errorNull"
                        }

                if subj != []:
                    count = 0
                    for result in subj:
                        addGrade = GradeUserStudent(
                            grade=result.get('grade'),
                            subject_id=result.get('subject_id'), 
                            userStudent_id=result.get('userStudent_id'),
                        )
                        addGrade.save()
                        count = count + 1
                    
                    print('--- count ---')
                    print(count)
                    if count == subj.__len__():
                        return HttpResponseRedirect('/historyGrade')
                return render(request, 'insertSubject.html', data)
            else:
                return HttpResponseRedirect('/Home/')                
        else:
            return HttpResponseRedirect('/loginn')


    @csrf_exempt            
    def historysGradeToPredict(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                subjectsUsrArr.clear()
                historysGradeToPredictArr.clear()
                gradeUserStudent = list(GradeUserStudent.objects.filter(
                    userStudent__username__username=request.session['name'].get('usrname')).values())
                # print('--- gradeUserStudent ---')
                # print(gradeUserStudent)
                gradeUsrArr.clear()
                datas = []
                count = 1
                amountSub = 1
                for result in gradeUserStudent:
                    subInDB = list(Subjects.objects.filter(
                        id=result.get('subject_id')).values())
                    historysGradeToPredictArr.append(subInDB[0].get('subjectNumber'))
                    gradeStr = ''
                    if result.get('grade') == 4:
                        gradeStr = 'A'
                    if result.get('grade') == 3.5:
                        gradeStr = 'B+'
                    if result.get('grade') == 3:
                        gradeStr = 'B'
                    if result.get('grade') == 2.5:
                        gradeStr = 'C+'
                    if result.get('grade') == 2:
                        gradeStr = 'C'
                    if result.get('grade') == 1.5:
                        gradeStr = 'D+'
                    if result.get('grade') == 1:
                        gradeStr = 'D'
                    if result.get('grade') == 0:
                        gradeStr = 'F'
                    data = {
                        # 'grade': result.get('grade'),
                        'grade': gradeStr,
                        'subjectNumber': subInDB[0].get('subjectNumber'),
                        'subjectName': subInDB[0].get('subjectName'),
                        'credit': subInDB[0].get('credit'),
                        'count': str(count)
                    }
                    dataa = {
                        'grade': result.get('grade'),
                        # 'grade': gradeStr,
                        'subjectNumber': subInDB[0].get('subjectNumber'),
                        'subjectName': subInDB[0].get('subjectName'),
                        'credit': subInDB[0].get('credit'),
                        'count': str(count)
                    }
                    datas.append(data)
                    gradeUsrArr.append(dataa)
                    subjectsUsrArr.append(subInDB[0].get('subjectNumber'))
                    amountSub = amountSub + 1
                    count = count + 1
                showData = {
                    'username': request.session['name'].get('usrname'),
                    'datas': datas,
                    'checkAmountOfSubject': amountSub
                }
                return render(request, 'stepbyStudent1.html', showData)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')


    @csrf_exempt
    def insertSubjectToPredict(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                historySubjectSelf = historysGradeToPredictArr
                subjects = list(Subjects.objects.all().values())

                for result in historySubjectSelf:
                    for result1 in subjects:
                        if result == result1.get('subjectNumber'):
                            subjects.remove(result1)

                data = {
                    'username': request.session['name'].get('usrname'),
                    'subjects': subjects,
                    'error':''
                }
                
                subj = []
                for result in subjects:
                    if request.POST.get(result.get('subjectNumber')) is not None and request.POST.get(result.get('subjectName')) == 'on' and request.POST.get(result.get('subjectNumber')) != '5':
                        request.POST.get(result.get('subjectNumber'))
                        subj.append({
                            'grade': request.POST.get(result.get('subjectNumber')),
                            'subject_id': result.get('id'),
                            'userStudent_id': request.session['name'].get('userID'),
                        })
                    
                    if request.POST.get(result.get('subjectNumber')) is not None and request.POST.get(result.get('subjectName')) == 'on' and request.POST.get(result.get('subjectNumber')) == "5":
                        data = {
                            'username': request.session['name'].get('usrname'), 
                            'subjects': subjects,
                            'error': "errorNull"
                        }
                        return render(request, 'insertSubjectToPredict.html', data) 
                        # addGrade = GradeUserStudent(grade=request.POST.get(result.get('subjectNumber')), subject_id=result.get(
                        #     'id'), userStudent_id=request.session['name'].get('userID'))
                        # addGrade.save()
                        # return HttpResponseRedirect('/historysGradeToPredict')
                        # print('--- print(addGrade)---')
                        # print(addGrade)

                if subj != []:
                    count = 0
                    for result in subj:
                        addGrade = GradeUserStudent(
                            grade=result.get('grade'),
                            subject_id=result.get('subject_id'), 
                            userStudent_id=result.get('userStudent_id'),
                        )
                        addGrade.save()
                        count = count + 1
                    
                    print('--- count ---')
                    print(count)
                    if count == subj.__len__():
                        return HttpResponseRedirect('/historysGradeToPredict')
                return render(request, 'insertSubjectToPredict.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')

    @csrf_exempt
    def chooseSubjectAsPredict(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                subjectChooseUsrArr.clear()
                historysGradeToPredictArrSelf = historysGradeToPredictArr
                subjects = list(Subjects.objects.all().values())
                for result in historysGradeToPredictArrSelf:
                    for result1 in subjects:
                        if result == result1.get('subjectNumber'):
                            subjects.remove(result1)
                data = {
                    'username': request.session['name'].get('usrname'),
                    'subjects': subjects
                }
                if request.POST.get('subject') is not None:
                    subjectChooseUsrArr.append(request.POST.get('subject'))
                # for result in subjects:
                    #  if request.POST.get(result.get('subjectNumber')) is not None:
                        # subjectChooseUsrArr.append(result)
                        # print('-------------------acgdgluadvi --------------')
                    # return HttpResponseRedirect('/testPredict')
                    return HttpResponseRedirect('/historysGradeToPredict/chooseSubjectAsPredict/predictGrade')
                return render(request, 'stepbyStudent2.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')


    @csrf_exempt
    def predictGrate(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                gradeFromDBForPearson.clear()
                # Get data form Database
                # historysGradeToPredictArrSelf = historysGradeToPredictArr
                # historysGradeToPredictArrSelf = ['INT101', 'INT102', 'INT104', 'INT105', 'INT106', 'INT107', 'INT303']
                historysGradeToPredictArrSelf = []
                for result in subjectsUsrArr:
                    historysGradeToPredictArrSelf.append(result)
                historysGradeToPredictArrSelf.append(subjectChooseUsrArr[0])
                print('--- subjectChooseUsrArr[0].get subjectNumber ---')
                print(subjectChooseUsrArr[0])            
                print('--- historysGradeToPredictArrSelf ---')
                print(historysGradeToPredictArrSelf)


                # subYearStudy = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
                subjectss = []
                for result in historysGradeToPredictArrSelf:
                    subjectss.append({
                        "subjectNumber": result,
                        "gradeSubject": list(Grade.objects.filter(
                            students__academicYears__years='2556',
                            subjects__subjectNumber=result).values()
                        )
                    })
                # Make data to equal data
                # print('--- subjectss1111111 ---')
                # print(subjectss)
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
                # Make data frame
                d = {}
                for result in arr:
                    ddd = []
                    for result1 in result.get('subb'):
                        ddd.append(result1.get('grade'))
                    d.update({result.get('sub'): pd.Series(ddd)})
                df = pd.DataFrame(d)
                gradeFromDBForPearson.append(df)
                # print('--- gradeFromDBForPearson1111111111 ---')
                # print(gradeFromDBForPearson)

                # Find Pearson
                # subSelect = subjectSelectedForPearson[0]
                # subSelect = 'INT303'
                subSelect = subjectChooseUsrArr[0]
                # sub = ['INT101','INT102','INT103','INT104','INT105','INT106','INT107','INT201','INT202','INT203','INT204','INT205','INT206','INT207','INT301','INT302','INT303','INT304','INT305','INT306','INT307','INT351','INT352','INT401','INT402','INT450','INT451']
                res = []
                gradeFromDBForPearsonSelf = gradeFromDBForPearson[0]
                # print('--- gradeFromDBForPearsonSelf1111111111111111 ---')
                # print(gradeFromDBForPearsonSelf)
                for result in historysGradeToPredictArrSelf:
                    pearsonr_coefficient, p_value = pearsonr(
                        gradeFromDBForPearsonSelf[subSelect], gradeFromDBForPearsonSelf[result])
                    if pearsonr_coefficient.item() >= 0 and pearsonr_coefficient.item() != 1:
                    # if pearsonr_coefficient.item() != 1:
                        res.append({
                            'subject1': subSelect,
                            'subject2': result,
                            'value': pearsonr_coefficient.item()
                        })
                # print(res)
                # subject1 = []
                # subject2 = []
                # value = []
                ress = []
                if res.__len__() < 3:
                    resLen = res.__len__()
                else:
                    resLen = 3
                iForFindTop = 1
                while iForFindTop <= resLen:
                    print('--- res ---')
                    print(res)
                    tmp = 0
                    for result in res:
                        if tmp <= result.get('value'):
                            tmp = result.get('value')

                    for result1 in res:
                        if tmp == result1.get('value'):
                            ress.append({
                                'subject1': result1.get('subject1'),
                                'subject2': result1.get('subject2'),
                                'value': result1.get('value'),
                            })
                            res.remove(result1)
                    iForFindTop = iForFindTop + 1

                # Send values to showDetailPredict()
                detailPredicted.clear()
                detailPredicted.append({
                    'subjectsValue': ress
                })
                # print('--- ress ---')
                # print(ress)

                        # subject1.append(result.get('subject2'))
                        # subject2.append(result.get('subject2'))
                        # value.append(result.get('value'))



                # Data Test
                # gradeUsrStu = [
                #     {
                #         'subjectNumber': 'INT101',
                #         'grade': 4
                #     },
                #     {
                #         'subjectNumber': 'INT102',
                #         'grade': 2.5
                #     },
                #     {
                #         'subjectNumber': 'INT104',
                #         'grade': 3
                #     },
                #     {
                #         'subjectNumber': 'INT105',
                #         'grade': 3
                #     },
                #     {
                #         'subjectNumber': 'INT106',
                #         'grade': 3.5
                #     },
                #     {
                #         'subjectNumber': 'INT106',
                #         'grade': 3
                #     },
                # ]
                

                prea = ress
                sumgradeNPear = 0
                sumValuePearson = 0

                for resultPrea in prea:
                    # for resultGradeUsrStu in gradeUsrStu:
                    for resultGradeUsrStu in gradeUsrArr:
                        if resultPrea.get('subject2') == resultGradeUsrStu.get('subjectNumber'):
                            # print('--- resultPrea.get("subject2") ---')
                            # print(resultPrea.get('subject2'))
                            # print('--- resultGradeUsrStu.get("subjectNumber") ---')
                            # print(resultGradeUsrStu.get('subjectNumber'))
                            resP = resultPrea.get('value') * resultGradeUsrStu.get('grade')
                            sumgradeNPear = sumgradeNPear + resP
                            sumValuePearson = sumValuePearson + resultPrea.get('value')

                resultPredict = 0
                if sumgradeNPear != 0 and sumValuePearson != 0:
                    resultPredict = sumgradeNPear / sumValuePearson
                    # print('--- resultPredict ---')
                    # print(resultPredict)

                resultPredictChar = ''
                if resultPredict >= 1 and resultPredict <= 1.24:
                    resultPredictChar = 'D'
                if resultPredict >= 1.25 and resultPredict <= 1.74:
                    resultPredictChar = 'D+'
                if resultPredict >= 1.75 and resultPredict <= 2.24:
                    resultPredictChar = "C"
                if resultPredict >= 2.25 and resultPredict <= 2.74:
                    resultPredictChar = "C+"
                if resultPredict >= 2.75 and resultPredict <= 3.24:
                    resultPredictChar = "B"
                if resultPredict >= 3.25 and resultPredict <= 3.74:
                    resultPredictChar = "B+"
                if resultPredict >= 3.75 and resultPredict <= 4:
                    resultPredictChar = "A"

                sub = list(Subjects.objects.filter(subjectNumber = subSelect).values())

                # print('--- subjectNumber ---')
                # print(sub[0].get('subjectNumber'))
                # print('--- subjectName ---')
                # print(sub[0].get('subjectName'))
                # print('--- credit ---')
                # print(sub[0].get('credit'))
                # print('--- resultPredict ---')
                # print(resultPredict)
                # data = {}
                data = {
                    'username': request.session['name'].get('usrname'),
                    'subjectNumber': sub[0].get('subjectNumber'),
                    'subjectName': sub[0].get('subjectName'),
                    'subjectCredit': sub[0].get('credit'),
                    'resultPredict': resultPredictChar
                }
                return render(request, 'stepbyStudent3.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')
    

    def showDetailPredict(request):
        detailPredictedSelf = detailPredicted[0].get('subjectsValue')
        print('--- detailPredictedSelf ---')
        print(detailPredictedSelf)

        data = {
            'username': request.session['name'].get('usrname'),
            'detailPredicted': detailPredictedSelf
        }
        return render(request, 'stepbyStudent3_ShowDetail.html', data)


    @csrf_exempt
    def delect(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':  
                editSubjectToPredictGrade.clear()          
                subjects = list(Subjects.objects.all().values())
                deOrEd = 'edit'
                subDe = []
                for result in subjects:
                    if request.POST.get(result.get('subjectNumber')) == 'delete':
                        subDe.append(result.get('id'))
                        deOrEd = 'delete'
                if subDe != []:
                    usrGrade = GradeUserStudent.objects.filter(
                        userStudent = request.session['name'].get('userID'),
                        subject = subDe[0]
                    )
                    usrGrade.delete()


                # Edit
                if deOrEd == 'edit':
                    editSubjectToPredictGrade.clear()
                    for result in subjects:
                        if request.POST.get(result.get('subjectNumber')) == 'edit':
                            gradeUsrStd = list(GradeUserStudent.objects.filter(
                                userStudent = request.session['name'].get('userID'),
                                subject = result.get('id')
                            ).values())
                            # editSubjectToPredictGrade.append(gradeUsrStd)

                            editSubjectToPredictGrade.append({
                                'subjectNumber': result.get('subjectNumber'),
                                'subjectName': result.get('subjectName'),
                                'credit': result.get('credit'),
                                'id': result.get('id'),
                                'grade': gradeUsrStd[0].get('grade'),
                                'gradeId': gradeUsrStd[0].get('id')
                            })
                            return HttpResponseRedirect('/editSubject')
                return HttpResponseRedirect('/historysGradeToPredict')
                # return render(request, 'stepbyStudent1.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')



    @csrf_exempt    
    def editToPredictGrade(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                dataSelf = editSubjectToPredictGrade[0]
                gradeStr = ''
                if dataSelf.get('grade') == 4:
                    gradeStr = 'A'
                if dataSelf.get('grade') == 3.5:
                    gradeStr = 'B+'
                if dataSelf.get('grade') == 3:
                    gradeStr = 'B'
                if dataSelf.get('grade') == 2.5:
                    gradeStr = 'C+'
                if dataSelf.get('grade') == 2:
                    gradeStr = 'C'
                if dataSelf.get('grade') == 1.5:
                    gradeStr = 'D+'
                if dataSelf.get('grade') == 1:
                    gradeStr = 'D'
                if dataSelf.get('grade') == 0:
                    gradeStr = 'F'
                data = {
                    'subjectNumber': dataSelf.get('subjectNumber'),
                    'subjectName': dataSelf.get('subjectName'),
                    'credit': dataSelf.get('credit'),
                    'grade': gradeStr,
                }

                if request.POST.get('subGrade') is not None:
                    gradeStd = GradeUserStudent.objects.get(id=dataSelf.get('gradeId'))
                    gradeStd.grade = request.POST.get('subGrade')
                    gradeStd.save()
                    return HttpResponseRedirect('/historysGradeToPredict')
                return render(request, 'EditToPredictGrade.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')


    @csrf_exempt
    def delectTrans(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                subjects = list(Subjects.objects.all().values())
                
                deOrEd = 'edit'
                subDe = []
                for result in subjects:
                    if request.POST.get(result.get('subjectNumber')) == 'delete':
                        subDe.append(result.get('id'))
                        deOrEd = 'delete'
                if subDe != []:
                    usrGrade = GradeUserStudent.objects.filter(
                        userStudent = request.session['name'].get('userID'),
                        subject = subDe[0]
                    )
                    usrGrade.delete()

                # Edit
                if deOrEd == 'edit':
                    editSubjectToPredictGrade.clear()
                    for result in subjects:
                        if request.POST.get(result.get('subjectNumber')) == 'edit':
                            gradeUsrStd = list(GradeUserStudent.objects.filter(
                                userStudent = request.session['name'].get('userID'),
                                subject = result.get('id')
                            ).values())
                            # editSubjectToPredictGrade.append(gradeUsrStd)

                            editSubjectToPredictGrade.append({
                                'subjectNumber': result.get('subjectNumber'),
                                'subjectName': result.get('subjectName'),
                                'credit': result.get('credit'),
                                'id': result.get('id'),
                                'grade': gradeUsrStd[0].get('grade'),
                                'gradeId': gradeUsrStd[0].get('id')
                            })
                            return HttpResponseRedirect('/historyGrade/editTransGrade')
                return HttpResponseRedirect('/historyGrade')
                # return render(request, 'stepbyStudent1.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')


    @csrf_exempt    
    def editTransGrade(request):
        if 'name' in request.session:
            if request.session['name'].get('userType') == 'student':
                dataSelf = editSubjectToPredictGrade[0]
                gradeStr = ''
                if dataSelf.get('grade') == 4:
                    gradeStr = 'A'
                if dataSelf.get('grade') == 3.5:
                    gradeStr = 'B+'
                if dataSelf.get('grade') == 3:
                    gradeStr = 'B'
                if dataSelf.get('grade') == 2.5:
                    gradeStr = 'C+'
                if dataSelf.get('grade') == 2:
                    gradeStr = 'C'
                if dataSelf.get('grade') == 1.5:
                    gradeStr = 'D+'
                if dataSelf.get('grade') == 1:
                    gradeStr = 'D'
                if dataSelf.get('grade') == 0:
                    gradeStr = 'F'
                data = {
                    'subjectNumber': dataSelf.get('subjectNumber'),
                    'subjectName': dataSelf.get('subjectName'),
                    'credit': dataSelf.get('credit'),
                    'grade': gradeStr,
                }

                if request.POST.get('subGrade') is not None:
                    gradeStd = GradeUserStudent.objects.get(id=dataSelf.get('gradeId'))
                    gradeStd.grade = request.POST.get('subGrade')
                    gradeStd.save()
                    return HttpResponseRedirect('/historyGrade')
                return render(request, 'editToPredictGrade.html', data)
            else:
                return HttpResponseRedirect('/Home/')
        else:
            return HttpResponseRedirect('/loginn')