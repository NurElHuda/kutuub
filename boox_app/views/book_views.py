
import os
from pprint import pprint

from boox_app.constants import REGIONS
from boox_app.models import Book
from boox_app.validators import validate_data
from config.settings import BASE_URL, BOOK_COVERS_PATH, BOOK_COVERS_URL
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class BookList(View):
    model = Book
    context_object_name = "books"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
                
        paginator = Paginator(books, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 
        return render(request, "boox_app/book_list.html", {"page_obj": page_obj})


class BookMine(LoginRequiredMixin, View):
    model = Book
    context_object_name = "books"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(seller=request.user)

        paginator = Paginator(books, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 
        return render(request, "boox_app/book_list.html", {"page_obj": page_obj})


class BookCreation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "boox_app/book_creation.html", {"regions": REGIONS})

    def post(self, request, *args, **kwargs):
        data, errors = validate_data(request.POST)
        pprint(data)

        if errors:
            return render(request, "boox_app/book_creation.html", {"data": data, "errors": errors, "regions": REGIONS})
        obj = Book.objects.create(**data, seller=request.user)
        return redirect("book-detail", pk=obj.pk)


class BookUpdate(LoginRequiredMixin, View):
    def get_object(self):
        obj = get_object_or_404(Book, pk=self.kwargs.get("pk", None))
        return obj

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return render(request, "boox_app/book_update.html", {"book": obj, "regions": REGIONS})

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        data, errors = validate_data(request.POST)

        if errors:
            return render(request, "boox_app/book_update.html", {"book": obj, "data": data, "errors": errors, "regions": REGIONS})

        obj.update(data)
        return redirect("book-detail", pk=obj.pk)


class BookDetail(DetailView):
    model = Book
    context_object_name = "book"


# TODO: login required
class BookCover(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("file", openapi.IN_FORM, type=openapi.TYPE_FILE,),
        ],
        responses={200: "Ok", 400: "Error"},
    )
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file", None)
        if not file_obj:
            raise exceptions.ValidationError(detail={
                "file": "File not found"
            })

        if file_obj.content_type.split("/")[0] != "image":
            raise exceptions.ValidationError(detail={
                "file": "File must be an image"
            })


        fs = FileSystemStorage(location=BOOK_COVERS_PATH)
        file_name = fs.save(file_obj.name, file_obj)

        return Response({
            "file_name": file_name,
            "file_path": f"{BOOK_COVERS_URL}/{file_name}"
        }, status=200)


    parser_classes = (MultiPartParser, FormParser)
