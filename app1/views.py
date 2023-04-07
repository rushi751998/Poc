from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form
from .models import Video2
import datetime
import pandas as pd
import json
import time
import matplotlib.pyplot as plt

# def index(request):
#     all_video=Video.objects.all()
#     if request.method == "POST":
#         form=Video_form(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request,'index.html')
#     else:
#         form=Video_form()
#         return render(request,'index.html',{"form":form})



def index(request):
    return render(request, 'index.html')


def videos(request):
    # time.sleep(2) 
    if request.method == "POST":
        dates = Video2.objects.values_list('caption',flat=True)
        global date
        
        try:
            date = request.POST.get('date')
            
        
            date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
            
            if date_time_obj.date() in dates:
                global filterd_videos
                filterd_videos = Video2.objects.filter(caption=date)
                return render(request, 'videos1.html', {"all": filterd_videos, "date": date})
            
            else:
                return render(request, 'error.html')
            
        except :
            return render(request, 'select_date.html')
            
        
    return render(request,'index.html')
    # return render(request, 'videos1.html', {"all": all_video})
    


def videos2(request):
    # time.sleep(20)
    return render(request, 'videos2.html', {"all": filterd_videos, "date": date})


def get_param(data):
    data.columns = data.columns.str.replace(" ","_")
    
    
    gender_values = data.groupby('Gender').count()['Age']
    # print(gender_values)

    activity = data.groupby('Suspecious').count()['Customer_ID']
    age=data.groupby('Age').mean()['Spend_Time']
    
    race  = data.groupby('Race').count()['Customer_ID']
    emotion = data.groupby('Emotion').count()['Customer_ID']
    print(age)


    # it will geive data frame to html
    json_records = data.reset_index().to_json(orient='records')
    data_html = json.loads(json_records)
    col_name = data.columns



    param = {'col_name': col_name,
    "data_html": data_html,
    "emotions_lables": (emotion.index), 'emotions_values': (emotion.values),
    'gender': gender_values.index, 'gender_values': gender_values.values,
    'activity_lable': (activity.index), 'activity_values': (activity.values), 
    'age_id_index' : (age.index),'age_id_values' : (age.values),
    'race_id_index' :(race.index),  'race_id_values':(race.values)}
    
    return param

def dashboard(request):
    data = '2023-03-01'
    if date == "2023-03-01":
        data = pd.read_csv('data/processed1.csv')
    
    elif date == "2023-03-02":
        data = pd.read_csv('data/processed3.csv')
        
    elif date == "2023-03-03":
        data = pd.read_csv('data/processed4.csv')
    
    elif date == "2023-03-04":
        data = pd.read_csv('data/processed5.csv')
        
    else:
        return render(request,'index.html')
        
        
    return render(request, 'dashboard_filter.html', get_param(data))



def get_data_kpi():
    data = pd.read_csv('data/combine.csv',date_parser='date')
    data.columns = data.columns.str.replace(" ","_")
    
    return data

def kpi_dashboard(request):

    # time.sleep(3)     
    return render(request, 'kpi_dashboard/kpi_dashboard.html')

