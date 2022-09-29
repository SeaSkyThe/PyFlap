from django import forms

class RegexForm(forms.Form):
    regularexpression = forms.CharField(label='Your Regular Expression', max_length=1000)
    regularexpression.widget = forms.TextInput(attrs={'title':'regularexpression', 'placeholder': 'Type your regular expression', 'class': 'round', 'id': 'regex',})

    teststring = forms.CharField(label='Your test string', max_length=100, empty_value='', required=False)
    teststring.widget = forms.TextInput(attrs={'title':'teststring', 'placeholder': 'Type your string to test', 'class': 'round', 'id': 'test_string',})
    
    teststring2 = forms.CharField(label='Your test string', max_length=100, empty_value='', required=False)
    teststring2.widget = forms.TextInput(attrs={'title':'teststring', 'placeholder': 'Type your string to test', 'class': 'round', 'id': 'test_string2',})