import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

st.title("Система оптимізації служби роботи доставки закладів громадського харчування")
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 5)

data = pd.read_csv(r"E:\Dyplom_Dataset\orders.csv")
data32 = pd.read_csv(r"E:\DyplomDataset2\stores.csv", encoding='latin-1')
st_data = data32.copy()
st_data_new = st_data.drop(["hub_id"], axis = 1)
st_data_new = st_data_new.drop(["store_plan_price"], axis = 1)
#st_data_new = st_data_new.drop(["store_latitude"], axis = 1)
#st_data_new = st_data_new.drop(["store_longitude"], axis = 1)

data_new = data.copy()
data_new['Year'] = data_new.order_moment_created.apply(lambda x: x.split(' '))
data_new['order_date'] = data_new.Year.apply(lambda x: (x[0]))

data_new = data_new.drop(["order_id"], axis = 1)
data_new = data_new.drop(["channel_id"], axis = 1)
data_new = data_new.drop(["payment_order_id"], axis = 1)
data_new = data_new.drop(["delivery_order_id"], axis = 1)
data_new = data_new.drop(["order_status"], axis = 1)
data_new = data_new.drop(["order_delivery_fee"], axis = 1)
data_new = data_new.drop(["order_delivery_cost"], axis = 1)
data_new = data_new.drop(["order_created_minute"], axis = 1)
data_new = data_new.drop(["order_moment_accepted"], axis = 1)
data_new = data_new.drop(["order_moment_ready"], axis = 1)
data_new = data_new.drop(["order_moment_collected"], axis = 1)
data_new = data_new.drop(["order_moment_in_expedition"], axis = 1)
data_new = data_new.drop(["order_moment_delivering"], axis = 1)
data_new = data_new.drop(["order_moment_delivered"], axis = 1)
data_new = data_new.drop(["order_moment_finished"], axis = 1)
data_new = data_new.drop(["order_metric_collected_time"], axis = 1)
data_new = data_new.drop(["order_metric_paused_time"], axis = 1)
data_new = data_new.drop(["order_metric_production_time"], axis = 1)
data_new = data_new.drop(["order_metric_walking_time"], axis = 1)
data_new = data_new.drop(["order_metric_transit_time"], axis = 1)
data_new = data_new.drop(["order_metric_cycle_time"], axis = 1)
data_new = data_new.drop(["order_metric_expediton_speed_time"], axis = 1)
data_new = data_new.drop(["order_moment_created"], axis = 1)
data_new = data_new.drop(["Year"], axis = 1)
#print(data_new)
#print(data_new.columns)

#print ("Тип данных ID " + str(type(data_new.store_id[0])))
#print ("Тип данных Amount " + str(type(data_new.order_amount[0])))
#print ("Тип данных Hour " + str(type(data_new.order_created_hour[0])))
#print ("Тип данных Day " + str(type(data_new.order_created_day[0])))
#print ("Тип данных Mounth " + str(type(data_new.order_created_month[0])))
#print ("Тип данных Year " + str(type(data_new.order_created_year[0])))
#print ("Тип данных Date " + str(type(data_new.order_date[0])))

finaldata_set = data_new.merge(st_data_new, left_on='store_id', right_on='store_id', suffixes=('_left', '_right'))
data_final = finaldata_set[finaldata_set.store_segment == "FOOD"]
data_final = data_final.drop(["store_segment"], axis = 1)
data_final['Names'] = data_final.apply(lambda x: str(x['store_name']) + ' ' + str(x['store_id']),1)
st.subheader("Датасет")
st.write(data.tail())
st.write(st_data.tail())
st.subheader("Датасет після обробки")
st.write(data_final.tail())


def quantity_orders_all():
    table1 = data_final.groupby('order_created_hour').store_id.count()
    st.bar_chart(table1)


st.subheader("Кількість замовлень протягом доби")
quantity_orders_all()


def top_of_companies(x):
    table = data_final.groupby('Names').Names.count()
    table = table.sort_values(inplace=False, ascending=False)
    print(table)
    table.head(x).plot(kind='bar')
    st.pyplot(plt)


