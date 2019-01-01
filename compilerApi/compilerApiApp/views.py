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
    submission = Submissions(username=username,language=language,datetime=datetime.now(),isRunning='YES',errortype='-')
    submission.save()

    submission = Submissions.objects.filter(username=username).last()
    id = submission.id
    submission = Submissions.objects.get(pk=int(id))
    #print(submission)
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

    submission.isRunning = 'NO'
    submission.save()
    print(submission.isRunning + "hjjkhjjkj")

    if os.stat(dirname+"/error.txt").st_size != 0:
        f = open(dirname+"/error.txt",'r')
        submission.errortype = "compile error"
        submission.save()
        c['message'] = "compiler error " + f.read(400)
        return render(request,'index.html',c)

    code_f = Files(type='codefile',submission=submission,filepath=codefile)
    code_f.save()

    input_f = Files(type='inputfile',submission=submission,filepath=dirname+"/input.txt")
    input_f.save()

    output_f = Files(type='outputfile',submission=submission,filepath=dirname+"/output.txt")
    output_f.save()

    f = open(dirname+"/output.txt",'r')
    data = f.read()
    f.close()

    index = int(data.find("Command terminated by signal"))
    termination_code = -1
    if index != -1:
        termination_code = data[index+28:index+30]
        c['code'] = termination_code
        submission.errortype = "RunTime error"
        submission.save()
        c['message'] ="runtime error" + data[index:index+31]
    else:
        c['message'] = "sucessfully run"

    index = int(data.find("Command"))
    f = open(dirname+"/output.txt","w")
    f.write(data[0:index])
    f.close()

    time_taken = int(data.find("User time (seconds)"))
    time_taken1 = data[time_taken+20:time_taken+24] + "sec"
    c['time_taken'] =  time_taken1

    memory_used = int(data.find("Maximum resident set size (kbytes)"))
    memory_used1 = data[memory_used+36:memory_used+41] +"kb"
    c['memory_used'] = memory_used1

    submission.runtime = time_taken1
    submission.memoryused = memory_used1

    submission.save()
    #print("sucessfully compiled")
    return render(request,'index.html',c)
