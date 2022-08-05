from django.shortcuts import render
from .forms import GrammarForm, GrammarTestForm

# Create your views here.
def grammars_page(request):
    context = {
        
    }
    if request.method == "POST":
        form1 = GrammarForm(request.POST)
        form2 = GrammarTestForm(request.POST)
        
        if(form1.is_valid()): # SE FOR O FORM DE ADICIONAR REGRA NA GRAMATICA
            print(f'Form 1 é valido\n\n')
            context['grammarform'] = form1
            context['grammartestform'] = GrammarTestForm()

        elif(form2.is_valid()): # SE FOR O FORM DE TESTAR A GRAMATICA
            print(f'\n\nForm 2 é valido\n\n')
            context['grammartestform'] = form2
            context['grammarform'] = GrammarForm()
        else:
            pass
        return render(request, 'grammars/index.html', context=context)
    else:
        context['grammarform'] = GrammarForm()
        context['grammartestform'] = GrammarTestForm()
        
    return render(request, 'grammars/index.html', context=context)

def test_sentence_handle(request):
    pass