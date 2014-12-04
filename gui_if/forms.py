# -*- encoding:UTF-8 -*-
from django import forms

'''
Created on 2014/12/02

@author: user
'''
WIDGET_ATTR = {'class': 'form-control'}

class InputApiKeyForm(forms.Form):
    url = forms.URLField(label=u'プールのURL'
            , help_text=u'例）http://www.mona1.monapool.com'
            , widget=forms.TextInput(attrs=WIDGET_ATTR)
    )
    api_key = forms.CharField(label=u'API Key', widget=forms.TextInput(attrs=WIDGET_ATTR))
