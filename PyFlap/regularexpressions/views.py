from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import re

from .forms import RegexForm
# Create your views here.
def regex_page(request):
    context = {

    }
    if request.method == 'POST':
        form = RegexForm(request.POST)
        context['regexform'] = form
        if(form.is_valid()):
            try:
                if(verify_regex(form['regularexpression'].value(), form['teststring'].value())):
                    context['string_validation'] = True
                else:
                    context['string_validation'] = False
            
                return render(request, 'regularexpressions/index.html', context=context)
            except Exception as e:
                context['invalid_regex'] = True
                context['error_message'] = str(e)
                return render(request, 'regularexpressions/index.html', context=context)

    else:
        context['regexform'] = RegexForm()
    return render(request, 'regularexpressions/index.html', context=context)



def verify_regex(regex, string):
    print(f'\nVerifying REGEX: {regex} for string {string}\n')
    try: # if re.compile works
        valid = re.compile(regex)
        if(valid.match(string)):
            return True
        else:
            return False
    except Exception as e:
        raise e