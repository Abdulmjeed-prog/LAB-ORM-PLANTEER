from django import forms
from plants.models import Plant
from plants.models import Comment


class PlantForm(forms.ModelForm):
    # Force yes/no values but coerce to boolean
    is_edible = forms.TypedChoiceField(
        choices=(('yes', 'Yes'), ('no', 'No')),
        coerce=lambda x: x == 'yes',
        error_messages={
            'invalid_choice': 'Please choose Yes or No.',
            'required': 'Is edible is required.',
        }
    )

    name = forms.CharField(
        min_length=3,
        max_length=50,
        error_messages={
            'required': 'Plant name is required.',
            'min_length': 'Plant name must be at least 3 characters.',
            'max_length': 'Plant name must not be more than 50 characters.',
        }
    )

    about = forms.CharField(
        min_length=10,
        max_length=1024,
        widget=forms.Textarea,
        error_messages={
            'required': 'Plant description is required.',
            'min_length': 'Plant description must be at least 10 characters.',
            'max_length': 'Plant description must not be more than 1024 characters.',
        }
    )

    used_for = forms.CharField(
        min_length=5,
        max_length=255,
        error_messages={
            'required': 'Please enter what the plant is used for.',
            'min_length': 'Used for must be at least 5 characters.',
            'max_length': 'Used for must not be more than 255 characters.',
        }
    )

    image = forms.ImageField(
        error_messages={
            'required': 'Please upload an image for the plant.',
        }
    )

    category = forms.ChoiceField(
        # Use the same choices as in your template
        choices=Plant.CategoryChoices.choices,
        error_messages={
            'required': 'Please select a category.',
        }
    )

    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible','countries']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','content']
