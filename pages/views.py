import os
import glob
import requests
from io import BytesIO
import base64
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView, View
from django.conf import settings

from .scripts.file2csv import file2csv
from .scripts.preprocessor import pdf2img
from .forms import ImageForm

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    form = ImageForm(None, None)

    def post(self, request):
        table_csv = settings.MEDIA_ROOT / "csv/output_table.csv"
        info_csv = settings.MEDIA_ROOT / "csv/output_info.csv"
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            path = os.getcwd() + "/media/pages/*"
            file_path = sorted(glob.glob(path, recursive=True), key=os.path.getmtime, reverse=True)[0]
            tables, info = file2csv(
                file_path,
                eval(form.data["table_data"]),
                output_table=table_csv,
                output_info=info_csv,
            )
            request.session["img"] = file_path.split("/")[-1]
            request.session["top"] = info[0]
            request.session["bottom"] = info[1]
            request.session["table"] = tables
            return HttpResponse(status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IndexView.form

        return context


class ResultView(TemplateView):
    template_name = "result.html"


class PDF2ImageView(View):
    def get(self, request):
        return render(request, "")

    def post(self, request):
        file_path = request.POST["file"]
        response = requests.get(file_path)
        if response.status_code == 200:
            blob_data = response.content
        decoded_blob_data = base64.b64decode(blob_data)
        bytes_io = BytesIO(decoded_blob_data)
        with open("/media/pages/mypdf.pdf", "wb") as output_file:
            output_file.write(bytes_io.read())

        return HttpResponse(pdf2img("/media/pages/mypdf.pdf"))
