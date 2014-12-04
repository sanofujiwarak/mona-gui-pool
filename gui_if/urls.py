# -*- encoding:UTF-8 -*-
from django.conf.urls import patterns, url

import views

'''
Created on 2014/12/03

@author: user
'''
urlpatterns = patterns('',
    # 画像確認用view
    url(r'^image$'
            , views.ImageCheckView.as_view(), name='image'
    ),

    # draft版表示用view
    url(r'^$'
            , views.InputApiKeyView.as_view(), name='input'
    ),

    # worker表示作成view
    url(r'^workers$'
            , views.WorkerView.as_view(), name='workers'
    ),

    # API へのアクセス処理
    url(r'^access_api$'
            , views.AccessApiView.as_view(), name='access_api'
    ),
)
