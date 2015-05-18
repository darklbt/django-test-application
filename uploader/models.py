from datetime import datetime, date
from hashlib import sha256
import os
import shutil
import io
from PIL import Image as PIL_Image
from PIL.ExifTags import TAGS
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.core.files import File
from django.utils.translation import ugettext as _




# Create your models here.
class ExifProperties(models.Model):
    camera_vendor = models.CharField(max_length=120, null=True)
    camera_model = models.CharField(max_length=120, null=True)
    creation_date = models.DateField()

    def clean(self):
        if relativedelta(date.today(), self.creation_date).years > 1:
            raise ValidationError(_("Too old photo!"))


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
            raise ValidationError(_("Exif not found!"))
        ret = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        try:
            creation_date = datetime.strptime(ret['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S").date()
        except:
            raise ValidationError(_("No date in Exif!"))
        exif = ExifProperties(camera_model=ret.get('Model'), camera_vendor=ret.get('Make'), creation_date=creation_date)
        exif.full_clean()
        exif.save()
        self.exif = exif

    def clean(self):

        self.check_image()
        self.check_file_extension()
        self.fill_exif()
        self.create_thumbnail()

    def check_file_extension(self):
        extension = self.image.name.split(".")
        correct_extension = self.image.file.image.format.lower()
        if len(extension) < 2 or extension[1] != correct_extension:
            self.image.name = "{0:s}.{1:s}".format(self.image.name, correct_extension)

    def create_thumbnail(self):
        thumb = PIL_Image.open(self.image.file)
        thumb.thumbnail((200, 200), PIL_Image.ANTIALIAS)
        bytes = io.BytesIO()
        thumb.save(bytes, format='png')
        file = File(bytes)
        self.thumbnail.field.upload_to = self.image.field.upload_to
        self.thumbnail.save("thumbnail-" + self.image.name, file)

    def check_image(self):
        try:
            getattr(self.image, "file")
        except ValueError:
            raise ValidationError(_("It is not image"))
        unique_folder = get_unique_path_to_save(self)
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, unique_folder)):
            raise ValidationError(_("File already exist"))
        self.image.field.upload_to = unique_folder

    def __unicode__(self):
        return self.image.name

    def delete(self, *args, **kwargs):
        path = os.path.dirname(self.image.file.name)
        self.image.delete(False)
        self.thumbnail.delete(False)
        shutil.rmtree(path)
        self.exif.delete()
        super(Image, self).delete(*args, **kwargs)



