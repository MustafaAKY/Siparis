import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.title ("Sipariş Kaydetme Ekranı")
ADRES_BİLGİSİ = [
    "isim_soyisim",
]

st.markdown("Detay girin")

connect = st.connection("gsheets",type=GSheetsConnection)
veriler_data = connect.read(worksheet="aras_kargo", usecols=list(range(23)),ttl=5)
veriler_data = veriler_data.dropna(how="all") 
#st.dataframe(veriler_data)

veriler_data2 = connect.read(worksheet="ptt_kargo", usecols=list(range(23)),ttl=5)
veriler_data2 = veriler_data2.dropna(how="all") 
#st.dataframe(veriler_data2)
action = st.selectbox(
    "Seçenekler",
    [
        "Yeni Sipariş",
        "Sipariş Güncelle",
        "Siparişleri Göster",
        "Sipariş Sil",
    ],
)

if action == "Yeni Sipariş":
    with st.form(key="siparis_form"):
        bilgiler = st.text_area(label="ADRESLER*")
        st.markdown("**Zorunlu*")
        dugme= st.form_submit_button(label="Siparişi Kaydet")
        
        BUSINESS_TYPES = [
        "ARAS KARGO",
        "PTT",]

        dugme2 = st.selectbox("Hangi Kargo",options=BUSINESS_TYPES, index=None)
        
        
        sube_kodu =""
        if dugme2 == "ARAS KARGO":
            
            sube_kodu ="205"
        else:
            
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
                            "İSİM SOYİSİM": isim_soyisim,
                            "İLÇE": ilce,
                            "İL": il,
                            "ADRES": adres_bilgisi,
                            "TELEFON": telefon,
                            "ŞUBE KOD": sube_kodu,
                            "MÜŞTERİ NO": "",
                            "TUTAR": ucret,
                            "ÜRÜN": urun_bilgisi,
                            "MİKTAR": "1",
                            "GRAM": "800",
                            "GTÜRÜ": "2",
                            "ÜCRETTÜRÜ": "6",
                            "EK HİZMET": " ",
                            "KDV": "8",
                            "SİP NO": "",
                            "ÇIKIŞ NO": "",
                            "SATICI": "",
                            "HATTAR": "",
                            "FATTAR": "",
                            "EN": "10",
                            "BOY": "15",
                            "YÜKSEKLİK": "10",
                        }
                    ]
                )

                if dugme2 == "ARAS KARGO":
                    updated_df = pd.concat([veriler_data, veri_Giris], ignore_index=True)
                    connect.update(worksheet="aras_kargo", data=updated_df)
                else:
                    updated_df1 = pd.concat([veriler_data2, veri_Giris], ignore_index=True)
                    connect.update(worksheet="ptt_kargo", data=updated_df1)

                st.success("Sipariş Kaydedildi")

elif action == "Sipariş Güncelle":
    st.markdown("Select a vendor and update their details.")

    vendor_to_update = st.selectbox(
     "Güncelleme", options=veriler_data["İSİM SOYİSİM"].tolist()    
    )
        
                
    veri_Giris = veriler_data[veriler_data["İSİM SOYİSİM"] == vendor_to_update].iloc[
        0
    ]
    with st.form(key="update_form"):
            bilgiler = st.text_input(
            
            label="isimler*", value=veri_Giris["İSİM SOYİSİM"]
            )
            ilce = st.text_input(
            
            label="ilçe*", value=veri_Giris["İLÇE"]
            )
            il = st.text_input(
            
            label="İL*", value=veri_Giris["İL"]
            )
            ADRES = st.text_input(
            
            label="ADRES*", value=veri_Giris["ADRES"]
            )

            TELEFON = st.text_input(
            
            label="TELEFON*", value=veri_Giris["TELEFON"]
            )

            TUTAR = st.text_input(
            
            label="TUTAR*", value=veri_Giris["TUTAR"]
            )

            ÜRÜN = st.text_input(
            
            label="ÜRÜN*", value=veri_Giris["ÜRÜN"]
            )





            update_button = st.form_submit_button(label="Siparişi güncelle")        
    if update_button:
     if not bilgiler:
                st.write("bilgiler Eksik")
                st.stop()
     else:
          veriler_data.drop(
                veriler_data[
                veriler_data["İSİM SOYİSİM"] == vendor_to_update
                ].index,
                inplace=True,
          )
          updated_vendor_data = pd.DataFrame(
                    [
                        {
                            "İSİM SOYİSİM": bilgiler,
                            "İLÇE": ilce,
                            "İL" :il,
                            "ADRES":ADRES,
                            "TELEFON":TELEFON,
                            "ŞUBE KOD": "205",
                            "MÜŞTERİ NO":"",
                            "TUTAR":TUTAR,
                            "ÜRÜN":ÜRÜN,
                            "MİKTAR": "1",
                            "GRAM": "800",
                            "GTÜRÜ": "2",
                            "ÜCRETTÜRÜ": "6",
                            "EK HİZMET": " ",
                            "KDV": "8",
                            "SİP NO": "",
                            "ÇIKIŞ NO": "",
                            "SATICI": "",
                            "HATTAR": "",
                            "FATTAR": "",
                            "EN": "10",
                            "BOY": "15",
                            "YÜKSEKLİK": "10",


                        }
                    ]
                )
                # Adding updated data to the dataframe
          updated_df = pd.concat(
          [veriler_data, updated_vendor_data], ignore_index=True
                )
          connect.update(worksheet="aras_kargo", data=updated_df)
          st.success("Vendor details successfully updated!")
