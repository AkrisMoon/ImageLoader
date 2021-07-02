from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ImageLoader.models import Image


class ImageCreateForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'url']

    def clean(self):
        super().clean()
        image = self.cleaned_data.get('image')
        url = self.cleaned_data.get('url')

        if (image and url) or (image is None and url == ''):
            errors = {'image': ValidationError('Too many or few input parameters', 'too many or few input parameters')}
            raise ValidationError(errors)

class ImageResizeForm(ModelForm):
    class Meta:
        model = Image
        fields = ['width', 'height', 'image', 'url']

    def clean(self):
        super().clean()
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if width==height==None:
            errors = {'width': ValidationError('No resizing options specified', 'no resizing options specified')}
            raise ValidationError(errors)

