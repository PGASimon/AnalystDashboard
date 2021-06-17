#Dashboard
import pandas as pd
import numpy as np
import streamlit as st
import pickle 
import altair as alt
import pandas_ta as pta

with open('Alldata','rb') as Alldata:
    Alldata=pickle.load(Alldata)
AllSymbolList=['Overall Market'] + list(Alldata['Symbol'].unique())

st.set_page_config(page_title='Analyst DashBoard',layout='wide')

st.title('Analyst Dashboard (Gang Gang Gang)')
TechnicalOptions=st.sidebar.selectbox('Technical Analysis:Select Security',AllSymbolList)
if TechnicalOptions=='Overall Market':
    st.write('Latest Market Sheet')
    st.dataframe(Alldata.xs('2021-06-09'))

else:

    #technical indicators for particular stock
    st.write('Technical Analysis for %s ' %TechnicalOptions)
    k=pd.DataFrame(Alldata[Alldata['Symbol']==TechnicalOptions]) #dataset split for particular stock 
    k=k.reset_index()

    #EMA and price plots 
    y=alt.Chart(k).mark_line().encode(x='Date:T',y='Close Price').interactive()
    y1=alt.Chart(k).mark_line(color='blue').encode(x='Date:T',y='EMA(26)')
    y2=alt.Chart(k).mark_line(color='purple').encode(x='Date:T',y='EMA(12)')
    y= alt.layer(y,y1,y2)
    st.altair_chart(y,use_container_width=True)

    #MFI and RSI
    techcol1, techcol2= st.beta_columns(2)
    with techcol1:
        st.header('MFI:')
        k['MFI']=pta.mfi(k['Today High'],k['Today Low'],k['Close Price'],k['Volume (non block)'],lenght=28)
        MFI=alt.Chart(k).mark_line().encode(x='Date:T',y='MFI').interactive()
        MFIrule1=alt.Chart(pd.DataFrame({'MFI':[80]})).mark_rule(color='red').encode(y='MFI')
        MFIrule2=alt.Chart(pd.DataFrame({'MFI':[20]})).mark_rule(color='red').encode(y='MFI')
        MFItotal=alt.layer(MFI,MFIrule1,MFIrule2)
        st.altair_chart(MFItotal,use_container_width=True)

        st.header('RSI:')
        k['RSI']=pta.rsi(k['Close Price'],length=28)
        RSI=alt.Chart(k).mark_line().encode(x='Date:T',y='RSI').interactive()
        RSIrule1=alt.Chart(pd.DataFrame({'RSI':[80]})).mark_rule(color='red').encode(y='RSI')
        RSIrule2=alt.Chart(pd.DataFrame({'RSI':[20]})).mark_rule(color='red').encode(y='RSI')
        RSItotal=alt.layer(RSI,RSIrule1,RSIrule2)
        st.altair_chart(RSItotal,use_container_width=True)       

    with techcol2:
        st.header('100 and 30 MA ')
        MA=alt.Chart(k).mark_line().encode(x='Date:T',y='Close Price').interactive()
        MA100=alt.Chart(k).mark_line(color='red').encode(x='Date:T',y='MA(100):Q')
        MA30=alt.Chart(k).mark_line(color='blue').encode(x='Date:T',y='MA(30):Q')
        MATotal=alt.layer(MA,MA100,MA30)
        st.altair_chart(MATotal,use_container_width=True)

      
        Bands=pta.bbands(k['Close Price'],lenght=40)
        Bands.index
        
        BBand=alt.Chart(k).mark_line().encode(x='Date:T',y='Close Price').interactive()
        BBandU=alt.Chart(Bands).mark_line(color='blue').encode(x='Date:T',y='BBU_5_2.0')
        BBandL=alt.Chart(Bands).mark_line(color='red').encode(x='Date:T',y='BBL_5_2.0')
        BBandM=alt.Chart(Bands).mark_line(color='red').encode(x='Date:T',y='BBM_5_2.0')
        BBandTotal=alt.layer(BBand,BBandM,BBandL,BBandU)
        st.altair_chart(BBandTotal,use_container_width=True)

        
    


    
    




hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 