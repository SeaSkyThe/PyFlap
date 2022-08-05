from django.shortcuts import render

# Create your views here.
def grammars_page(request):
    context = {
        
    }
    if request.method == "GET":
        return render(request, 'grammars/index.html', context=context)