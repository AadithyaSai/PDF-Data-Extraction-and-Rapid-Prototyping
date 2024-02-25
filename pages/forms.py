from django.forms import ModelForm, FileInput
from .models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["file"]
        widgets = {"file": FileInput(attrs={"accept": "image/*,.pdf"})}
