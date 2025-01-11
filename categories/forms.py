from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "custom-name-id",
                "placeholder": "Enter category name",
                "data-category": "name-field",
            }
        )

        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control custom-description-class",
                "id": "custom-description-id",
            }
        )
        # Customizing labels
        self.fields["name"].label = "Category Name"
        self.fields["description"].label = "Category Description"
