from turtle import right
from django.db import models

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
    
    def test_sentence(self, sentence: str) -> bool: # Funcao que testa uma sentença de acordo com a gramatica
        print(f"\n\nTESTEI A STRING: {sentence} CONFIA\n\n")


    
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

        


