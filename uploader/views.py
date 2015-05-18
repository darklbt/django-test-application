from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from django import forms
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext as _
import json

from models import Image
from utils import JSONResponse

# Create your views here.

class ImageForm(ModelForm):
    """
    Форма создания модели Image
    """
    class Meta:
        model = Image
        fields = ["image"]

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()
        name = self.data.get("name")
        image = cleaned_data.get("image")
        if  image:
            image.name = name
        return cleaned_data





class ImageCreateView(CreateView):
    """
    Главная вьюха. По get - отдает главную страницу с формой згрузки. По post - сохраняет новое изображение.
    """
    model = Image
    form_class = ImageForm


    def get(self, request, *args, **kwargs):
        context = RequestContext(request)
        images = Image.objects.all()
        context.push({ "images" : images })
        return render_to_response("uploader/image_form.html", context_instance=context)

    def form_valid(self, form):
        """
        Если валидация прошла успешно - сохраним данные из формы и отправим сообщение, что все хорошо.
        :param form: форма
        :return:
        """
        self.object = form.save()
        response = JSONResponse({"success" : True}, mimetype='application/json')
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        """
        Если в процессе сохранения что-то пошло не так - отправим ошибку на клиент. Так как сохранение выполняется
         ajax-запросами, то шибку отправим в виде json.
        :param form:
        :return:
        """
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')



class ImageDeleteView(DeleteView):
    """
    Вьюха для удаления изображения.
    """

    model = Image

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype='application/json')
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

class ImageListView(ListView):
    """
    Возвращает таблицу с загруженными изображениями.
    """
    model = Image

    def get(self, request, *args, **kwargs):
        context = RequestContext(request)
        context.push({"images" : self.get_queryset() })
        return render_to_response("uploader/image_list.html", context_instance=context)
