from django.shortcuts import render
from django.http import JsonResponse

import requests
import pandas as pd
from datetime import datetime, timedelta
from .models import API_keys, Items_table, Countries, Indicators
import json

import numpy as np


# to use mongodb
# from pymongo import MongoClient
# MONGO_HOST= 'mongodb://127.0.0.1:27017' 
# client = MongoClient(MONGO_HOST)
# db = client.local 


def diff_by_freq(d1,d2,freq):
    du=datetime.strptime(d1,'%Y-%m-%d')
    dl=datetime.strptime(d2,'%Y-%m-%d')
    if freq=='daily':
        dmax=(du-dl).days
    elif freq=='weekly':
        dmax=(du-dl).days/7
    elif freq=='monthly':
        dmax=(du.year - dl.year) * 12 + du.month - dl.month
    elif freq=='quarterly':
        dmax=((du.year - dl.year) * 12 + du.month - dl.month)/3
    else:
        dmax=du.year-dl.year
    return dmax


def freq2days(freq,type):
    if type==0:
        if freq=='daily': res=1
        elif freq=='weekly': res=7
        elif freq=='monthly': res=30
        elif freq=='quarterly': res=90
        else: res=365
    elif type==1:
        if int(freq)==1: res='daily'
        elif int(freq)==7: res='weekly'
        elif int(freq)==30: res='monthly'
        elif int(freq)==90: res='quarterly'
        else: res='annual'
    else:
        if freq=='daily': res='days'
        elif freq=='weekly': res='weeks'
        elif freq=='monthly': res='months'
        elif freq=='quarterly': res='quarters'
        else: res='years'
    return res      


def quandl_content(title, dataset,default_item, col_index,sorting, category, country, ctype):

    start_date=(datetime.now()-timedelta(3*365)).strftime('%Y-%m-%d')
    end_date=datetime.now().strftime('%Y-%m-%d')
    items=Items_table.objects.filter(dataset=dataset).order_by(sorting)

    url = 'https://www.quandl.com/api/v3/datasets/{}/{}'  \
					+ '.json?&api_key=xgnhYnpkFuqTgBDX4bjK&start_date={}&end_date={}&order=asc&collapse=none&transform=none&column_index={}'
    dataurl=url.format(dataset,default_item,start_date,end_date,col_index)
    print(dataurl)
    result=requests.get(dataurl).json()
    freq=result['dataset']['frequency']
    lower_limit=result['dataset']['oldest_available_date']
    upper_limit=result['dataset']['newest_available_date']

    freq_days=freq2days(freq,0)
    freq_unit=freq2days(freq,2)
    if category.upper()=='Y':
        cat_list=items.values('category').distinct()
    else:
        cat_list=None
    if country.upper()=='Y':
        cntry_list=Items_table.objects.filter(dataset=dataset).order_by('country').values('ccode','country').distinct()    
    else:
        cntry_list=None

    context={'title':title,'dataset':dataset, 'items': items ,  'category':cat_list ,'ccode':cntry_list,
            'default_item':default_item, 'default_title':result['dataset']['name'] , 'col_index': col_index, 'ctype': ctype, 
            'min':lower_limit, 'max':upper_limit, 'start_date':start_date,'end_date':end_date, 'freq_days':freq_days, 'freq_unit':freq_unit }
    return context

def stock(request):
    # if request.method=='POST':
    #     form=  ItemForm(request.POST)
    #     form.save()
        
    # key=API_keys.object.all()

    # url=''
    # result=requests.get(url).json()
    # print(r.text)
    # item1=result['item']

    # items={
    #     'item1': result['item1'],
    #     'item2': result['item2']
    # }
    # context={'items':items}
    # return render(request, 'quandl_chart/index.html', context) 

    
    dataset='WIKI'
    default_item='AAPL'
    title='Stock Markets'
    col_index='11'
    ctype='line'
    sorting='description'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'n','n',ctype)

    return render(request, 'quandl_chart/chart.html', context)



def yale(request):
    dataset='YALE'
    default_item='RHPI'
    title='Yale Housing Market Indicators'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    
    return render(request, 'quandl_chart/chart.html', context)


def lme(request):

    dataset='LME'
    default_item='PR_AL'
    title='LME Markets'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    
    return render(request, 'quandl_chart/chart.html', context)
    #lme_items=db.quandl.find({'dataset':'LME'}).sort('symbol')


def johnmatt(request):

    dataset='JOHNMATT'
    default_item='PLAT'
    title='Rare Metal Markets'
    col_index='1'
    ctype='line'
    sorting='description'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'n','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)


def future(request):

    dataset='CHRIS'
    default_item='MCX_CL1'
    title='Future Markets'
    col_index='1'
    ctype='line'
    sorting='symbol'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'n','n',ctype)
    
    return render(request, 'quandl_chart/chart.html', context)


def imf(request):
    dataset='ODA'
    default_item='KOR_LP'
    title='IMF Macroeconomic Indicators'
    col_index='1'
    ctype='bar'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','y',ctype)
    return render(request, 'quandl_chart/chart.html', context)

def jodi(request):

    dataset='JODI'
    default_item='OIL_TCPRBK_WORLD'
    title='JODI Oil Statistics'
    col_index='1'
    ctype='bar'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','y',ctype)
   
    return render(request, 'quandl_chart/chart.html', context)


def bp(request):

    dataset='BP'
    default_item='OIL_RESERVES_WRLD'
    title='BP Energy Statistics'
    col_index='1'
    ctype='bar'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','y',ctype)
   
    return render(request, 'quandl_chart/chart.html', context)

def umich(request):

    dataset='UMICH'
    default_item='SOC1'
    title='University of Michigan Consumer Surveys'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    
    return render(request, 'quandl_chart/chart.html', context)

def lbma(request):

    dataset='LBMA'
    default_item='GOLD'
    title='London Bullion Market'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    
    return render(request, 'quandl_chart/chart.html', context)


def fmac(request):
 
    dataset='FMAC'
    default_item='FIX30YR'
    title='Freddie MAC Housing Indicators'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
 
    return render(request, 'quandl_chart/chart.html', context)


def fred(request):

    dataset='FRED'
    default_item='GDP'
    title='Fed Macroeconomic Indicators'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)

def gpp(request):

    dataset='GPP'
    default_item='CFP_KOR'
    title='Global Petrol Prices'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)


def ism(request):
    
    dataset='ISM'
    default_item='MAN_PMI'
    title='ISM Business Sentiment'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)


def comdty(request):
    
    dataset='COM'
    default_item='PALLFNF_INDEX'
    title='Commodity Markets'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)

def urc(request):
    
    dataset='URC'
    default_item='NYSE_ADV'
    title='Stock Market ADV'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)

def trsry(request):
    
    dataset='USTREASURY'
    default_item='YIELD'
    title='US Treasury Yields'
    col_index='1'
    ctype='line'
    sorting='description'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'n','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)



def wwgi(request):
    
    dataset='WWGI'
    default_item='PV_EST'
    title='Political Stability'
    col_index='1'
    ctype='line'
    sorting='category'
    context=quandl_content(title, dataset,default_item,col_index,sorting,'y','n',ctype)
    return render(request, 'quandl_chart/chart.html', context)



def ecb(request):
    items=Items_table.objects.filter(dataset='ECB').order_by('description')
    context={'title':'ECB Statistics', 'dataset':'ECB', 'items': items, 'default_item':'BKN_M_U2_NC10_B_10P1_AS_S_E', 'default_title':'Euro area Net Circulation Banknotes 10 All design series Stock denominated in Euro' , 'ctype':'bar'  }
    return render(request, 'quandl_chart/chart.html', context)

def loaditem(request):
    dataset=request.GET['dataset'].upper()
    if request.GET['category']!='':
        category=request.GET['category']
        print(category)
        try:
            ccode=request.GET['ccode']
            items=Items_table.objects.filter(dataset=dataset,category=category,ccode=ccode).order_by('description').values('symbol','description').distinct()
        except:
            items=Items_table.objects.filter(dataset=dataset,category=category).order_by('description').values('symbol','description').distinct()
        item_list=[]
        for item in items:
            item_list.append(item)
        content={'items':item_list}
            
        return JsonResponse(content)
    else:
        items=Items_table.objects.filter(dataset=dataset).order_by('description').values('symbol','description').distinct()
        item_list=[]
        for item in items:
            item_list.append(item)
        content={'items':item_list}
        return JsonResponse(content)

