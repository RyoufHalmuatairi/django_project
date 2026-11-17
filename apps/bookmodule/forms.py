from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    price = forms.FloatField(min_value=0)
    edition = forms.IntegerField(min_value=1, max_value=32767)

    class Meta:
        model = Book
        fields = ('title', 'author', 'price', 'edition')
