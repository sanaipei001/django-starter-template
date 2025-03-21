# mentee/forms.py
from django import forms
from .models import Survey, Progress, Reflection, Recommendation

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['background_info', 'career_interests']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['category', 'description', 'status']

class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['what_learned', 'challenges', 'feedback']

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['title', 'description', 'link', 'category']