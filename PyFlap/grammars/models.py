from django.db import models
import re
# Create your models here.
class SingletonModel(models.Model): # SINGLETON
    class Meta:
        abstract = True

    def save(self, *args, **kwargs): # Salva mudanças
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls): # Carrega a gramatica existente, ou cria uma nova
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Grammar(SingletonModel): # GRAMATICA SÓ EXISTE 1
    name = models.CharField(max_length=30, default="grammar")
    initial = models.CharField(max_length=1, default="S")
    regex = models.CharField(max_length=1000, default="")

    def generate_definition(self) -> str: # Funcao que gera a definicao da gramatica no formato G = ({S, A}, {a, b}, P, S)
        terminals = []
        non_terminals = []
        definition = '' # Definition to return
        rules = Rule.objects.filter(grammar__pk=self.pk)

        for rule in rules:
            if(not rule.left_side in non_terminals): # Se a parte esquerda da regra não estiver na lista de não terminais, adiciona
                non_terminals.append(rule.left_side)
            
            right_side = rule.right_side.split('|') # Separando as partes do lado direito
            for part in right_side: # Para cada parte, transformamos ela numa lista de caracteres e verificamos se esse caracter é minusculo, se for, adicionamos à lista de terminais
                for symbol in list(part):
                    if symbol.islower() and not symbol in terminals:
                        terminals.append(symbol)
        
        non_terminals.remove(self.initial) # removendo o simbolo inicial para ordernar a lista e manter ele em primeiro
        non_terminals.sort()
        terminals.sort()

        definition = f"G = ({{{self.initial}, {', '.join(non_terminals)}}}, {{{', '.join(terminals)}}}, P, {self.initial})"

        return definition
    
    # Funcao que testa uma sentença de acordo com a gramatica
    # Essa função é recursiva, recebe a sentença, o index atual do caracter a ser verificado pela função e o não terminal atual que está sendo derivado.
    # def test_sentence(self, sentence: str, index: int, currentNonTerminal: str) -> bool:
    #     #Se não foi passado nenhum não terminal - é a primeira iteracao
    #     if(not currentNonTerminal): 
    #         currentNonTerminal = self.initial # Se nenhum 'não terminal' foi passado, devemos iniciar pelo simbolo inicial da função.
        
    #     # Se não tem index definido (posição na sentença analizada), começamos pelo primeiro caracter
    #     if(not index): 
    #         index = 0 # definimos como 0
        
    #     # Se de alguma forma o index for maior que o tamanho da sentença, ocorreu algo errado.
    #     if(index >= len(sentence)):
    #         print('Problem with the solution. End of sentence.')
    #         return False
        
        
    #     # Iniciando teste
    #     print('\n\nStarting test: ')

    #     print(f"Testing char '{sentence[index]}' ({index}) from sentence '{sentence}'")

    #     done = False
    #     currentIndex = index
    #     # Verificando qual regra deriva o não terminal atual.
    #     for rule in Rule.get_all(self.pk): # Pega todas as regras da gramatica e verifica qual delas deriva o não terminal atual.
    #         if(rule.left_side != currentNonTerminal): # Se a regra do lado esquerdo, for diferente ao não terminal atual
    #             continue
            
    #         print(f"Rule for NonTerminal: '{currentNonTerminal}' found. Derivating by the rule: {rule.left_side} -> {rule.right_side}...")
    #         for derivation in rule.right_side.split('|'): # Para cada derivação existente no lado direito
    #             currentIndex = index 
    #             for symbol in derivation: # Para cada simbolo na derivação
    #                 if(isNonTerminal(symbol)): # Verifica se o simbolo é não terminal, se for, deriva ele recursivamente
    #                     print(f"Non terminal symbol '{symbol}' found. Recursively devirating it from sentence = '{sentence}' currentIndex = '{currentIndex}' symbol = '{symbol}'")
    #                     done = self.test_sentence(sentence, currentIndex, symbol)
    #                     if(done):
    #                         return True
    #                     else:
    #                         currentIndex = currentIndex + 1
    #                 elif(symbol == sentence[currentIndex]): # Se for terminal
    #                     print(f"Symbol '{symbol}' found in '{derivation}' of '{rule.left_side}' | Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}'")
    #                     currentIndex = currentIndex + 1
    #                     if(currentIndex == len(sentence)):
    #                         done = True
    #                     else:
    #                         done = False
    #                 elif(symbol == 'ε'):
    #                     if(sentence == ''):
    #                         print(f'Empty sentence is allowed. Sentence is valid.')
    #                         return True
    #                     if(currentIndex == len(sentence)):
    #                         done = True
    #                     else:
    #                         done = False
    #                     print(f"Symbol 'ε' found. If the sentence is complete '{done}', so done = True")
    #                 else:
    #                     print(f'In this case, the current symbol does not match with the next on the sentence. Finishing derivation.\n\n')
    #                     done = False
    #                     break
         
    #     print(f"\nRecursion finished: Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}' | Result = {done}\n")
    #     print(f"------------------------------------------------------------------------------------------------------------------------------\n")
    #     return done
    def test_sentence(self, sentence: str, index: int, currentNonTerminal: str) -> bool:
        print("\n\nREGEX: ", self.regex)
        if(self.regex != ""):
            matcha = re.fullmatch(self.regex, sentence)
            if(matcha and matcha.group()):
                return True
        
        #Se não foi passado nenhum não terminal - é a primeira iteracao
        if(not currentNonTerminal): 
            currentNonTerminal = self.initial # Se nenhum 'não terminal' foi passado, devemos iniciar pelo simbolo inicial da função.
        # Se não tem index definido (posição na sentença analizada), começamos pelo primeiro caracter
        if(not index): 
            index = 0 # definimos como 0
        
        # Se for uma sentenca vazia, adicionamos o simbolo vazio
        if(sentence==''):
            sentence = 'ε'
        
        # Se de alguma forma o index for maior que o tamanho da sentença, ocorreu algo errado
        if(index >= len(sentence)):
            print('Problem with the solution. End of sentence.')
            return False
        
        
        # Iniciando teste
        print('\n\nStarting test: ')

        print(f"Testing char '{sentence[index]}' ({index}) from sentence '{sentence}'")

        done = False
        currentIndex = index
        # Verificando qual regra deriva o não terminal atual.
        for rule in Rule.get_all_as_unique(self.pk): # Pega todas as regras da gramatica e verifica qual delas deriva o não terminal atual.
            if(rule.left_side != currentNonTerminal): # Se a regra do lado esquerdo, for diferente ao não terminal atual
                continue
            
            print(f"Rule for NonTerminal: '{currentNonTerminal}' found. Derivating by the rule: {rule.left_side} -> {rule.right_side}...")
            for derivation in rule.right_side.split('|'): # Para cada derivação existente no lado direito
                currentIndex = index 
                for symbol in derivation: # Para cada simbolo na derivação
                    if(isNonTerminal(symbol)): # Verifica se o simbolo é não terminal, se for, deriva ele recursivamente
                        print(f"Non terminal symbol '{symbol}' found. Recursively devirating it from sentence = '{sentence}' currentIndex = '{currentIndex}' symbol = '{symbol}'")
                        done = self.test_sentence(sentence, currentIndex, symbol)
                        if(done):
                            if(derivation.index(symbol) + 1 == len(derivation)):
                                print(f"\nRecursion finished: Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}' | Result = {done}\n")
                                return True
                            else:
                                print(f"\nThe character was accepted but the derivation was not finished: Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}' | Derivation = '{derivation}'\n")
                        else:
                            currentIndex = currentIndex + 1
                    elif(symbol == sentence[currentIndex]): # Se for terminal
                        print(f"Symbol '{symbol}' found in '{derivation}' of '{rule.left_side}' | Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}'")
                        currentIndex = currentIndex + 1
                        if(currentIndex == len(sentence)):
                            done = True
                            print(f"\nRecursion finished: Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}' | Result = {done}\n")
                            print(f"------------------------------------------------------------------------------------------------------------------------------\n")
                            return done
                        else:
                            done = False
                    elif(symbol == 'ε'):
                        if(sentence == ''):
                            print(f'Empty sentence is allowed. Sentence is valid.')
                            return True
                        if(currentIndex == len(sentence)):
                            done = True
                        else:
                            done = False
                        print(f"Symbol 'ε' found. If the sentence is complete '{done}', so done = True")
                    else:
                        print(f'In this case, the current symbol does not match with the next on the sentence. Finishing derivation.\n\n')
                        done = False
                        break
         
        print(f"\nRecursion finished: Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}' | Result = {done}\n")
        print(f"------------------------------------------------------------------------------------------------------------------------------\n")
        return done
