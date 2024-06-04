from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password as django_check_password

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            username=username,
            email=email,
            password=password,
        )
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255) # 關掉unique=True
    password = models.CharField(max_length=128)
    last_login = models.TimeField(auto_now=True)
    REQUIRED_FIELDS = ['email']  
    USERNAME_FIELD = 'username'


    objects = CustomUserManager()

    def __str__(self):
        return self.username
    def check_password(self, raw_password):
        return raw_password == self.password
    @property
    def is_authenticated(self):
        """
        自定义的认证属性，用于检查用户是否认证成功。
        在这个示例中，我们简单地检查用户的最后登录时间是否为空来判断用户是否认证成功。
        你可以根据实际需求和项目逻辑来扩展这个属性。
        """
        return self.last_login is not None and self.last_login != ''

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
        # exclude = ['last_login'] 

class UserAuthForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            print(f'User found: {user.username}')  # 除錯輸出
            if user.check_password(password):
                print('Password is correct')  # 除錯輸出
                return user
            else:
                print('Password is incorrect')  # 除錯輸出
                return None
        except CustomUser.DoesNotExist:
            print('User not found')  # 除錯輸出
            return None
        

class TodoItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)  # 添加这个字段


    class Meta:
        ordering = ['-is_pinned', '-created_at']

class DiaryEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()
    image = models.ImageField(upload_to='diary_images/', blank=True, null=True)


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['content', 'is_pinned', 'is_completed']  
        labels = {
            'content': '内容',
            'is_pinned': '置頂',
            'is_completed': '完成',
        }

class DiaryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        # fields = ['date', 'content', 'image']
        fields = ['date', 'content']
        labels = {
            'date': '日期',
            'content': '內容',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }