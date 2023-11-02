import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.title ("Sipariş Kaydetme Ekranı")
st.markdown("Detay girin")

connect = st.connection("gsheets",type=GSheetsConnection)
veriler_data = connect.read(worksheet="Sayfa1", usecols=list(range(23)),ttl=5)
veriler_data = veriler_data.dropna(how="all") 
st.dataframe(veriler_data)

with st.form(key="siparis_form"):
    bilgiler = st.text_area(label="ADRESLER*")
    st.markdown("**Zorunlu*")
    dugme= st.form_submit_button(label="Siparişi Kaydet")
    
    BUSINESS_TYPES = [
    "ARAS KARGO",
    "PTT",]

    dugme2 = st.selectbox("ARAS KARGO",options=BUSINESS_TYPES, index=None)
    
    sayfa_ismi =""
    sube_kodu =""
    if dugme2 == "ARAS KARGO":
        sayfa_ismi = "Sayfa1"
        sube_kodu ="205"
    else:
        sayfa_ismi= "example"
        sube_kodu ="155"      
    lines = bilgiler.split('\n')
    if len(lines) >= 6:
                isim_soyisim = lines[0]
                adres_bilgisi = lines[1]
                ilce = lines[2]
                il = lines[3]
                telefon = lines[4]
                ucret = lines[5]
                urun_bilgisi = '\n'.join(lines[7:])

                 
                



    if dugme:
        if not bilgiler:
            st.write("bilgiler Eksik")
            st.stop()



        else:
            veri_Giris = pd.DataFrame(
                [
                    { 
                          
                        "İSİM SOYİSİM" : isim_soyisim,
                        "İLÇE"  : ilce,
                        "İL": il,
                        "ADRES":adres_bilgisi,
                        "TELEFON": telefon,
                        "ŞUBE KOD" :sube_kodu,
                        "MÜŞTERİ NO" :"",
                        "TUTAR": ucret,
                        "ÜRÜN": urun_bilgisi,
                        "MİKTAR":"1",
                        "GRAM ":"800",
                        "GTÜRÜ":"2",
                        "ÜCRETTÜRÜ":"6",
                        "EK HİZMET":" ",
                        "KDV":"8",
                        "SİP NO":" 123",
                        "ÇIKIŞ NO":"",
                        "SATICI":"",
                        "HATTAR":"",
                        "FATTAR":"",
                        "EN" : "10",
                        "BOY" : "15",
                        "YÜKSEKLİK" : "10",
                            
                    }
                ]
            )
            


            updated_df = pd.concat([veriler_data, veri_Giris], ignore_index=True)
            connect.update(worksheet=sayfa_ismi, data=updated_df)

            st.success("Sipariş Kaydedildi")