def operation(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        customer_service =get_data_kpi()[['date', 'Customer_ID','transaction_in_system','Spend_Time','footfall_not_captured','transactions_Volume']]
        footfalls = customer_service.groupby('date').count()[ 'Customer_ID']
        uncap_foot = customer_service[ 'footfall_not_captured'].unique()
        transactions = customer_service[ 'transaction_in_system'].unique()
        transactions_Volume = customer_service[ 'transactions_Volume'].unique()
        avg_stay = customer_service[ 'Spend_Time'].mean()
        avg_stay_bydate= customer_service.groupby('date').mean()['Spend_Time']
        # print(avg_stay_bydate.values)

        audio_df =pd.read_csv('data/audio.csv')
        tags = audio_df.groupby('categeory').count()['tags']

        
        parms = {
            'kpi':'Operational',
            "foot_fall":footfalls.values,
            'date':footfalls.index,
            'n_transactions':transactions,
            'avg_stay':round(avg_stay),
            'uncap_foot':uncap_foot,
            'transactions_Volume':transactions_Volume,
            'avg_stay_bydate':avg_stay_bydate.values,
            'tags_lable':tags.index,
            'tags_value':tags.values,
            }
        return render(request, 'kpi_dashboard/operation.html',parms)
    return render(request, 'kpi_dashboard/error.html')
    
    

def customer_service(request):
    if request.method == "POST":
        
        global time
        time = request.POST.get('time')
        customer_service = get_data_kpi()[['date','Gender','Emotion', 'Age', 'Race','Customer_ID']]
        gender = customer_service.groupby('Gender').count()['date']
        happy_customers = customer_service.groupby('Customer_ID').first()[['Emotion','Gender']]
        emotions = happy_customers.groupby('Emotion').count()


        emotiondf =customer_service.groupby(['date','Emotion']).count().unstack(fill_value=0).stack()[['Customer_ID']]
        emotiondf=emotiondf.reset_index()
        angry=(emotiondf[emotiondf['Emotion']=='angry']['Customer_ID'])
        fear=(emotiondf[emotiondf['Emotion']=='fear']['Customer_ID'])
        happy=(emotiondf[emotiondf['Emotion']=='happy']['Customer_ID'])
        neutral=(emotiondf[emotiondf['Emotion']=='neutral']['Customer_ID'])
        sad=(emotiondf[emotiondf['Emotion']=='sad']['Customer_ID'])
        surprise=(emotiondf[emotiondf['Emotion']=='surprise']['Customer_ID'])
        # print(surprise)
        

        
        foregin_customer= customer_service[customer_service['Race']!='indian'][['date','Customer_ID','Race']]
        foregin_customer = customer_service.groupby('Customer_ID').first()[['Race']]
        foregin_customer = customer_service.groupby('Race').first()[['Customer_ID']]
        foregin_customer= foregin_customer[foregin_customer['Customer_ID']>0]
        
        parms = {
        'kpi':'customer Service', 
        'gender_lable':gender.index,
        'gender_values':gender.values,
        'emotion_lable':emotiondf.date.unique(),
        'angry':angry,
        'fear':fear,
        'happy':happy,
        'neutral':neutral,
        'sad':sad,
        'surprise':surprise,
        'foreign_lable':foregin_customer.index,
        'foreign_values':foregin_customer.values,       
        }
        return render(request, 'kpi_dashboard/customer_service.html',parms)
    return render(request, 'kpi_dashboard/error.html')

    

def primer_customer(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        df = get_data_kpi()[['date','No_cutomers', 'transaction_in_system','account_balance','Emotion','Spend_Time']]
  
        primer_customers =df[df['account_balance']>1000000]
        transaction_by_all = df.groupby('date').sum()['transaction_in_system']
        transaction_by_primer = primer_customers.groupby('date').sum()['transaction_in_system']
        avg_stay = primer_customers[ 'Spend_Time'].mean()
        date = df['date'].unique()
        total_customer = df.groupby('date').count()['No_cutomers']
        total_primer = primer_customers.groupby('date').count()['No_cutomers']
        total_primum_count = primer_customers['Emotion'].count()
        happpy_primum_count = primer_customers[primer_customers['Emotion']=='happy'].count()['date']
        per_happy_primum = (happpy_primum_count*100)/total_primum_count
        # print(primer_customers['Emotion'].unique())
        # print(per_happy_primum)
        parms = { 
            'kpi': 'Primer Customers',
            'date':date,
            'total_primer':total_primer.values,
            'total_customer':total_customer.values,
            'transaction_by_all':transaction_by_all.values,
            'transaction_by_primer':transaction_by_primer.values,
            'avg_stay':round(avg_stay),
            'per_happy_primum':round(per_happy_primum,2)
            }
        return render(request, 'kpi_dashboard/primer_customer.html',parms)
    return render(request, 'kpi_dashboard/error.html')
    

    

def security(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        security = get_data_kpi()[['date','Suspecious','No_cutomers','frequent_visit', 'transaction_in_system',
       'transactions_Volume']]
        
        suspicious_footfall = security.groupby('date').sum()['Suspecious']
        frequent_visit = security['frequent_visit'].unique()
        transaction_in_system = security['transaction_in_system'].unique()
        transactions_Volume = security['transactions_Volume'].unique()
        No_cutomers = security['No_cutomers'].unique()
        date = security['date'].unique()
        
   
        

        
        parms = {
        'date':date,
        'date_suspecious':suspicious_footfall.index,'kpi':'Security & Safety',
        'suspicious_footfall':suspicious_footfall.values,
        'frequent_visit':frequent_visit,
        'transaction_in_system':transaction_in_system,
        'transactions_Volume':transactions_Volume,
        'No_cutomers':No_cutomers
        }
        return render(request, 'kpi_dashboard/security.html',parms)
    return render(request, 'kpi_dashboard/error.html')

    