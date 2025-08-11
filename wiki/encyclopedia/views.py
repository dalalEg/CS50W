from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect 
import markdown2 as markdown
import random

from . import util


def index(request):
        entry =request.GET.get('q', '')
        if entry:
            return redirect(reverse('encyclopedia:search') + f'?q={entry}')
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })  
    

def search(request):
    entry = request.GET.get("q", "")
    content = util.get_entry(entry)
    if content :
            content = markdown.markdown(content)
            return redirect(reverse('encyclopedia:entry', kwargs={'title': entry}))  # Redirect to update URL

    entries = util.list_entries()
    results = [entry1 for entry1 in entries if entry.lower() in entry1.lower()]
    return render(request, "encyclopedia/search.html", {"entries": results})

        




def entry(request, title):
    entry =request.GET.get('q', '')
    if entry:
        return redirect(reverse('encyclopedia:search') + f'?q={entry}')
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {'entry': title ,'message': 'The requested page was not found'})   
    content = markdown.markdown(content)
    return render(request, 'encyclopedia/entry.html',
                   {'entry': title, 'content': content})


def error(request):
    entry =request.GET.get('q', '')
    if entry:
            return redirect(reverse('encyclopedia:search') + f'?q={entry}')
    return render(request, "encyclopedia/error.html")

def add(request):
    if request.method == "GET":
        entry =request.GET.get('q', '')
        if entry:
            return redirect(reverse('encyclopedia:search') + f'?q={entry}')
        else:
           return render(request, "encyclopedia/add.html")
    if request.method == "POST":
        entry =request.POST['entry']
        content = request.POST['content']
        if util.get_entry(entry) is not None:
            return render(request, "encyclopedia/error.html", {'entry': entry, 'message': 'The requested page already exists'})
        else:
            util.save_entry(entry,content )
            return redirect(reverse('encyclopedia:entry', kwargs={'title': entry}))  # Redirect to update URL


def random_entry(request):
    entry =request.GET.get('q', '')
    if entry:
            return redirect(reverse('encyclopedia:search') + f'?q={entry}')
    entries = util.list_entries()  
    entry = random.choice(entries)  
    return redirect(reverse('encyclopedia:entry', kwargs={'title': entry}))  # Redirect to update URL


def edit(request, entry): 
    if request.method == "GET":
        isS =request.GET.get('q', '')
        if isS:
            return redirect(reverse('encyclopedia:search') + f'?q={isS}')
        content = util.get_entry(entry)
        if content is None:
            return render(request, 'encyclopedia/error.html', {'entry': entry, 'message': 'The requested page was not found'})
        return render(request, 'encyclopedia/edit.html', {'entry': entry, 'content': content})
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(entry, content)
        return redirect(reverse('encyclopedia:entry', kwargs={'title': entry}))  # Redirect to update URL
