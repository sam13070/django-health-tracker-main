from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, FitnessActivity, DietaryLog, WeightEntry
from django.utils import timezone

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="電子郵件")
    date_of_birth = forms.DateField(
        label="出生日期",
        help_text='必填，格式：YYYY-MM-DD',
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    height = forms.IntegerField(label="身高", help_text='單位：公分')
    weight = forms.IntegerField(label="體重", help_text='單位：公斤')
    fitness_level = forms.IntegerField(label="體適能等級", help_text='範圍：1 到 10')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'date_of_birth', 'height', 'weight', 'fitness_level']
        labels = {
            'username': '使用者名稱',
            'password1': '密碼',
            'password2': '確認密碼',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight'],
                fitness_level=self.cleaned_data['fitness_level']
            )
        return user


class ActivityForm(forms.ModelForm):
    class Meta:
        model = FitnessActivity
        fields = ['activity_type', 'duration', 'intensity', 'calories_burned', 'date_time']
        labels = {
            'activity_type': '活動類型',
            'duration': '持續時間（分鐘）',
            'intensity': '強度',
            'calories_burned': '消耗卡路里',
            'date_time': '日期',
        }
        widgets = {
            'date_time': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class DietaryLogForm(forms.ModelForm):
    class Meta:
        model = DietaryLog
        fields = ['food_item', 'calories', 'carbs', 'proteins', 'fats', 'quantity', 'date_time']
        labels = {
            'food_item': '食物項目',
            'calories': '卡路里',
            'carbs': '碳水化合物（克）',
            'proteins': '蛋白質（克）',
            'fats': '脂肪（克）',
            'quantity': '份量',
            'date_time': '日期',
        }
        widgets = {
            'date_time': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']
        labels = {
            'weight': '體重（公斤）',
            'date': '日期',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date().isoformat()}),
        }
