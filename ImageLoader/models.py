from django.db import models
from django.urls import reverse


class Image(models.Model):
    image = models.ImageField(blank=True)
    url = models.URLField(blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('resize_image', args=[str(self.id)])
