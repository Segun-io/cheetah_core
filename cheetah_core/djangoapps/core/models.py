from django.db import models

# Create your models here.
class ValveDataAbstract(models.Model):
    name = models.CharField('Name', max_length=50)
    localized_name = models.CharField('Localized name', max_length=50)
    nicknames = models.TextField('Nicknames', blank=True)
    use_custom_image = models.BooleanField('Use custom image?', default=False)
    custom_image = models.ImageField('Custom image', upload_to='custom_images', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
