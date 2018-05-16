from django.urls import path
from . import views
from . import importdata

app_name = 'quandl'
urlpatterns = [

    path('stock',views.stock, name='stock' ),
    path('yale',views.yale, name='yale' ),
    path('lme',views.lme , name='lme'),
    path('lbma',views.lbma , name='lbma'),
    path('future',views.future, name='future' ),
    path('imf',views.imf, name='imf' ),
    path('jodi',views.jodi, name='jodi' ),
    path('bp',views.bp , name='bp'),
    path('johnmatt',views.johnmatt , name='johnmatt'),
    path('umich',views.umich , name='umich'),
    path('ecb',views.ecb ),
    path('fred',views.fred , name='fred'),
    path('fmac',views.fmac , name='fmac'),
    path('gpp',views.gpp , name='gpp'),
    path('ism',views.ism , name='ism'),
    path('comdty',views.comdty , name='comdty'),
    path('trsry',views.trsry , name='treasury'),
    path('urc',views.urc , name='urc'),
    path('quandldata',views.quandldata ),
    path('plotdata',views.plotdata ),
    path('loaditem',views.loaditem ),
    path('loadcntry',views.loadcntry ),
    path('importquandl', importdata.importquandl),
    path('importindicator', importdata.importindicator),
    path('importcountries', importdata.importcountries),
    path('remove',importdata.removeobj),
    
]