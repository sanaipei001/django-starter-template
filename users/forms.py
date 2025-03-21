# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, MenteeProfile, CaseManagerProfile

class UserRegisterForm(UserCreationForm):
    type = forms.ChoiceField(
        choices=User.Types.choices,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2'
        })
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "type", "password1", "password2", "gender", "profile_picture", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

class UserChangeForm(UserChangeForm):
    type = forms.ChoiceField(
        choices=User.Types.choices,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2'
        })
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "type", "profile_picture", "phone_number", "gender")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['email'].disabled = True  # Make email read-only in profile updates

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'phone_number', 'first_name', 'last_name']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number (e.g., +254123456789)'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'mt-1 block w-full'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.startswith('+'):
            raise forms.ValidationError('Phone number must start with a country code (e.g., +254).')
        if phone_number and len(phone_number) < 10:
            raise forms.ValidationError('Phone number must be at least 10 characters long.')
        return phone_number
            
class MenteeProfileForm(forms.ModelForm):
    class Meta:
        model = MenteeProfile
        fields = ['career_interests']
        widgets = {
            'career_interests': forms.TextInput(attrs={'placeholder': 'Enter your career interests (e.g., Software Development, Graphic Design)'}),
        }

    def clean_career_interests(self):
        career_interests = self.cleaned_data.get('career_interests')
        if career_interests and len(career_interests) > 100:
            raise forms.ValidationError('Career interests cannot exceed 100 characters.')
        return career_interests

class CaseManagerProfileForm(forms.ModelForm):
    class Meta:
        model = CaseManagerProfile
        fields = ['expertise']
        widgets = {
            'expertise': forms.TextInput(attrs={'placeholder': 'Enter your expertise (e.g., Career Counseling, Tech Training)'}),
        }

    def clean_expertise(self):
        expertise = self.cleaned_data.get('expertise')
        if expertise and len(expertise) > 100:
            raise forms.ValidationError('Expertise cannot exceed 100 characters.')
        return expertise