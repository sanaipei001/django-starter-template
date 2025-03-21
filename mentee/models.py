# mentee/models.py
from django.db import models
from users.models import User

class Survey(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    background_info = models.TextField()
    career_interests = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey by {self.mentee.email}"

class Progress(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    category = models.CharField(max_length=50, choices=[
        ('self_discovery', 'Self-Discovery'),
        ('career', 'Career'),
        ('mindset', 'Mindset'),
        ('behavioral_change', 'Behavioral Change'),
    ])
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mentee.email} - {self.category}"

class Reflection(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reflections')
    what_learned = models.TextField()
    challenges = models.TextField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflection by {self.mentee.email} on {self.created_at}"

class Recommendation(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('resource', 'Resource'),
        ('internship', 'Internship'),
        ('education', 'Education'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.mentee.email}"