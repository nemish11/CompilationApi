from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
import pandas as pd
from compilerApi.settings import *
from django.core.files.storage import FileSystemStorage
import subprocess
# Create your views here.

def program_file(request):
    #print(BASE_DIR)
    return render(request,'index.html')

def submit_code(request):
    fs = FileSystemStorage()
    filename = BASE_DIR + "\\compilerApiApp\\static\\code.cpp"
    handle1=open(filename,'r+')
    handle1.write(request.POST.get('code',''))
    handle1.close()
    subprocess.call(["cd", BASE_DIR+"\\compilerApiApp\\static"],shell=True)
    tmp = subprocess.call(["g++",filename])
    #tmp=subprocess.call(BASE_DIR + "\\compilerApiApp\\static\\a.exe")
    #tmp=subprocess.call(BASE_DIR + "\\compilerApiApp\\static\\code.exe")
    tmp=subprocess.call(BASE_DIR + "./a.exe")
    subprocess.call(["type",BASE_DIR+"\\inp.txt"],shell=True)
    print()
    print ("printing result")
    print (tmp)
    return render(request,'index.html')