from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ojapp.models import Problems
import subprocess
import os
import uuid

@login_required
def executes(request):
    if(request.method == 'POST'):
        print(request.POST)
        url = request.path
        print(url)
        action = request.POST.get('action')
        if(action == "Submit"):
            pass
        if(action == "Run"):
            input= request.POST.get('input','')
            lang = request.POST.get('lang','')
            # inputlst = list(map(int, input.split()))
            code = request.POST.get('code', '')
            user_name = request.user.username
            input_path = rf"D:\fun\django alg\oj\oj\compilation_data\input\{user_name}.txt"
            output_path = rf"D:\fun\django alg\oj\oj\compilation_data\output\{user_name}.txt"
            filename = rf"D:\fun\django alg\oj\oj\compilation_data\codes\{user_name}.{lang}"
            executable = rf"D:\fun\django alg\oj\oj\compilation_data\codes\{user_name}.exe"
            p_id = request.POST.get('problem_id')
            data = Problems.objects.get(id = p_id)
            with open(filename, 'w') as f:
                f.write(code)
            
            with open(input_path, 'w') as f:
                f.write(input)
                
            with open(output_path, 'w') as f:
                pass
            if(lang == "cpp"):         
                compile = subprocess.run(["g++",filename,"-o",executable], capture_output=True, text=True)
                
                if(compile.returncode != 0):
                    return render(request, "ojapp/pb_base.html", {'output' : compile.stderr , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
                
                run = subprocess.run([executable],input=input, capture_output=True, text=True)
                # return HttpResponse("Output : \n" + run.stdout)
                return render(request, "ojapp/pb_base.html", {'output' : run.stdout , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
        return HttpResponse("submit under construction")
        
    else:
        return HttpResponse("page is not accessable")


@login_required
def run(request):
    pass