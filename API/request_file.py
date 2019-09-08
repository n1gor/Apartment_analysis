import requests
from sklearn.externals import joblib

model_columns = joblib.load('model_columns.pkl')

# print(model_columns)

# data = [{'square': 10, 'kitchen_scace': 5, 'curr_floor': 1, 'max_floor': 5, 'build_year': 1988, 'serv_lift': 0, 'pass_lift': 0, 'parking': 1, 'loggia': 0, 'balcony': 0, 'garbage_chute': 0, 'bathroom': 1, 'avg_price_for_m': 50000, 'avg_room_price': 1000000, 'home_type_Блочный': 0, 'home_type_Кирпичный': 0, 'home_type_Монолитно': 0, 'home_type_Монолитный': 1, 'home_type_Панельный': 0, 'district_Железнодорожный': 0, 'district_Кировский': 0, 'district_Ленинский': 0, 'district_Октябрьский': 0, 'district_Первомайский': 1, 'district_Пролетарский': 0, 'district_Советский': 0, 'repair_type_Без ремонта': 0, 'repair_type_Дизайнерский': 1, 'repair_type_Евроремонт': 0, 'repair_type_Косметический': 0, 'wind_view_Во двор': 1, 'wind_view_На улицу': 0, 'wind_view_На улицу и двор': 0}]
data = {}
for column in model_columns:
    print(column)
    data[column] = int(input())

predict = requests.post('http://127.0.0.1:12345/predict', json=[data]).json()
print(predict)
