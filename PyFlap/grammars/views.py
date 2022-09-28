from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import GrammarForm, GrammarTestForm
from .models import Grammar, Rule, create_tree_with_grammar
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def grammars_page(request):
    context = {
        
    }
    grammar = Grammar.load()
    rules = Rule.get_all(grammar.pk).order_by('left_side')
    context['rules_objects'] = rules# Enviando todas as regras da gramática para o template
    context['grammar_definition'] = grammar.generate_definition()
    context['grammar'] = grammar
    if request.method == "POST":
        form1 = GrammarForm(request.POST)
        form2 = GrammarTestForm(request.POST)
        
        if(form1.is_valid()): # SE FOR O FORM DE ADICIONAR REGRA NA GRAMATICA
            # Criando a RULE de acordo com os valores que vieram do FORM (lado esquerdo e lado direito)
            Rule.create(grammar=grammar, 
                        left_side=form1['grammarRuleLeft'].value(), 
                        right_side=form1['grammarRuleRight'].value())
            
            # Setando o inicial, se existir uma regra que deriva esse simbolo
            new_initial = form1['grammarInitial'].value()
            for rule in rules:
                if(rule.left_side == new_initial):
                    grammar.initial = new_initial
                    grammar.save()
                    break
            
            # Atualizando variáveis que serão enviadas para o template (HTML)
            context['grammarform'] = form1 # Form de adicionar rule é enviado com a request
            context['grammartestform'] = GrammarTestForm() # Form de testar gramatica é enviado vazio
            
            
        elif(form2.is_valid()): # SE FOR O FORM DE TESTAR A GRAMATICA
            #create_tree_with_grammar()
            context['grammartestform'] = form2
            context['grammarform'] = GrammarForm(initial={'grammarInitial': grammar.initial})
            sentence_test = grammar.test_sentence(sentence=form2['testString'].value(), index=None, currentNonTerminal='') # Funcao que verifica a validade da sentença de acordo com a gramatica existente
            context['sentence_test'] = sentence_test
            return render(request, 'grammars/index.html', context=context) # renderiza com as variáveis setadas
        
        else:
            print(f'\n\nNENHUM FORM VALIDO: {form1.is_valid()}\n\n')

        return HttpResponseRedirect(reverse('grammars_page'))

    else: # caso seja uma GET REQUEST (ou seja, chamando a pagina)
        context['grammarform'] = GrammarForm(initial={'grammarInitial': grammar.initial}) # Passando os formularios que serão exibidos
        context['grammartestform'] = GrammarTestForm(initial={'testString': ''})


    return render(request, 'grammars/index.html', context=context) # renderiza com as variáveis setadas
    

def verify_rules_with_initial_symbol(current_rule):
    rules = Rule.objects.all()
    
    grammar = Grammar.load()
    for rule in rules:
        if(rule != current_rule):
            if(rule.left_side == grammar.initial):
                return True
    return False
def delete_rule(request, id):
    rule = Rule.objects.get(pk=id)
    grammar = Grammar.load()
    if(rule.left_side == grammar.initial): # Se tiver tentando remover uma regra com o simbolo inicial, garantimos que existe outra
        if(verify_rules_with_initial_symbol(rule)):
            rule.delete()
    else:
        rule.delete()
    return redirect('grammars_page')

def delete_all_rules(request):
    Rule.objects.all().delete()
    return redirect('grammars_page')






 


