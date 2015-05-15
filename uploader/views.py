from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from django.views.generic import CreateView, DeleteView
from django.forms import ModelForm
from django.forms import TextInput
import json
from models import Image
from utils import JSONResponse

# Create your views here.

class ImageForm(ModelForm):
    name = TextInput()
    class Meta:
        model = Image
        fields = ["image"]

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()
        name = self.data.get("name")
        image = cleaned_data.get("image")
        image.name = name



class ImageCreateView(CreateView):
    model = Image
    form_class = ImageForm


    def get(self, request, *args, **kwargs):
        context = RequestContext(request)
        images = Image.objects.all()
        context.push({ "images" : images })
        return render_to_response("uploader/image_form.html", context_instance=context)

    def form_valid(self, form):
        self.object = form.save()
        # files = [self.object]
        # data = {'files': files}
        response = JSONResponse({"success" : True}, mimetype='application/json')
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')



class ImageDeleteView(DeleteView):
    model = Image

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype='application/json')
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response