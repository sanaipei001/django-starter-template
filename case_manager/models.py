# case_manager/models.py
from django.db import models
from users.models import User

class Session(models.Model):
    case_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_sessions')
    date = models.DateField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session with {self.mentee.email} on {self.date}"

class Report(models.Model):
    case_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_reports')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.mentee.email} by {self.case_manager.email}"