from django.db import models


# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images')
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.image.name

    # def save(self, *args, **kwargs):
    #     self.slug = self.image.name
    #     super(Image, self).save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     self.image.delete(False)
    #     super(Image, self).delete(*args, **kwargs)