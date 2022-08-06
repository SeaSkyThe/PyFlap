from turtle import right
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import GrammarForm, GrammarTestForm
from .models import Grammar, Rule
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def grammars_page(request):
    context = {
        
    }
    grammar = Grammar.load()
    if request.method == "POST":
        form1 = GrammarForm(request.POST)
        form2 = GrammarTestForm(request.POST)
        
        if(form1.is_valid()): # SE FOR O FORM DE ADICIONAR REGRA NA GRAMATICA
            # Setando o inicial
            grammar.initial = form1['grammarInitial'].value()
            grammar.save()

            # Agora criando a RULE de acordo com os valores que vieram do FORM (lado esquerdo e lado direito)
            rule = Rule(grammar=grammar, 
                        left_side=form1['grammarRuleLeft'].value(), 
                        right_side=form1['grammarRuleRight'].value().replace(" ", ""))
            rule.save() # Salvando a nova regra da gramática

            # Atualizando variáveis que serão enviadas para o template (HTML)
            context['grammarform'] = form1 # Form de adicionar rule é enviado com a request
            context['grammartestform'] = GrammarTestForm() # Form de testar gramatica é enviado vazio
            
            
        elif(form2.is_valid()): # SE FOR O FORM DE TESTAR A GRAMATICA
            context['grammartestform'] = form2
            context['grammarform'] = GrammarForm()
            grammar.test_sentence(sentence=form2['testString'].value()) # Funcao que verifica a validade da sentença de acordo com a gramatica existente

        else:
            print(f'\n\nNENHUM FORM VALIDO: {form1.is_valid()}\n\n')

        return HttpResponseRedirect(reverse('grammars_page'))

    else: # caso seja uma GET REQUEST (ou seja, chamando a pagina)
        context['grammarform'] = GrammarForm(initial={'grammarInitial': grammar.initial}) # Passando os formularios que serão exibidos
        context['grammartestform'] = GrammarTestForm()
        context['rules_objects'] = Rule.get_all(grammar.pk) # Enviando todas as regras da gramática para o template
        context['grammar_definition'] = grammar.generate_definition()
        context['grammar'] = grammar

    return render(request, 'grammars/index.html', context=context) # renderiza com as variáveis setadas
    

def delete_rule(request, id):
    rule = Rule.objects.get(pk=id)
    rule.delete()
    return redirect('grammars_page')

def delete_all_rules(request):
    Rule.objects.all().delete()
    return redirect('grammars_page')






 


