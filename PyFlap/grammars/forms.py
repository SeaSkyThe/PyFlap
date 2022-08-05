from django import forms
import re

letter_uppercase = re.compile('[A-Z]')

class GrammarForm(forms.Form):
    grammarRuleLeft = forms.CharField(label='Grammar Rule - Left Side', max_length=1)
    grammarRuleLeft.widget = forms.TextInput(attrs={'title':'rule_left_side', 'placeholder': 'S, A, etc...', 'class': 'round', 'id': 'rule_left_side', 'maxlength': '1', 'onkeyup': 'this.value = this.value.toUpperCase();'})

    grammarRuleRight = forms.CharField(label='Grammar Rule - Right Side', max_length=100)
    grammarRuleRight.widget = forms.TextInput(attrs={'title':'rule_right_side', 'placeholder': 'aS | bS | a | b', 'class': 'round', 'id': 'rule_right_side',})

    def clean(self):
        super(GrammarForm, self).clean()
        left_side = self.cleaned_data.get('grammarRuleLeft')

        if(not letter_uppercase.match(left_side)):
            self._errors['grammarRuleLeft'] = self.error_class(['The left side of the rule MUST be an uppercase letter [A-Z].'])

        return self.cleaned_data

class GrammarTestForm(forms.Form):
    testString = forms.CharField(label='Test String', max_length=1000)
    testString.widget = forms.TextInput(attrs={'title':'test_string', 'placeholder': 'abb', 'class': 'round', 'id': 'grammar_test_string',})