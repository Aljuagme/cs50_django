import re
import random

from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import util
from .util import get_entry

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, title):
    print("Title coming from post: ", title)
    if request.method == "GET":
        print("GET: ", title)
        title_content = get_entry(title)
        print("GET: Title Content: ", title_content)
        if not title_content:
            raise Http404("Page not Found")

        return render(request, "encyclopedia/title.html",
                      {"title": title,"title_content": title_content})

    elif request.method == "POST":
        title = request.POST.get("q")
        print("POST: ", title)
        title_content = get_entry(title)
        print("POST: Title Content: ", title_content)
        if not title_content:
            print("Am I here?")
            return entry(request, title)

        return HttpResponseRedirect(reverse("encyclopedia:wiki_page", args=[title]))


def entry(request, title):
    if request.method == "GET":
        print("GET: ENTRY: ", title)
        pass

    if request.method == "POST":
        print("POST: ENTRY: ", title)
        entries = util.find_matching_entry(title)
        print("Print en la entry de entries: ", entries)

        if entries:
            return render(request, "encyclopedia/index.html", {
            "entries": entries})
        else:
            return HttpResponseRedirect(reverse("encyclopedia:index"))


def new_page(request):
    return render(request, "encyclopedia/new_page.html",
                  {"new_entry": NewEntryForm()})


def save_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        print("YEAH, the form: ", form)
        title = form.cleaned_data["title"]
        if title in util.list_entries():
            raise Exception("Title Already Exists")

        title = request.POST.get("title")
        content = request.POST.get("content")

        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:wiki_page", args=[title]))


def random_page(request):
    entries = util.list_entries()
    chosen = random.choice(entries)

    return HttpResponseRedirect(reverse("encyclopedia:wiki_page", args=[chosen]))
