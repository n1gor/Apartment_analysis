from django.shortcuts import render
import requests
from sklearn.externals import joblib
from .forms import PredictForm
from sklearn.externals import joblib

df = joblib.load('df.pkl')

def home(request):
    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            model_columns = joblib.load('predict/model_columns.pkl')
            data = {}
            for column in model_columns:
                data[column] = 0
            f = form.cleaned_data
            print(f)
            districts = ['Железнодорожный',
                         'Кировский',
                         'Ленинский',
                         'Октябрьский',
                         'Первомайский',
                         'Пролетарский',
                         'Советский']
            for key in f.keys():
                print(f[key])
                print(data.get(key))
                if key == 'district':
                    data['district_' + f[key]] = 1
                elif key == 'repair_type':
                    data['repair_type_' + f[key]] = 1
                elif key == 'home_type':
                    data['home_type_' + f[key]] = 1
                elif isinstance(f[key], bool):
                    data[key] = int(f[key])
                else:
                    data[key] = f[key]
            print(data)
            predict_price = int(requests.post('http://127.0.0.1:12345/predict', json=[data]).json()['prediction'][0])
            df_tmp = df[df['rooms'] == f['rooms']]
            df_tmp = df_tmp[abs(df_tmp['square'] - f['square']) <= 10]
            df_tmp = df_tmp[abs(df_tmp['price'] - predict_price) <= 300000]
            df_tmp = df_tmp[df_tmp['district'] == f['district']]
            print(df_tmp)
            predict = ''
            try:
                predict = df_tmp.iloc[0].to_dict().items()
                # for key, value in df_tmp.iloc[0].to_dict().items():

            except:
                predict = 'Try to choose another districts'

    else:
        predict = ''
    return render(request, 'predict/home.html', {'title': 'It works!', 'form': PredictForm(), 'predict': predict})
