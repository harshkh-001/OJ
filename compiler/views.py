from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ojapp.models import Problems
from .models import Compilers
import subprocess
import os
import uuid
import sys

@login_required
def executes(request):
    if(request.method == 'POST'):
        print(request.POST)
        url = request.path
        print(url)
        action = request.POST.get('action')
        if(action == "Submit"):
            problem = Problems.objects.get(id = request.POST.get('problem_id'))
            user = request.user
            lang = request.POST.get('lang','')
            uid = uuid.uuid4()
            
            code = request.POST.get('code','')
            code_file = rf"D:\fun\django alg\oj\oj\compilation_data\codes\{uid}.{lang}"
            executable = rf"D:\fun\django alg\oj\oj\compilation_data\codes\{uid}.exe"
            with open(code_file, 'w') as f:
                f.write(code)
            p_folder = rf"D:\fun\django alg\oj\oj\compilation_data\testcases\problem_{problem.id}"
            if(lang == "cpp"):
                compile = subprocess.run(["g++",code_file,"-o",executable], capture_output=True, text=True, timeout=50)
                if(compile.returncode != 0):
                    err_msg = compile.stderr
                    Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message=err_msg, status=False)
                    return HttpResponse(err_msg)      # throw error for wrong code with code err message
                
                for file in os.listdir(p_folder):
                    if(file.startswith("input_")):
                        num = file.split('_')[1].split('.')[0]
                        input_file_path = os.path.join(p_folder,file)
                        with open(input_file_path, 'r') as fi:
                            file_input = fi.read()
                        run = subprocess.run([executable],input=file_input, capture_output=True, text=True,timeout=15)
                        with open(rf"{p_folder}\output_{num}.txt") as fo:
                            file_output = fo.read()
                        if(file_output.strip() != run.stdout.strip()):
                            message = f"err occur in Test Case {num} \n your output : {run.stdout} \n Expected Output : {file_output.strip()} \n err : {run.stderr}"
                            Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message=message, status=False)
                            return HttpResponse(message)
                Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message="Submitted Successfully", status=True)
                return HttpResponse("successfully submitted")
            
            if(lang == "py"):
                
                for file in os.listdir(p_folder):
                    if(file.startswith("input_")):
                        num = file.split('_')[1].split('.')[0]
                        input_file_path = os.path.join(p_folder,file)
                        with open(input_file_path, 'r') as fi:
                            file_input = fi.read()
                            fiarr = file_input.split()
                            inp_str = '\n'.join(fiarr) + '\n'
                        # run = subprocess.run([executable],input=file_input, capture_output=True, text=True,timeout=15)
                        run = subprocess.run([sys.executable,code_file],input=inp_str, capture_output=True, text=True, timeout=5)
                        if(run.returncode != 0):
                            err_msg = run.stderr
                            Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message=err_msg, status=False)
                            return HttpResponse(err_msg)  
                        with open(rf"{p_folder}\output_{num}.txt") as fo:
                            file_output = fo.read()
                        if(file_output.strip() != run.stdout.strip()):
                            message = f"err occur in Test Case {num} \n your output : {run.stdout} \n Expected Output : {file_output.strip()} \n err : {run.stderr}"
                            Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message=message, status=False)
                            return HttpResponse(message)
                Compilers.objects.create(problem=problem, user=user, lang=lang, uuid=uid, message="Submitted Successfully", status=True)
                return HttpResponse("successfully submitted")
            
            return HttpResponse("unknown error occur try again later")
        
        if(action == "Run"):
            input= request.POST.get('input','')
            lang = request.POST.get('lang','')
            inputlst = input.split()
            input_str = '\n'.join(inputlst) + '\n'
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
                compile = subprocess.run(["g++",filename,"-o",executable], capture_output=True, text=True, timeout=15)
                
                if(compile.returncode != 0):
                    return render(request, "ojapp/pb_base.html", {'output' : compile.stderr , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
                
                run = subprocess.run([executable],input=input, capture_output=True, text=True,timeout=15)
                # return HttpResponse("Output : \n" + run.stdout)
                return render(request, "ojapp/pb_base.html", {'output' : run.stdout , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
            
            if(lang == "py"):
                if(code == ''):
                    return render(request, "ojapp/pb_base.html", {'output' : "code cannot be empty" , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
                if(input == ''):
                    return render(request, "ojapp/pb_base.html", {'output' : "input cannot be empty" , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
                compile = subprocess.run([sys.executable,filename],input=input_str, capture_output=True, text=True, timeout=5)
                if(compile.returncode != 0):
                    return render(request, "ojapp/pb_base.html", {'output' : compile.stderr , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
                
                return render(request, "ojapp/pb_base.html", {'output' : compile.stdout , 'p_id' : p_id, 'input' : input , 'code':code , 'lang':lang , 'data':data})
        return HttpResponse("submit under construction")
        
    else:
        return HttpResponse("page is not accessable")


@login_required
def run(request):
    pass