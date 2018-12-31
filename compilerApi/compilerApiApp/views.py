from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
import pandas as pd
from compilerApi.settings import *
from django.core.files.storage import FileSystemStorage
import subprocess
import os
# Create your views here.

def program_file(request):
    return render(request,'index.html')

def submit_code(request):
    fs = FileSystemStorage()
    filename = BASE_DIR + "/compilerApiApp/static/code.cpp"
    filename1 = BASE_DIR + "/compilerApiApp/static/"
    handle1=open(filename,'w+')
    handle1.write(request.POST.get('code',''))
    handle1.close()
    #subprocess.call(["cd", BASE_DIR+"/compilerApiApp/static"],shell=True)
    tmp = subprocess.call([BASE_DIR+"/compilerApiApp/static/./run.sh",filename,filename1+"abc.out",filename1+"./abc.out",filename1+"input.txt",filename1+"output.txt"])

    #tmp = subprocess.call(["g++",filename,"-o",BASE_DIR+"/compilerApiApp/static/abcd.out"])
    #tmp = subprocess.call(BASE_DIR+"/compilerApiApp/static/abcd.out")
    print()
    print ("printing result")
    print (tmp)
    return render(request,'index.html')
