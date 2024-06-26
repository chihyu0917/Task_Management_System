from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from tasks.userinfo import UserCreateForm, UserAuthForm, TodoForm, DiaryForm, TodoItem, DiaryEntry
from tasks.email import SendEmail

from django.contrib.auth.decorators import login_required

@login_required
def todo_list(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    items = TodoItem.objects.filter(user=request.user)
    return render(request, 'todo_list.html', {'items': items, 'form': form})

def update_task(request, task_id):
    task = TodoItem.objects.get(id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('/tasks/todo/')  # 根据实际情况调整重定向 URL


@login_required
def diary_list(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()
            return redirect('diary_list')
    else:
        form = DiaryForm()
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'diary_list.html', {'entries': entries, 'form': form})

def delete_entry(request, entry_id):
    if request.method == 'POST':
        entry = DiaryEntry.objects.get(id=entry_id)
        entry.delete()
        return redirect('diary_list')  # 确保 'diary_list' 是显示日记列表的视图的 URL 名称
    else:
        return redirect('diary_list')  # GET 请求也重定向，避免直接访问删除 URL

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_email = request.POST.get('email')  #收件者
            
            email = SendEmail()
            email.send_register_mail(user,user_email)
             

            login(request, user)
            return redirect('login')  # 修改為註冊成功後要跳轉的頁面，比如首頁
    else:
        form = UserCreateForm()
    # return HttpResponse("Event創建失敗。")
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)

                email = SendEmail()
                email.getemail(user)
                
                # show_username(request)
                # print(request.user.is_authenticated)
                request.session['username'] = user.username  # Store username in session
                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('/tasks')  # Redirect to tasks page
                # return show_username(request) # 登錄成功後跳轉到指定頁面
            else:
                # 驗證失敗，顯示錯誤訊息或者重新渲染登錄頁面
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = UserAuthForm()
        return render(request, 'login.html', {'form': form })

def user_logout(request):
    logout(request)
    print(request.user.is_authenticated)
    return redirect('/login')  # 修改為登出後要跳轉的頁面，比如首頁

# def show_username(request):
    print("show_username 被调用了")
    # 检查用户是否已经登录
    if request.user.is_authenticated:
        # 获取当前登录用户的用户名
        usernames = request.user.username
        print(f'Username in 登录: {usernames}')
        # 渲染包含用户名的页面
        return render(request, 'create_event.html', {'user': request.user})
    else:
        # 用户未登录，可以根据需要进行处理，比如跳转到登录页面
        usernames = request.user.username
        print(f'Username in 未登录: {usernames}')
        return render(request, 'login.html')  # 假设登录页面的模板名为'login.html'
    
# def task_view(request):
    print(f'Username in 登录task_view: {usernames}')
    username = request.session.get('username')  # Get username from session
    if username:
        return render(request, 'create_event.html', {'username': username})
    else:
        return HttpResponse('Please log in to access this page.')
