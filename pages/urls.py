from django.urls import path

from .views import IndexView, ResultView, PDF2ImageView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("result", ResultView.as_view(), name="result"),
    path("pdf2img", PDF2ImageView.as_view(), name="p2i"),
]
