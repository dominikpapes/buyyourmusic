from django import forms
from .models import Album, Review, Author

from django import forms
from .models import Album, Author

from django.core.exceptions import ValidationError
from PIL import Image

class AlbumForm(forms.ModelForm):
    new_author = forms.CharField(
        required=False,
        label="New Author (if not listed)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Fill this only if the author isn't in the list."
    )

    class Meta:
        model = Album
        fields = ['title', 'author', 'new_author', 'year', 'price', 'quantity', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1800, 'max': 2100, 'step': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].required = False

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")
        new_author = cleaned_data.get("new_author")

        if not author and not new_author:
            raise forms.ValidationError("Please select an author or enter a new one.")
        return cleaned_data

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if cover:
            img = Image.open(cover)
            if img.format not in ['JPEG', 'JPG']:
                raise ValidationError("Only JPEG images are allowed.")
            if img.width > 1000 or img.height > 1000:
                raise ValidationError("Image must be no larger than 1000x1000 pixels.")
        return cover

    def save(self, commit=True):
        new_author_name = self.cleaned_data.get("new_author")
        if new_author_name:
            author = Author.objects.filter(name__iexact=new_author_name.strip()).first()
            if not author:
                author = Author.objects.create(name=new_author_name.strip())
            self.instance.author = author
        else:
            self.instance.author = self.cleaned_data.get("author")

        return super().save(commit=commit)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

