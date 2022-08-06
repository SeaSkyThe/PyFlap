from django import forms
import re

letter_uppercase = re.compile('[A-Z]')

class GrammarForm(forms.Form):
    grammarRuleLeft = forms.CharField(label='Grammar Rule - Left Side', max_length=1)
    grammarRuleLeft.widget = forms.TextInput(attrs={'title':'rule_left_side', 'placeholder': 'S, A, etc...', 'class': 'round', 'id': 'rule_left_side', 'maxlength': '1'})

    grammarRuleRight = forms.CharField(label='Grammar Rule - Right Side', max_length=100)
    grammarRuleRight.widget = forms.TextInput(attrs={'title':'rule_right_side', 'placeholder': 'aS | bS | a | b', 'class': 'round', 'id': 'rule_right_side',})

    grammarInitial = forms.CharField(label='Grammar Initial', max_length=1)
    grammarInitial.widget = forms.TextInput(attrs={'title':'grammar_initial', 'placeholder': 'S, A, etc...', 'class': 'round', 'id': 'grammar_initial', 'maxlength': '1'})

    def clean(self):
        super(GrammarForm, self).clean()

        # VERIFICANDO O CAMPO DE SIMBOLO INICIAL
        initial_symbol = self.cleaned_data.get('grammarInitial')
        if(initial_symbol):
            if(not letter_uppercase.match(initial_symbol)):
                self._errors['grammarInitial'] = self.error_class(['The initial symbol MUST be an uppercase letter [A-Z].'])
        else:
            self._errors['grammarInitial'] = self.error_class(['The initial symbol CANNOT be empty.'])


        # VERIFICANDO O LADO ESQUERDO DA REGRA
        left_side = self.cleaned_data.get('grammarRuleLeft')

        if(left_side):
            if(not letter_uppercase.match(left_side)):
                self._errors['grammarRuleLeft'] = self.error_class(['The left side of the rule MUST be an uppercase letter [A-Z].'])
        else:
            self._errors['grammarRuleLeft'] = self.error_class(['The left side of the rule CANNOT be empty.'])

        return self.cleaned_data

class GrammarTestForm(forms.Form):
    testString = forms.CharField(label='Test String', max_length=1000)
    testString.widget = forms.TextInput(attrs={'title':'test_string', 'placeholder': 'abb', 'class': 'round', 'id': 'grammar_test_string',})