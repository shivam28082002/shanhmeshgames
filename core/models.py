from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



TASK_TYPES = [
        ('watch_ad', 'Watch Ad'),
        ('read_hafez', 'Read Hafez'),
        ('join_tg', 'Join Telegram'),
        ('follow_social', 'Follow Social Media')
    ]


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.telegram_id})"
    


# 1. Level System
class Level(models.Model):
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Level {self.number}: {self.name}"


class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    experience = models.PositiveIntegerField(default=0)


# 2. Token & Mining
class TokenWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_tokens = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    last_mined = models.DateTimeField(null=True, blank=True)


class MiningCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MiningCard(models.Model):
    category = models.ForeignKey(MiningCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.FloatField()
    is_active = models.BooleanField(default=True)


class UserMiningCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(MiningCard, on_delete=models.CASCADE)
    obtained_at = models.DateTimeField(auto_now_add=True)


# 3. Daily Tasks
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TASK_TYPES)
    reward = models.PositiveIntegerField()
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)


# 4. Mini-Games
class MiniGame(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward = models.PositiveIntegerField()


class UserMiniGameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)


# 5. Airdrops
class Airdrop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)


class UserAirdropEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    airdrop = models.ForeignKey(Airdrop, on_delete=models.CASCADE)
    claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(blank=True, null=True)


    
    
class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Skin(models.Model):
    character = models.ForeignKey(Character, related_name='skins', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_unlocked = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    image_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return f'{self.name} for {self.character.name}'


class Purchase(models.Model):
    # user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, related_name='purchases', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.skin.is_unlocked:
            self.skin.is_unlocked = True
            self.skin.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} purchased {self.skin.name}'
    

class UserCharater(models.Model):
    CHARACTER_CHOICES = [
        ('fourse_aladin', 'Fourse Aladin'),
        ('king_q', 'King Q'),
        ('nashmieh', 'Nashmieh'),
        ('arshine', 'Arshine'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.CharField(max_length=20, choices=CHARACTER_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_character_display()}"


class UserCharater(models.Model):
    CHARACTER_CHOICES = [
        ('fourse_aladin', 'Fourse Aladin'),
        ('king_q', 'King Q'),
        ('nashmieh', 'Nashmieh'),
        ('arshine', 'Arshine'),
    ]

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.CharField(max_length=20, choices=CHARACTER_CHOICES)
    level = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(11)
        ],
        default=1
    )
    engry = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000)
        ],
        default=1
    )
    def __str__(self):
        return f"{self.user.username} - {self.get_character_display()} (Level {self.level})"