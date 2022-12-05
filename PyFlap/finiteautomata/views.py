from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from finiteautomata.finite_automata import FiniteAutomata

import re
# Create your views here.


def fa_page(request):
    if(request.is_ajax()):
        # Verify if automata is valid
#         a = {'nodes': [{'data': {'id': 'q0', 'is_initial': True, 'is_final': True}, 'position': {'x': 213.5, 'y': 235}, 'group': 'nodes', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': False, 'classes': 'automove-viewport'}, {'data': {'id': 'q1'}, 'position': {'x': 460.5, 'y': 241}, 'group': 'nodes', 
# 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': False, 'classes': 'automove-viewport'}, {'data': {'id': 'q2'}, 'position': {'x': 681.5, 'y': 232}, 'group': 'nodes', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': False, 'classes': 'automove-viewport'}], 'edges': [{'data': {'source': 'q0', 'target': 'q1', 'id': 'a4766617-e65c-4a0f-a042-39bbd09bda59', 'label': '1'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}, {'data': {'source': 'q1', 'target': 'q2', 'id': '4a31dee8-eddd-4e0a-ab22-23a4ebb951f8', 'label': '0'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}, {'data': {'source': 'q2', 'target': 'q1', 'id': 'f2624e70-6c70-45ec-aef8-51e407976f0b', 'label': '0'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}, {'data': {'source': 'q1', 'target': 'q0', 'id': '03ccb6e9-79a8-4176-8117-5900fdf517a0', 'label': '1'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}, {'data': {'source': 'q2', 'target': 'q2', 'id': 'fe86a58f-1fce-42ae-84e1-a7ed5cd90e59', 'label': '1'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': True, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}, {'data': {'source': 'q0', 'target': 'q0', 'id': 'e7ea72d9-75d8-442b-bdb2-5d4af0e67ad0', 'label': '0'}, 'position': {'x': 0, 'y': 0}, 'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False, 'grabbable': True, 'pannable': True, 'classes': ''}]}
#         sentence = '1010'

        #print(json.loads(request.body)['finite_automata'])
        try:
            fa = FiniteAutomata(json.loads(request.body)['finite_automata'])
            sentence = json.loads(request.body)['sentence']
        except:
            return JsonResponse({'sentence_accepted': 'error', 'message': 'Verifique se seu autômato está completo e se a sentença testada tem caracteres válidos.'})
        if(not sentence):
            sentence=''
        
        try:
            regex = fa.convert_fa_to_regex()
        except:
            return JsonResponse({'sentence_accepted': 'error', 'message': 'Verifique se seu autômato está completo e se a sentença testada tem caracteres válidos.'})
        raw_regex = r'{}'.format(regex)
        
        print("\n", raw_regex, "\n")
        matcha = re.fullmatch(raw_regex, sentence)
        if(matcha and matcha.group()):
            #return HttpResponse({'sentence_accepted': False})
            return JsonResponse({'sentence_accepted': 'true'})
        else:
            return JsonResponse({'sentence_accepted': 'false'})
        
        
    if(request.method == 'GET'):
        return render(request, 'finiteautomata/index.html')