def loadcntry(request):
    dataset=request.GET['dataset'].upper()
    category=request.GET['category']
    items=Items_table.objects.filter(dataset=dataset,category=category).order_by('country').values('ccode','country').distinct()
    cntry_list=[]
    for item in items:
        cntry_list.append(item)
    return JsonResponse({'countries':cntry_list})



def quandldata(request):
    dataset=request.GET['dataset'].upper()
    symbol=request.GET['symbol'].upper()
    if symbol=='UNDEFINED':
        symbol='AAPL'
    
    try:
        freq_days=request.GET['freq_days']
        
    except: 
        freq_days=1
    freq=freq2days(freq_days,1)
    print(freq)
    if request.GET['start_date']=='':
        start_date=''
    else:
        start_date=request.GET['start_date']
    if request.GET['end_date']=='':
        end_date=''
    else:    
        end_date=request.GET['end_date']
        
    try:    
        if request.GET['range']=='max': 
            start_date=''
            end_date=''
    except:
        pass
   
 
    transform=request.GET['transform']
    
        
 
    # if dataset=='WIKI':
    #     start_date=(datetime.now()+timedelta(days=-300)).strftime('%Y-%m-%d')
    # else:
    #     start_date=(datetime.now()+timedelta(weeks=-500)).strftime('%Y-%m-%d')        

    url = 'https://www.quandl.com/api/v3/datasets/{}/{}'  \
					+ '.json?&api_key=xgnhYnpkFuqTgBDX4bjK&start_date={}&end_date={}&order=asc&collapse={}&transform={}&column_index={}'
    
    try:
        col_index=request.GET['col_index']
    except:
        col_index=1
    dataurl=url.format(dataset,symbol,start_date,end_date,freq,transform,col_index)
    print(dataurl)
    result=requests.get(dataurl).json()
    name=result['dataset']['name']

    desc=result['dataset']['description']
    freq_act=result['dataset']['frequency']

    df=pd.DataFrame(result['dataset']['data'], columns=result['dataset']['column_names'])
    df['Date']=pd.DatetimeIndex(df.iloc[:,0]).strftime("%Y-%m-%d")
    df.iloc[:,1]=round(df.iloc[:,1],2)
    label=list(df.Date)
    data=list(df.iloc[:,1])
    
    freq_act_days=int(freq2days(freq_act,0))
    
    freq_days=int(freq_days)
    freq_max_days=max(freq_days,freq_act_days)
    
    freq_max=freq2days(freq_max_days,1)
    print(freq_max)
    max_timedelta=diff_by_freq(result['dataset']['newest_available_date'],result['dataset']['oldest_available_date'],freq_max)
    dsc_table=df.iloc[:,1].describe().to_json()
    print(dsc_table)
    if len(data)<=40 and (transform=="rdiff" or transform=="rdiff_from"): 
        ctype='bar'
    else: 
        ctype='line'
    content={'label':label,'data':data, 'col_index':col_index, 'ctype':ctype, 'dsc_table':dsc_table, 'name':name, 'desc':desc, 
            'freq':freq_max, 'freq_days':freq_days, 'max_timedelta':max_timedelta, 'freq_act_days':freq_max_days }

    return  JsonResponse(content)


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import style
#import mpld3
#from mpld3 import plugins
import mglearn
from cycler import cycler

import io
import base64
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas import Series

matplotlib.rc('font', family='NanumBarunGothic', size='5')
matplotlib.rcParams['axes.unicode_minus'] = False


plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 200
plt.rcParams['image.cmap'] = "viridis"
plt.rcParams['image.interpolation'] = "none"
plt.rcParams['savefig.bbox'] = "tight"
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['legend.numpoints'] = 1
plt.rcParams['interactive'] = False

plt.rc('axes', prop_cycle=(
    cycler('color', mglearn.plot_helpers.cm_cycle.colors) +
    cycler('linestyle', ['-', '-', "--", (0, (3, 3)), (0, (1.5, 1.5))])))

np.set_printoptions(precision=3, suppress=True)

pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows", 50)
pd.set_option('precision', 2)

style.use('seaborn-muted')


