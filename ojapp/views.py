from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Problems
from compiler.models import Compilers
from django.utils.text import slugify
# @login_required
def index(request):
    return HttpResponse(f"hello , welcome to oj")

@login_required
def dashboard(request):
    # if(request.method == 'POST'):
    #     submited_code = request.POST.get('code')
    #     return render(request, "ojapp/dashboard.html", {'code': submited_code})
    return render(request, "ojapp/dashboard.html")
    

@login_required
def problem_list(request):
    data = Problems.objects.all()
    return render(request, "ojapp/problem.html", {"data" : data}) 

@login_required
def problems(request, p_name):
    pblist = Problems.objects.all()
    for data in pblist:
        if(slugify(data.name) == p_name):
            return render(request, "ojapp/pb_base.html", {"data": data , "slug_name":p_name})

    return HttpResponse("No Quesion with this name Exist")
    
    
@login_required
def problem_submissions(request, p_name):
    name = p_name.replace('-'," ")
    print(name)
    data = []
    temp = list(Compilers.objects.filter(user = request.user).values())
    for x in temp:
        x["problem_id"] = Problems.objects.get(id= x["problem_id"]).name
        if(x["problem_id"].lower() == name):
            data.append(x)
    # problem = Problems.objects.get(name=name)
    # data = Compilers.objects.filter(user = request.user , problem=problem).values()
    return render(request, "ojapp/submissions.html" , {"data":data})
    # return HttpResponse(data)
    
    
@login_required
def submissions(request):
    
    data = list(Compilers.objects.filter(user =  request.user).values())
    data.reverse()
    for x in data:
        x["problem_id"] = Problems.objects.get(id= x["problem_id"]).name
    # return HttpResponse(data)
    return render(request, "ojapp/submissions.html" , {"data":data})
    
# @login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

