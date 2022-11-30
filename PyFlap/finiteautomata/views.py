from django.shortcuts import render

# Create your views here.

def fa_page(request):
    return render(request, 'finiteautomata/index.html')