from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.

def home(request):
    context = {"site_name": "BuyYourMusic",
               "albums": [
                   {
                       "id": 1,
                       "title": "In Utero",
                       "author": "Nirvana",
                       "year": 1993,
                       "price": 20,
                       "cover": "bym/images/inutero.jpg"
                   },
               ]}
    return render(request, "bym/home.html", context)


def album_detail(request, id):
    context = {
        "title": "In Utero",
        "author": "Nirvana",
        "year": 1993,
        "price": 20,
        "cover": "bym/images/inutero.jpg",
        "rating": 4.3,
        "reviews": [
            {
                "id": 1,
                "user": "user",
                "rating": 5,
                "review": "Written review"
            },
        ]
    }
    return render(request, "bym/album_detail.html", context)