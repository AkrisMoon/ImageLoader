from django.shortcuts import redirect, render, get_object_or_404
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from ImageLoader.models import Image
from ImageLoader.forms import ImageCreateForm, ImageResizeForm
from PIL import Image as img
import requests
from django.conf import settings


class CreateImageView(CreateView):
    model = Image
    form_class = ImageCreateForm
    template_name = 'add_image.html'

    def post(self, request, *args, **kwargs):
        form = ImageCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if form.image:
                im = img.open(form.image)
            elif form.url != '':
                im = img.open(requests.get(form.url, stream=True).raw)
            (width, height) = im.size
            image = Image.objects.create(image=form.image, url=form.url, width=width, height=height)
            return redirect('resize_image', pk=image.id)
        else:
            print(form.errors)
            return render(request, 'add_image.html', {'form': form})

class ImageListView(ListView):
    model = Image
    template_name = 'image_list.html'

    def get_queryset(self):
        queryset = Image.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ImageResizeView(UpdateView):
    model = Image
    form_class = ImageResizeForm
    template_name = 'resize_image.html'

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, id=int(self.kwargs.get('pk')))
        form = ImageResizeForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            parent_image = Image.objects.get(id=int(self.kwargs.get('pk')))
            new_image = Image.objects.create(width=form.cleaned_data['width'], height=form.cleaned_data['height'])
            size = new_image.width, new_image.height
            if parent_image.image:
                im = img.open(parent_image.image)
            elif parent_image.url != '':
                im = img.open(requests.get(parent_image.url, stream=True).raw).convert('RGB')
            if new_image.height is None:
                wpercent = (new_image.width / float(im.size[0]))
                hsize = int((float(im.size[1]) * float(wpercent)))
                im = im.resize((new_image.width, hsize), img.ANTIALIAS)
            elif new_image.width is None:
                wpercent = (new_image.height / float(im.size[1]))
                wsize = int((float(im.size[0]) * float(wpercent)))
                im = im.resize((wsize, new_image.height), img.ANTIALIAS)
            elif new_image.width and new_image.height:
                im = im.resize((new_image.width, new_image.height), img.ANTIALIAS)
            path = settings.MEDIA_ROOT +  '_ID_'+ str(new_image.id) + '.jpg'
            im.save(path, "JPEG")
            new_image.image = '_ID_'+ str(new_image.id) + '.jpg'
            new_image.save()
            return redirect('resize_image', pk=new_image.id)
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})