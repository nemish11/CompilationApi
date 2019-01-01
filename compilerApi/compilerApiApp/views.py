from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
import pandas as pd
from datetime import datetime
from django.utils import timezone
from .models import Submissions,Files
from compilerApi.settings import *
from django.core.files.storage import FileSystemStorage
import subprocess
import os
import shutil

# Create your views here.

def program_file(request):
    return render(request,'index.html')

def submit_code(request):
    username = request.POST.get('username','')
    inputfile = request.FILES["inputfile"]
    language = request.POST.get('language','')
    code = request.POST.get('code','')
    c = {}
    submission = Submissions(username=username,language=language,datetime=datetime.now())
    submission.save()

    submission = Submissions.objects.filter(username=username).last()
    id = submission.id

    fs = FileSystemStorage()
    filename = BASE_DIR + "/compilerApiApp/static/"
    dirname = filename + str(id)

    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)

    codefile = dirname + "/codefile.cpp"
    codefile_handler=open(codefile,'w+')
    codefile_handler.write(code)
    codefile_handler.close()

    inp = fs.save(dirname+"/input.txt",inputfile)
    outputfile_handler = open(dirname+"/output.txt",'w+')
    codefile_handler.close()
    errorfile_handler = open(dirname+"/error.txt",'w+')
    errorfile_handler.close()
    tmp = subprocess.call([filename+"./run.sh", codefile, dirname+"/codefile.out", dirname+"/./codefile.out", dirname+"/input.txt",dirname+"/output.txt", dirname+"/error.txt"])

    if os.stat(dirname+"/error.txt").st_size != 0:
        f = open(dirname+"/error.txt",'r')
        c['message'] = f.read(400)
        return render(request,'index.html',c)

    code_f = Files(type='codefile',submission=submission,filepath=codefile)
    code_f.save()

    input_f = Files(type='inputfile',submission=submission,filepath=dirname+"/input.txt")
    input_f.save()

    output_f = Files(type='outputfile',submission=submission,filepath=dirname+"/output.txt")
    output_f.save()

    f = open(dirname+"/output.txt",'r')
    c['message'] = f.read()
    print("sucessfully compiled")
    return render(request,'index.html',c)
