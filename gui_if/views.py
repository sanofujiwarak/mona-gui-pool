# -*- encoding:UTF-8 -*-
import json

from django.http import HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

import requests

import api_wrapper, forms, utils

'''
Created on 2014/12/02

@author: user
'''
class ImageCheckView(TemplateView):
    '''
    画像確認用view
    '''
    template_name = 'gui_if/image.html'

class InputApiKeyView(FormView):
    '''
    draft版表示用view
    '''
    form_class = forms.InputApiKeyForm
    template_name = 'gui_if/input.html'

    def form_valid(self, form):
        '''
        formのvalidationがOKの場合
        '''
        # url、api_key を渡す
        context = self.get_context_data()
        context['url'] = form.cleaned_data['url']
        context['api_key'] = form.cleaned_data['api_key']

        # 絶対URL
        context['absolute_url'] = utils.get_absolute_url(self.request)

        # Dashboard画面 を表示する
        return self.response_class(
            request=self.request,
            template='gui_if/dashboard.html',
            context=context,
            content_type=self.content_type,
        )

class WorkerView(TemplateView):
    '''
    worker表示作成view
    '''
    # GET のみ許可
    http_method_names = ['get']
    template_name = 'gui_if/worker.html'

    def get_context_data(self, **kwargs):
        '''
        表示情報の取得
        '''
        context = super(WorkerView, self).get_context_data(**kwargs)

        # worker情報
        context['workers'] = api_wrapper.get_worker_info(
                self.request.GET['url'], self.request.GET['api_key']
        )

        # hashrate の単位
        context['unit'] = self.request.GET['unit']

        return context

class JsonpResponse(HttpResponse):
    '''
    JSONPレスポンス
    '''
    def __init__(self, content, status=None
            , content_type='application/json', callback='callback'
    ):
        super(JsonpResponse, self).__init__(
                content=callback + '(' + json.dumps(content) + ')',
                status=status,
                content_type=content_type,
        )

class AccessApiView(View):
    '''
    API へのアクセス処理
    Response は JSONPで返す
    '''
    # GET のみ許可
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        '''
        表示情報の取得
        '''
        url = self.request.GET['url']
        key = self.request.GET['api_key']

        # JSONPにはviewのcontext情報を入れない
        context = kwargs

        # getdashboarddata
        dashboard = api_wrapper.get_dashboard_data(url, key)
        context['hashrate'] = dashboard['hashrate']
        context['unit'] = dashboard['unit']
        context['currency'] = dashboard['currency']

        # getusertransactions
        context['credit'] = api_wrapper.get_credit(url, key)['credit']

        # getuserworkers は別viewからアクセスする
        r = requests.get(utils.get_absolute_url(self.request) + '/workers'
                , params={'url': url, 'api_key': key, 'unit': context['unit']}
        )
        context['worker'] = r.text

        return context

    def get(self, request, *args, **kwargs):
        '''
        get時の処理
        '''
        if not 'callback' in self.request.GET:
            # GETパラメータ内に'callback'が存在しない場合
            return HttpResponse('You must pass a callback parameter.')

        else:
            # GETパラメータ内に'callback'が存在する場合
            return JsonpResponse(
                    self.get_context_data(**kwargs), callback=request.GET['callback']
            )
