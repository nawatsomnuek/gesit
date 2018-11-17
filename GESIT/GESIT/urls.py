"""GESIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from AnalyzeGrade import views
# from AnalyzeGrade.views import ChartData

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^index/$', views.index, name='api-data'),
    url(r'^data/$', views.page.get_data, name='api-data'),
    # url(r'^$', views.index, name='index'),
    # path('chart/', views.listSubjects),
    path('', views.page.firstPage),
    # url(r'^Home$', views.homePage, name='homePage'),
    path('Home/', views.page.homePage),
    # re_path(r'^Home', views.homePage),gra
    # path('gra', views.page.gra),
    path('login', views.page.loginPage),
    path('register', views.page.register),
    path('regisSuccess', views.page.regisSuccess),
    path('loginn', views.page.login),
    path('lecturer', views.page.Home_lecturerPage),
    # path('Home/login/TallSoneY55', views.TallSoneY55Page),
    # path('Home/login/selectSubject', views.selectSubject),
    path('selectYearKmean', views.page.selectYearKmean),
    path('selectYearKmean/selectSubject', views.page.selectSubject),
    path('selectYearKmean/selectSubject/showGraphKmean', views.page.showGeaphOfCluster),
    # path('selectSubject/GraphallSoneY', views.page.showGeaphOfCluster),
    path('selectYearPreason', views.page.selectYearPreason),
    path('selectYearPreason/selectSubjectPreason', views.page.selectSubjectPreason),
    path('selectYearPreason/selectSubjectPreason/showGraphPearson', views.page.showGraphPearson),
    path('showAllPearsonValues', views.page.showAllPearson),
    # path('ggg', views.page.ggg),
    path('logout', views.page.logout),


    path('profile', views.page.profileStu),
    path('student', views.page.Home_studentPage),
    path('historyGrade', views.page.historyGrade),
    path('historyGrade/insertSubject', views.page.insertSubject),
    path('historysGradeToPredict', views.page.historysGradeToPredict),
    path('historysGradeToPredict/insertSubjectToPredict', views.page.insertSubjectToPredict),
    path('historysGradeToPredict/chooseSubjectAsPredict', views.page.chooseSubjectAsPredict),
    path('historysGradeToPredict/chooseSubjectAsPredict/predictGrade', views.page.predictGrate),
    path('delectSubject', views.page.delect),
    path('editSubject', views.page.editToPredictGrade),
    path('delectSubjectTrans', views.page.delectTrans),
    path('historyGrade/editTransGrade', views.page.editTransGrade),
    path('historysGradeToPredict/chooseSubjectAsPredict/predictGrade/showDetailPredict', views.page.showDetailPredict),


    # path('testPredict', views.page.editToPredictGrade),
    # url(r'^chart/data/$', ChartData.as_view())
]
