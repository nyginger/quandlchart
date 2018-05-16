from django.shortcuts import render
from django.http import JsonResponse
import csv
from .models import API_keys, Items_table, Indicators,Countries
#from .forms import ItemForm

'''to use mongodb
from pymongo import MongoClient
MONGO_HOST= 'mongodb://127.0.0.1:27017' 
client = MongoClient(MONGO_HOST)
db = client.local'''

def importquandl(request):
    '''if request.method=='POST':
        form=  ItemForm(request.POST)
        form.save()
        
    key=API_keys.object.all()

    url=''
    result=requests.get(url).json()
    print(r.text)
    item1=result['item']

    items={
        'item1': result['item1'],
        'item2': result['item2']
    }
    context={'items':items}
    return render(request, 'quandl_chart/index.html', context)'''
    create_list=[]
    dataset=request.GET['dataset'].upper()
    with open('quandl_chart/dataset/{}-datasets-codes.csv'.format(dataset),'r') as file:
        result=csv.reader(file, delimiter=',')
        print(result)
        for row in result:
            '''' to use mongodb
            dt_dict={}
            dt_dict['name']=row[0]
            dt_dict['dataset']=row[1]
            dt_dict['symbol']=row[2]
            dt_dict['description']=row[3]

            create_list.append(dt_dict)
            
        db.quandl.insert_many(create_list) '''
            if len(row)>=7:
                item=Items_table(name=row[0],dataset=row[1], symbol=row[2], description=row[3], category=row[4], subcategory=row[5], country=row[6],ccode=row[7])
            elif len(row)>=5:
                item=Items_table(name=row[0],dataset=row[1], symbol=row[2], description=row[3], category=row[4])
            else:
                item=Items_table(name=row[0],dataset=row[1], symbol=row[2], description=row[3])
            create_list.append(item)
        Items_table.objects.bulk_create(create_list)

    return JsonResponse({'result':'finished'})



def importindicator(request):

    create_list=[]
    with open('quandl_chart/dataset/IMF_indicator.csv','r') as file:
        result=csv.reader(file, delimiter=',')
        print(result)
        for row in result:
            item=Indicators(dataset=row[0],code=row[1], name=row[2])
            create_list.append(item)
        Indicators.objects.bulk_create(create_list)

    return JsonResponse({'result':'finished'})



def importcountries(request):

    create_list=[]
    with open('quandl_chart/dataset/ISO_country_ccodes.txt','r') as file:
        result=csv.reader(file, delimiter='|')
        print(result)
        for row in result:
            item=Countries(dataset='ODA',code=row[0], name=row[1])
            create_list.append(item)
        Countries.objects.bulk_create(create_list)

    return JsonResponse({'result':'finished'})



def removeobj(request):
    dataset=request.GET['dataset'].upper()
    items=Items_table.objects.filter(dataset=dataset)
    items.delete()
    return JsonResponse({'result':dataset+' is removed'})