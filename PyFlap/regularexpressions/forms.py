from django import forms

class RegexForm(forms.Form):
    regularexpression = forms.CharField(label='Your Regular Expression', max_length=1000)
    regularexpression.widget = forms.TextInput(attrs={'title':'regularexpression', 'placeholder': 'Digite sua expressão regular', 'class': 'round', 'id': 'regex',})

    teststring = forms.CharField(label='Your test string', max_length=100, empty_value='', required=False)
    teststring.widget = forms.TextInput(attrs={'title':'teststring', 'placeholder': 'Digite sua string de teste', 'class': 'round', 'id': 'test_string',})
    
    teststring2 = forms.CharField(label='Your test string', max_length=100, empty_value='', required=False)
    teststring2.widget = forms.TextInput(attrs={'title':'teststring', 'placeholder': 'Digite sua string de teste', 'class': 'round', 'id': 'test_string2',})