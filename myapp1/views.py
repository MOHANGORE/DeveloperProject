from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import Blog
from . forms import Edit_Blog
# Create your views here.
def index(request):
    blog = Blog.objects.all()
    context={'blogs':blog}
    return render(request, 'home.html', context)

def user_register(request):
    if request.method=='POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        
        return redirect('index')
    return render(request, 'login.html')

def post_blog(request):
    if request.method=='POST':
        title = request.POST.get('title')
        desc = request.POST.get('Description')
        blog = Blog(title=title,dsc=desc,user_id=request.user)
        blog.save()
        return redirect('index')
    return render(request, 'blog_post.html')

def blog_detail(request,id):
    blog = Blog.objects.get(id=id)
    context = {'blog':blog}
    return render(request,'blog_detail.html',context)

def delete(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('/')

def edit(request,id):
    blog = Blog.objects.get(id=id)
    editblog = Edit_Blog(instance=blog)
    if request.method=='POST':
        form = Edit_Blog(request.POST,instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'edit_blog.html',{'edit_blog':editblog})
    