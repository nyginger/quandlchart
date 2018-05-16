from django.shortcuts import render
from django.http import JsonResponse
import csv
from .models import API_keys, Items_table, Indicators,Countries
#from .forms import ItemForm


def importquandl(request):

    create_list=[]
    dataset=request.GET['dataset'].upper()
    with open('quandl_chart/dataset/{}-datasets-codes.csv'.format(dataset),'r') as file:
        result=csv.reader(file, delimiter=',')
        print(result)
        for row in result:

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
