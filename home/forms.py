from dataclasses import fields
from pydoc import describe
from django import forms
from home.models import Blog
from ckeditor.fields import RichTextField

class Textform(forms.Form):
    text = forms.CharField( widget=forms.Textarea , required=True)

class AddBlog(forms.ModelForm):
    description = RichTextField()
    class Meta:
        model = Blog
        fields = ("title",'category', 'description',"Banner")