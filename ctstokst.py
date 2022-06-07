# SPDX-FileCopyrightText: 2022 Kazuo Toda

import pandas as pd
import re
import datetime as dt
import sys
import streamlit as st

st.set_page_config(layout="wide")

"""
### CT stok input app
"""

#menu = ["input", "edit", "quit"]
#chois = st.sidebar.selectbox("Menu", menu)
#
#if chois == "input":
#    st.subheader("Data input")
#elif chois == "edit":
#    st.subheader("data Edit...under constraction!")
#elif chois == "quit":
#    st.subheader("goodbye")

def main():
    
    pmas = pd.read_csv('protector_master.csv', index_col='dia') 

    pio = pd.read_csv('protector_io.csv')
    pio["Stok awal"] = pio["Stok awal"].astype(int)
    pio["In"] = pio["In"].astype(int)
    pio["Out"] = pio["Out"].astype(int)
    pio["Stok Akhir"] = pio["Stok Akhir"].astype(int)
    #pio["datetime"] = pio["datetime"].astype(datetime)

    #extract master data
    col1, col2 = st.columns(2)
    with col1:
        #st.text("please input No. or TYPE ex 12 or THR :")
        st.write("please input No. or TYPE ex 12 or THR :")
    with col2:
        sno = st.text_input(' ',max_chars=11)
    #sno = input("please input No. or TYPE ex 12 or THR :")
    if re.search("[0-9]+", sno):
        dfc = pmas[pmas['NO'] == int(sno)]
        #st.dataframe(dfc,width=2000,height=100)
        st.write(dfc,width=2000,height=100)
    else:
        dfc = pmas[pmas['TYPE'].str.contains(sno)]
        st.dataframe(dfc,1500,200)
        #print(dfc)
    
    
    #ino = int(input("please input No: "))
    col3, col4 = st.columns(2)
    with col3:
        st.text('please input No: ')
    with col4:
        ino = st.number_input(' ',min_value=0, max_value=200)

    dfi = pio[pio['NO'] == int(ino)]
    lastakhir = dfi.iloc[-1]['Stok Akhir']
    st.dataframe(dfi.tail(1))
    
    #io = int(input('please input IN>1, Out>2: '))
    io = st.radio('In? or Out?',('In', 'Out'))
    
    col5, col6 = st.columns(2)
    with col5:
        st.text('please input qty: ')
    with col6:
        qty = st.number_input(' ',min_value=0, max_value=10000, value = 0)
    
    
    #qty = int(input("please input qty: "))
    now = dt.datetime.now()

    if io == 'In':
        adddata =[{'NO': ino, 'Stok awal': lastakhir, 'In': qty, 'Out' : 0, 'datetime': now.strftime('%Y%m%d_%H%M'), 'Stok Akhir': lastakhir+qty}]
    elif io == 'Out':
        adddata =[{'NO': ino, 'Stok awal': lastakhir, 'In' : 0, 'Out': qty, 'datetime': now.strftime('%Y%m%d_%H%M'),'Stok Akhir': lastakhir-qty}]

    pio = pio.append(adddata, ignore_index = False, sort=False)
    st.dataframe(pio.tail(1))
    
    button_state = st.button('to_CSV')
    if button_state:
        pio.to_csv("protector_io.csv", encoding='utf-8', index = False)
        st.dataframe(pio.tail(1))
    
    #button_state = st.button('exit')
    #if button_state:
    #    sys.exit()



if __name__ == '__main__':
    main()



