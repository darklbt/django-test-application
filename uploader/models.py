from datetime import datetime, date
from hashlib import sha256
import os
import io
from PIL import Image as PIL_Image
from PIL.ExifTags import TAGS
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.files import File




# Create your models here.
class ExifProperties(models.Model):
    camera_vendor = models.CharField(max_length=120, null=True)
    camera_model = models.CharField(max_length=120, null=True)
    creation_date = models.DateField()

    def clean(self):
        if relativedelta(date.today(), self.creation_date ).years > 1:
            raise ValidationError("Too old photo!")


def get_unique_path_to_save(instance):
    unique_folder = sha256(instance.image.file.read()).hexdigest()
    return unique_folder

class Image(models.Model):
    # image = models.ImageField(upload_to=get_unique_path_to_save)
    image = models.ImageField()
    thumbnail = models.ImageField()
    upload_date = models.DateTimeField(auto_now_add=True)
    exif = models.OneToOneField(ExifProperties)

    def fill_exif(self):
        try:
            info = self.image.file.image._getexif()
        except:
            raise ValidationError("Exif not found!")
        ret = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        try:
            creation_date = datetime.strptime(ret['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S").date()
        except:
            raise ValidationError("No date in Exif!")
        exif = ExifProperties(camera_model=ret.get('Model'), camera_vendor=ret.get('Make'), creation_date=creation_date)
        exif.full_clean()
        exif.save()
        self.exif = exif

    def clean(self):
        self.check_image()
        self.fill_exif()
        self.create_thumbnail()

    def create_thumbnail(self):
        thumb = PIL_Image.open(self.image.file)
        thumb.thumbnail((500,500), PIL_Image.ANTIALIAS)
        bytes = io.BytesIO(thumb.tobytes())
        file = File(bytes)
        self.thumbnail.field.upload_to = self.image.field.upload_to
        self.thumbnail.save("thumbnail-"+self.image.name, file)

    def check_image(self):
        unique_folder = get_unique_path_to_save(self)
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, unique_folder)):
                raise ValidationError("File already exist")
        self.image.field.upload_to = unique_folder

    def __unicode__(self):
        return self.image.name

    def delete(self, *args, **kwargs):
        self.image.delete(False)
        self.exif.delete()
        super(Image, self).delete(*args, **kwargs)