class Rule(models.Model):
    grammar = models.ForeignKey(Grammar, models.CASCADE, related_name="rules", null=True)
    left_side = models.CharField(max_length=30)
    right_side = models.CharField(max_length=30)

    def __str__(self):
        return f'Rule from Grammar: {self.grammar} | {self.left_side} -> {self.right_side}'

    @classmethod
    def get_all(cls, grammar_pk: int):
        return cls.objects.filter(grammar__pk=grammar_pk)

    @classmethod
    def get_all_as_unique(cls, grammar_pk: int):
        rules = cls.get_all(grammar_pk)
        rules_as_unique = []
        for rule in rules:
            derivations = rule.right_side.split('|')
            #print(f'\n\nDERIVATIONS {derivations} \n-------------------------')
            if(len(derivations) > 1):
                for derivation in derivations:
                    rules_as_unique.append(Rule(left_side=rule.left_side, right_side=derivation))
            else:
                if(rule not in rules_as_unique):
                    rules_as_unique.append(Rule(left_side=rule.left_side, right_side=rule.right_side))
        return rules_as_unique

    @classmethod
    def create(cls, grammar: Grammar, left_side: str, right_side: str):
        right_side = right_side.replace(" ", "")

        rule = cls.objects.filter(grammar=grammar, left_side=left_side, right_side=right_side)
        if(not rule.exists()):
            rule = cls(grammar=grammar, left_side=left_side, right_side=right_side)
            rule.save()

        return rule

