from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class ReviewForm(forms.Form):
    '''форма отзыва'''
    CHOICES = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5'), ]
    name = forms.CharField(label='Имя', required=True,
                           max_length=150,
                           widget=forms.TextInput(attrs={'placeholder': 'Представьтесь', 'class': 'form-control'})
                           )
    text = forms.CharField(label='Содержание',
                           required=True,
                           widget=forms.Textarea({'placeholder': 'Содержание', 'class': 'form-control'})
                           )
    stars = forms.ChoiceField(label='Оценка',
                              required=False,
                              widget=forms.RadioSelect,
                              choices=CHOICES, )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',
                  'password1', 'password2']
