from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import util
from .util import get_entry


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, title):
    if request.method == "GET":
        print("GET: ", title)
        title_content = get_entry(title)
        if not title_content:
            raise Http404("Page not Found")

        return render(request, "encyclopedia/title.html",
                      {"title": title,"title_content": title_content})

    elif request.method == "POST":
        title = request.POST.get("q")
        print(title)
        title_content = get_entry(title)
        if not title_content:
            return HttpResponseRedirect(reverse("encyclopedia:index"))

        return HttpResponseRedirect(reverse("encyclopedia:wiki_page", title))

