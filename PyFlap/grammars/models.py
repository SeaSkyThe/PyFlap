from turtle import right
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
    
    def isNonTerminal(self, symbol):
        valid = re.compile('[A-Z]')
        if(valid.match(symbol)):
            return True
        else:
            return False
    
    # Funcao que testa uma sentença de acordo com a gramatica
    # Essa função é recursiva, recebe a sentença, o index atual do caracter a ser verificado pela função e o não terminal atual que está sendo derivado.
    def test_sentence(self, sentence: str, index: int, currentNonTerminal: str) -> bool:
        #Se não foi passado nenhum não terminal - é a primeira iteracao
        if(not currentNonTerminal): 
            currentNonTerminal = self.initial # Se nenhum 'não terminal' foi passado, devemos iniciar pelo simbolo inicial da função.
        
        # Se não tem index definido (posição na sentença analizada), começamos pelo primeiro caracter
        if(not index): 
            index = 0 # definimos como 0
        
        # Se de alguma forma o index for maior que o tamanho da sentença, ocorreu algo errado.
        if(index > len(sentence)):
            print('Problem with the solution. End of sentence.')
            return False
        
        
        # Iniciando teste
        print('\n\nStarting test: ')

        print(f"Testing char '{sentence[index]}' ({index}) from sentence '{sentence}'")

        done = False
        currentIndex = index 
        
        # Verificando qual regra deriva o não terminal atual.
        for rule in Rule.get_all(self.pk): # Pega todas as regras da gramatica e verifica qual delas deriva o não terminal atual.
            if(rule.left_side != currentNonTerminal): # Se a regra do lado esquerdo, for diferente ao não terminal atual
                continue
            
            print(f"Rule for NonTerminal: '{currentNonTerminal}' found. Derivating by the rule: {rule.left_side} -> {rule.right_side}...")
            for derivation in rule.right_side.split('|'): # Para cada derivação existente no lado direito
                currentIndex = index 
                for symbol in derivation: # Para cada simbolo na derivação
                    if(self.isNonTerminal(symbol)): # Verifica se o simbolo é não terminal, se for, deriva ele recursivamente
                        print(f"Non terminal symbol '{symbol}' found. Recursively devirating it from sentence = '{sentence}' currentIndex = '{currentIndex}' symbol = '{symbol}'")
                        done = self.test_sentence(sentence, currentIndex, symbol)
                        if(done):
                            return True
                        else:
                            currentIndex = currentIndex + 1
                    elif(symbol == sentence[currentIndex]): # Se for terminal
                        print(f"Symbol '{symbol}' found in '{derivation}' of '{rule.left_side}' | Sentence = '{sentence}' CurrentIndex = '{currentIndex}' Symbol = '{currentNonTerminal}'")
                        currentIndex = currentIndex + 1
                        if(currentIndex == len(sentence)):
                            done = True
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
    grammar = models.ForeignKey(Grammar, models.CASCADE, related_name="rules")
    left_side = models.CharField(max_length=30)
    right_side = models.CharField(max_length=30)

    @classmethod
    def get_all(cls, grammar_pk: int):
        return cls.objects.filter(grammar__pk=grammar_pk)

    @classmethod
    def create(cls, grammar: Grammar, left_side: str, right_side: str):
        right_side = right_side.replace(" ", "")

        rule = cls.objects.filter(grammar=grammar, left_side=left_side, right_side=right_side)
        if(not rule.exists()):
            rule = cls(grammar=grammar, left_side=left_side, right_side=right_side)
            rule.save()

        return rule



