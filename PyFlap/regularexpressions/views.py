from email import header
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
                    context['string_validation1'] = True
                else:
                    context['string_validation1'] = False

                if(verify_regex(form['regularexpression'].value(), form['teststring2'].value())):
                    context['string_validation2'] = True
                else:
                    context['string_validation2'] = False
                
            except Exception as e:
                context['invalid_regex'] = True
                context['error_message'] = str(e)
                
            else:
                if('Source' in request.headers and request.headers['Source'] == 'fetch_api'): # quer dizer que é uma request dinamica feita pelo javascript, assim que o campo de texto é modificado
                    context.pop('regexform')
                    #print(f'{context}')
                    return JsonResponse(data=context)
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