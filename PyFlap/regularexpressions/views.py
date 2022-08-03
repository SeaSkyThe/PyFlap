from django.shortcuts import render, HttpResponse
import re

from .forms import RegexForm
# Create your views here.
def index(request):
    context = {

    }
    if request.method == 'POST':

        form = RegexForm(request.POST)
        context['regexform'] = form
        if(form.is_valid()):
            if(verify_regex(form['regularexpression'].value(), form['teststring'].value())):
                context['regex_validation'] = True
            else:
                context['regex_validation'] = False
        
        return render(request, 'regularexpressions/index.html', context=context)

    else:
        context['regexform'] = RegexForm()
    
    return render(request, 'regularexpressions/index.html', context=context)



def verify_regex(regex, string):
    print(f'\nVerifying REGEX: {regex} for string {string}\n')
    valid = re.compile(regex)
    if(valid.match(string)):
        return True
    else:
        return False