st.subheader("Заклади громадського харчування з найбільшою кількістю замовлень")

restaurant_quantity = st.radio("Оберіть кількість закладів", ("Топ 5", "Топ 10", "Топ 30"))
if restaurant_quantity == "Топ 5":
    top_of_companies(5)
elif restaurant_quantity == "Топ 10":
    top_of_companies(10)
elif restaurant_quantity == "Топ 30":
    top_of_companies(30)

stoks = (pd.unique(data_final.Names)).tolist()

st.subheader("Оберіть заклад громадського харчування")
selected_stocks = st.selectbox(" ", stoks)

st.subheader("Кількість замовлень закладу протягом доби")
datetim = data_final[data_final.Names == selected_stocks]

map_cr_lat = datetim.iloc[0,8]
map_cr_long = datetim.iloc[0,9]
map_data = pd.DataFrame({'lat': [map_cr_lat], 'lon': [map_cr_long]})

st.map(map_data)


table2 = datetim.groupby('order_created_hour').store_id.count()
delifr1 = datetim[datetim['order_created_hour'].isin([8, 9, 10, 11, 12])]
delifr2 = datetim[datetim['order_created_hour'].isin([13, 14, 15, 16, 17, 18])]
delifr3 = datetim[datetim['order_created_hour'].isin([19, 20, 21, 22, 23])]
delifr4 = datetim[datetim['order_created_hour'].isin([0, 1, 2, 3, 4, 5, 6, 7])]


st.bar_chart(table2)


st.subheader("Динаміка замовлень закладу")
table3 = datetim.groupby('order_date').store_id.count()
#print(table3)

st.line_chart(table3)



#res = table3.to_frame()
res = datetim.groupby('order_date').store_id.count().reset_index(name = "num_orders")
st.write(res.tail())
res.order_date = pd.to_datetime(res.order_date).dt.strftime("%Y-%m-%d")
#st.write(res)
#print(res.info())

period = 97 + 30

#Forecast

df_train = res[['order_date', 'num_orders']]
df_train = df_train.rename(columns ={"order_date": "ds", "num_orders": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

datefoepred = st.date_input("Оберіть дату, аби дізнатись кількість кур'єрів")

finalldate = datefoepred.strftime("%Y-%m-%d")
fdate = finalldate + "T00:00:00"

st.write(fdate)

final_set = forecast[forecast.ds == fdate]

st.write(final_set.tail())

res2 = final_set.iloc[0,15]

st.write(res2)

er_t = len(delifr1)
day_t = len(delifr2)
ev_t = len(delifr3)
night_t = len(delifr4)

all_day = er_t + day_t + ev_t + night_t

er = er_t/all_day
day = day_t/all_day
ev = ev_t/all_day
night = night_t/all_day

st.write(er)
st.write(day)
st.write(ev)
st.write(night)

quntity_for_er = res2*er
quntity_for_day = res2*day
quntity_for_ev = res2*ev
quntity_for_night = res2*night

def quntity_of_coruers(tem):
    if tem <= 5:
        return 1
    elif tem > 5 and tem<=10:
        return 2
    elif tem > 10 and tem <=20:
        return 3
    elif tem >20 and tem <= 30:
        return 4
    elif tem > 30 and tem <=45:
        return 5
    elif tem > 45 and tem <=65:
        return 6
    elif tem > 65 and tem <= 90:
        return 7
    elif tem >90 and tem <= 120:
        return 9
    else:
        tem > 120
        return 10

st.subheader("Кількість кур'єрів, яка необхідна для швидкої та якісної доставки замовлень закладу " + str(selected_stocks))
st.write(quntity_of_coruers(quntity_for_er))
st.subheader("Ранок 8:00 - 12:00: " + str(quntity_of_coruers(quntity_for_er)))
st.subheader("День 12:00 - 18:00: " + str(quntity_of_coruers(quntity_for_day)))
st.subheader("Вечір 18:00 - 00:00: " + str (quntity_of_coruers(quntity_for_ev)))
st.subheader("Ніч 00:00 - 8:00: " + str(quntity_of_coruers(quntity_for_night)))