def plotdata(request):
    plottype=request.GET['plottype'].upper()
    
    dataset=request.GET['dataset'].upper()
    symbol=request.GET['symbol'].upper()
    if symbol=='UNDEFINED':
        symbol='AAPL'
    freq_days=request.GET['freq_days']
    try:
        freq=freq2days(freq_days,1)
    except: 
        freq='daily'

    rng=request.GET['range']
    try:
        start_date=request.GET['start_date']
    except:
        if rng=='max': start_date=''
        else : start_date=(datetime.now()-timedelta(float(rng)*365)).strftime('%Y-%m-%d')
    try:
        end_date=request.GET['end_date']
    except:
        end_date=datetime.now().strftime('%Y-%m-%d')
    transform=request.GET['transform']
    plottype=request.GET['plottype']


    url = 'https://www.quandl.com/api/v3/datasets/{}/{}'  \
                    + '.json?&api_key=xgnhYnpkFuqTgBDX4bjK&start_date={}&end_date={}&order=asc&collapse={}&transform={}&column_index={}' 
    try:
        col_index=request.GET['col_index']
    except:
        col_index=1
    dataurl=url.format(dataset,symbol,start_date,end_date,freq,transform,col_index)
    print(dataurl)
    result=requests.get(dataurl).json()
    df=pd.DataFrame(result['dataset']['data'], columns=result['dataset']['column_names'])

    df['Date']=pd.DatetimeIndex(df.iloc[:,0]).strftime("%Y-%m-%d")
    print(df)  
    df.iloc[:,1]=round(df.iloc[:,1],2)
    new_df=df.iloc[:,0:2]
    new_df=new_df.set_index('Date')

    series=Series(new_df.iloc[:,0])
    print(series)
    if plottype=='hist':
    #try:
        fig, ax = plt.subplots(figsize=(4,3),edgecolor='lightgray')
        plt.title('Probability Distribution')
        ax.grid(color='lightgray', alpha=0.7, linewidth=0.5)
        df.iloc[:,1].plot(kind='kde',style='k--')
        df.iloc[:,1].hist(bins=30, alpha=0.3, color='g', normed=True)
        count, division = np.histogram(df.iloc[:,1])
        print(count)
        print(np.around(division,0))
        kurtosis=round(df.iloc[:,1].kurtosis(),4)
        skew=round(df.iloc[:,1].skew(),4)
        f = io.BytesIO()
        plt.savefig(f, format="png")
        encoded_img = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
        f.close()
        fig.clear() 
        return  JsonResponse({'imagedata':'<img src="data:image/png;base64,%s" />' % encoded_img, 'kurtosis':kurtosis, 'skew':skew},safe=False)
    
    # df_min=df.iloc[:,1].min()*0.9
    # df_max=df.iloc[:,1].max()*1.1
    # df_mode=df_max-df_min
    # d=len((str(df_mode).split('.'))[0])
    # if d==1:d=3
    # else: d=-d+3
    # bins=np.arange(round(df_min,d-1),round(df_max,d-1),round(df_mode/20,d))
    # label=np.around(bins[1:],d).tolist()
    # data=df.groupby(pd.cut(df.iloc[:,1], bins=bins)).count().iloc[:,1]
    # content={'label':label,'data':list(data)}
    # return  JsonResponse(content)
        
    #except:
    #    return  JsonResponse('<h6>No plot</h6>', safe=False)
    elif plottype=='trend':
        freq_act=result['dataset']['frequency']
        freq_days_act=freq2days(freq_act,0)
        freq_days=freq2days(freq,0)
        freq_int=min(260,int(365/max(freq_days,freq_days_act)))
        fig, ax = plt.subplots(figsize=(4,3),edgecolor='lightgray')
        plt.title('Trend & Seasonality Analysis')
        
        ax.grid(color='lightgray', alpha=0.7, linewidth=0.5)
        result=seasonal_decompose(series.values, model='additive', freq=freq_int)
        print(result.resid)
        print(result.seasonal)
        print(result.trend)
        result.plot()
        

        f = io.BytesIO()
        plt.savefig(f, format="png")
        encoded_img = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
        f.close()
        fig.clear() 
        return  JsonResponse({'imagedata':'<img src="data:image/png;base64,%s" />' % encoded_img},safe=False)
    