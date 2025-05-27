# from pyspark.sql import SparkSession
# import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import matplotlib.pyplot as plt
from jupyter_server.services.kernelspecs.handlers import kernel_name_regex
from streamlit import metric
import random
# import streamlit as st

# spark = SparkSession.builder.appName("carmax").master("local[*]").getOrCreate()

dict2 = {}

# st.set_page_config(
#         page_title="PySpark Carmax",
#         page_icon="✅",
#         layout="wide",
#     )
#
# st.title("Real Time Data")
# placeholder = st.empty()

# placeholder = st.empty()
prevs_ct = 0

def sl_metrics(ct,df,prevs_ct,fltr1,prceMlgeFltr,st,placeholder,model_yr_fltr):
    rand_num = random.random()
    with placeholder.container():
        kp1,kp2 = st.columns(2)
        kp1.metric(label="Total records", value=ct, delta=ct-prevs_ct)
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("## Model count")
            # df['model'] = df['name'].map(lambda x: x.split(' ')[0])
            df['model'] = df['name'].apply(lambda x: int(x.split(" ")[0])) #Changing to 'int' datatype

            #Applying model year filter the dataframe will change based on the filter
            df = df[(df['model'] >= model_yr_fltr[0]) & (df['model'] <= model_yr_fltr[1])]

            if len(list(df['name'])) == 0:
                st.markdown("No Results found")
            else:
                val_cts = df['model'].value_counts()
                x = sorted(list(map(str, list(val_cts.index))))
                y = list(map(int, val_cts.values))
                # fig = px.bar(data_frame=None, y=y, x=x,)
                # fig.update_layout(xaxis=dict(showticklabels=True))
                fig = px.bar(x=x, y=y,color=x)
                fig.update_layout(xaxis_type='category',
                                  xaxis_title="Year",
                                  yaxis_title="No. of Cars",
                                  yaxis = {
                                      "tickvals" : list(range(0,10000))
                                  }
                                  )
                st.write(fig)
                # def model_yr_func(fltrd_df):
                #     val_cts = fltrd_df['model'].value_counts()
                #     x = sorted(list(map(str,list(val_cts.index))))
                #     y = list(map(int,val_cts.values))
                #     # fig = px.bar(data_frame=None, y=y, x=x,)
                #     # fig.update_layout(xaxis=dict(showticklabels=True))
                #     fig = px.bar(x = x, y = y, color = x)
                #     fig.update_layout(xaxis_type='category')
                #     st.write(fig)
                st.markdown(f"### {fltr1} {prceMlgeFltr}")
                if fltr1 == 'Lowest':
                    df = df[df[prceMlgeFltr] == df[prceMlgeFltr].min()]
                    # print("Price ",df['price'])
                    # model_yr_func(df)
                    name = list(df['name'])
                    prceMlmin = list(df[prceMlgeFltr])
                    url = list(df['link'])
                    # for i in range(len(name)):
                    st.write(f"Name :  {name[-1]}  \n {prceMlgeFltr.capitalize()} : ${prceMlmin[-1]}")
                        # st.write("check out this [link](%s)" % df['link'][i])
                    st.markdown("[More Info](%s)" % url[-1])
                elif fltr1 == 'Highest':
                    df = df[df[prceMlgeFltr] == df[prceMlgeFltr].max()]
                    # model_yr_func(df)
                    name = list(df['name'])
                    prceMl = list(df[prceMlgeFltr])
                    url = list(df['link'])
                    # for i in range(len(name)):
                    st.write(f"Name : {name[-1]}  \n {prceMlgeFltr.capitalize()} : ${prceMl[-1]}")
                        # st.write(" Link to the page [link](%s)" % df['link'][i])
                    st.markdown("[More Info](%s)" % url[-1])

def visualized(dict2, fltr1, prceMlgeFltr, st, placeholder, model_yr_fltr):
    global prevs_ct
    df = pd.DataFrame.from_dict(dict2)

    # df = pd.DataFrame.from_dict(dict2)
    df['price'] = df['price'].fillna(0.0)
    # job_filter = st.selectbox("Select the Job", pd.unique(df['job']))

    # # plt.plot(df, linestyle = 'dotted')
    # st.set_page_config(
    #     page_title="PySpark Carmax",
    #     page_icon="✅",
    #     layout="wide",
    # )
    #
    # st.title("Real Time Data")

    # job_filter = st.selectbox("Select the column ", pd.unique(['Lowest','Highest']))
    # if fltr1 == 'Lowest':
    #     print(df['price'])
    #     print(df['price'].min())
    #     df = df[df['price'] == df['price'].min()]
    # elif fltr1 == 'highest':
    #     df = df[df['price'] == df['price'].max()]

    count = int(df['name'].count())

    print("count is ------> ", count)

    #Calling the function
    # time.sleep(3)
    sl_metrics(count,df,prevs_ct,fltr1,prceMlgeFltr,st,placeholder, model_yr_fltr)
    prevs_ct = count





def streaming(incoming_data,fltr1,prceMlgeFltr,st,placeholder,model_yr_fltr):
    for k, v in incoming_data.items():
        if k in dict2:
            dict2[k].append(v)
        else:
            dict2[k] = [v]
    # df.to_csv('carmax_stm_testing.csv',index=False)
    visualized(dict2,fltr1,prceMlgeFltr,st,placeholder,model_yr_fltr)