def isNonTerminal(symbol):
    valid = re.compile('[A-Z]')
    if(valid.match(symbol)):
        return True
    else:
        return False



 # NAO ESTÁ USANDO
from .tree import Tree, Node
def create_tree_with_grammar():
    # Carrega gramatica e seu simbolo inicial
    grammar = Grammar.load()
    initial = grammar.initial

    # RAIZ GENERICA, P (CONJUNTO DE REGRAS DA GRAMATICA) SERÁ O PAI DE TODOS OS NÓS
    root = Node('S') 
    
    # Passamos, o simbolo inicial da gramática e o nó PAI dos nós a serem criados com esse simbolo.
    derivate_non_terminal(initial, root)
    
    # Por fim criamos a arvore com o nó P como raiz.
    tree = Tree(root=root)       
    print(tree)

# Deriva um não terminal, cria nós filhos que representam esse não terminal e suas derivações, e associa esses nós a um nó pai.
def derivate_non_terminal(non_terminal, father):
    # Carrega gramatica e regras
    grammar = Grammar.load()
    rules = Rule.get_all_as_unique(grammar.pk)

    # Pega apenas as regras referentes ao não terminal que foi passado como param.
    rules_with_current_non_terminal = []
    for rule in rules:
        if(rule.left_side == non_terminal):
            rules_with_current_non_terminal.append(rule)
    
    # Para cada regra desse não terminal:
    #print('--------------------')
    current_nodes_list = []
    for rule in rules_with_current_non_terminal:
        #print(rule)
        stack = [] # Cria-se uma pilha para registrar as derivações feitas.
        current_node = Node(non_terminal)
        
        for derivation in rule.right_side.split('|'): # Para cada derivação existente no lado direito
            # Preparando a pilha
            stack.append(rule.left_side)
            for symbol in derivation: # Para cada simbolo da derivação
                stack.append(symbol) # Colocamos o simbolo na pilha
            
            # Criando a lista que irá ter os nós filhos
            children = []
            # Enquanto a pilha tiver mais de 1 item (todos exceto o não terminal atual)
            while(len(stack) > 0 and stack[-1] != rule.left_side):
                current_symbol = stack.pop()
                new_node = Node(current_symbol)
                if(isNonTerminal(current_symbol)):
                    new_nodes = derivate_non_terminal(current_symbol, current_node)
                    children = children + new_nodes
                    if(len(new_nodes) > 1):
                        new_node = Node(current_symbol, children=new_nodes)
                        children = [new_node]
                    else:
                        children.append(new_nodes[0])
                else:
                    children.append(new_node)
            children.reverse()
            current_node.children = children
            current_nodes_list.append(current_node)
            stack.pop()
        
        father.children.append(current_node)
    return current_nodes_list