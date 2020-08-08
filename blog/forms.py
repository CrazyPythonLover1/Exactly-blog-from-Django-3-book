from django import forms 
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

# class CommentForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#     body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control'})
        }

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))