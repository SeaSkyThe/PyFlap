from django import forms

class GrammarForm(forms.Form):
    grammarRuleLeft = forms.CharField(label='Grammar Rule - Left Side', max_length=1000)
    grammarRuleLeft.widget = forms.TextInput(attrs={'title':'rule_left_side', 'placeholder': 'S, A, etc...', 'class': 'round', 'id': 'rule_left_side',})

    grammarRuleRight = forms.CharField(label='Grammar Rule - Right Side', max_length=100)
    grammarRuleRight.widget = forms.TextInput(attrs={'title':'rule_right_side', 'placeholder': 'aS | bS | a | b', 'class': 'round', 'id': 'rule_right_side',})


class GrammarTestForm(forms.Form):
    testString = forms.CharField(label='Test String', max_length=1000)
    testString.widget = forms.TextInput(attrs={'title':'test_string', 'placeholder': 'abb', 'class': 'round', 'id': 'grammar_test_string',})