from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 新增 UserProfile 模型來擴展 Django 內建的 User 模型
class UserProfile(models.Model):
    """
    UserProfile model to extend Django's built-in User model.
    It holds additional user-specific information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 添加以下欄位，以匹配註冊時可能傳遞的參數
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="出生日期")
    height = models.FloatField(null=True, blank=True, verbose_name="身高 (公分)")
    weight = models.FloatField(null=True, blank=True, verbose_name="體重 (公斤)")
    fitness_level = models.CharField(max_length=50, blank=True, verbose_name="健身程度") # 例如：初級, 中級, 高級

    default_weight_goal = models.FloatField(null=True, blank=True, verbose_name="預設體重目標 (公斤)")

    def __str__(self):
        return self.user.username

class FitnessActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField("活動類型", max_length=50)
    duration = models.DurationField()
    intensity = models.CharField(max_length=50)
    calories_burned = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.activity_type} on {self.date_time.strftime('%Y-%m-%d')}"

class DietaryLog(models.Model):
    """
    Dietary Log
        Fields: user (ForeignKey to User), food item, calories, nutrients (carbs, proteins, fats), quantity, date/time of meal.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    food_item = models.CharField(max_length=50)
    calories = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    fats = models.IntegerField()
    quantity = models.IntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.food_item} for {self.user.username} on {self.date_time.strftime('%Y-%m-%d')}"


class FitnessGoal(models.Model):
    """
    Fitness Goal
        Fields: user (ForeignKey to User), goal type (e.g., weight loss, hydration), target value, start date, end date, current progress.
    """
    GOAL_CHOICES = [
        ('WGT', 'Weight Loss'),
        ('HYD', 'Hydration'),
        ('MUS', 'Muscle Gain'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=3, choices=GOAL_CHOICES)
    target_value = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    current_progress = models.IntegerField()

    def __str__(self):
        return f"{self.goal_type} goal for {self.user.username}"

class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.date.strftime("%Y-%m-%d")}'
