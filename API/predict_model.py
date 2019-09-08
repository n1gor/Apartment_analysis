import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from statsmodels.formula.api import ols
from sklearn.externals import joblib
import matplotlib.pyplot as plt
#('scaler', StandardScaler())

# steps = [('imputation', SimpleImputer(missing_values=np.nan, strategy="median")),
#         ('scaler', StandardScaler()),
#         ('ridge', Ridge())]
#
# pipeline = Pipeline(steps)

df = pd.read_csv('apartments_cian.csv')
df = df * ([1] * 21 + [10])
df = df.fillna(0)
df = df.drop('living_space', 1)
df = df.drop('rooms', 1)
df = df.drop('emergency_exit', 1)
m = ols('price ~ square',df).fit()
infl = m.get_influence()
sm_fr = infl.summary_frame()
a = sm_fr['dffits']<0.2841371938943025
a = a.reindex(range(1090))
a = a.fillna(True)
df = df.iloc[:-115]
df = df[a]
#df = df.drop('avg_price_for_m', 1)
#df = df.drop('avg_room_price', 1)

#df = df.drop('street', 1)
#df = df.dropna()
df_dm = pd.get_dummies(df, drop_first=True)
# df_dm = df_dm[df_dm['rooms'] != 4]
# df_dm = df_dm[df_dm['rooms'] != 0]
#df_dm = df_dm[df_dm['price, RUB']<750000]

x = df_dm.drop('price', 1)
x_imp = SimpleImputer(missing_values=np.nan, strategy="median").fit_transform(x)
#x_scaled = StandardScaler().fit_transform(x_imp)
# x = x.drop('avg_price_for_m', 1)
# x = x.drop('avg_room_price', 1)
y = df_dm['price']

x_train, x_test, y_train, y_test = train_test_split(x_imp, y, test_size=0.45, random_state=24)
#{'linearreggression__alpha': np.logspace(-5,8,15)}
# {'max_depth': range(9,10)
print(type(x_test))
tree = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=17)
gm_cv = GridSearchCV(tree, {'max_depth': range(9,15)}, cv = 5)
gm_cv.fit(x_train, y_train)
r21 = gm_cv.score(x_train, y_train)
r2 = gm_cv.score(x_test, y_test)
# model = RandomForestRegressor()
# model.fit(x_train, y_train)

# data = {'square': 35, 'kitchen_scace': 10, 'curr_floor': 7, 'max_floor': 20, 'build_year': 2007, 'serv_lift': 1, 'pass_lift': 1, 'parking': 1, 'loggia': 1, 'balcony': 0, 'garbage_chute': 0, 'bathroom': 1, 'avg_price_for_m': 75714, 'avg_room_price': 2000000, 'home_type_Блочный': 0, 'home_type_Кирпичный': 0, 'home_type_Монолитно': 0, 'home_type_Монолитный': 0, 'home_type_Панельный': 1, 'district_Железнодорожный': 0, 'district_Кировский': 0, 'district_Ленинский': 0, 'district_Октябрьский': 0, 'district_Первомайский': 0, 'district_Пролетарский': 0, 'district_Советский': 1, 'repair_type_Без ремонта': 0, 'repair_type_Дизайнерский': 1, 'repair_type_Евроремонт': 0, 'repair_type_Косметический': 1, 'wind_view_Во двор': 1, 'wind_view_На улицу': 0, 'wind_view_На улицу и двор': 0}
# count = 0
#
# print(gm_cv.predict(pd.DataFrame(data, index = [0], columns=x.columns)))


for i in range(10):
    # print(x_test[i].reshape(1, -1) )

    a = int(gm_cv.predict(x_test[i].reshape(1, -1))[0])
    # a = int(model.predict(x_train.iloc[[i]])[0])
    b = int(y_test.iloc[i])
    # if abs(int(a-b)) < 300000:
    #     # count += abs(int(a-b))
    #     count += 1
    print('predict: ', a)
    print('real:    ', b)
    print('dif: ', abs(a-b))
    print('--------------------')

print("Tuned params: {}".format(gm_cv.best_params_))
print("Train squared: {}".format(r21))
print("Tuned squared: {}".format(r2))
# print(len(x_test))
# print(count)
# rf_predict = gm_cv.predict(x_test)
#
# plt.figure(figsize=(10, 6))
# # plt.plot(x_test, f(x_test), "b")
# plt.scatter(x_train, y_train, c="b", s=20)
# plt.plot(x_test, rf_predict, "r", lw=2)
# plt.xlim([-5, 5])
# plt.title("Случайный лес, MSE = %.2f" % np.sum((y_test - rf_predict) ** 2));
# plt.show()
# joblib.dump(gm_cv, 'model.pkl')
# print('----------Model dumped----------')
#
# model = joblib.load('model.pkl')
#
# model_columns = list(x.columns)
# joblib.dump(model_columns, 'model_columns.pkl')
# print('----------Model columns dumped----------')

# Tuned Ridge Alpha: {'ridge__alpha': 31.622776601683793}
# Train Ridge R squared: 0.6084272273328867
# Tuned Ridge R squared: 0.6382523606287185
