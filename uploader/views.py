from django.shortcuts import render, render_to_response, RequestContext, HttpResponse
from django.views.generic import CreateView
import json
from models import Image
from utils import JSONResponse

# Create your views here.


class ImageCreateView(CreateView):
    model = Image
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        # files = [self.object]
        # data = {'files': files}
        response = JSONResponse({"success" : True} , mimetype='application/json')
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')