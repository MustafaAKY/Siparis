import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
import time

tab11, tab22 = st.tabs(["Sipariş", "SİL"]      )
with tab11:

        st.title ("Sipariş Kaydetme Ekranı")
        
        
        
        connect = st.connection("gsheets",type=GSheetsConnection)
        veriler_data = connect.read(worksheet="aras_kargo", usecols=list(range(23)),ttl=5)
        veriler_data = veriler_data.dropna(how="all") 
        
        
        veriler_data2 = connect.read(worksheet="ptt_kargo", usecols=list(range(23)),ttl=5)
        veriler_data2 = veriler_data2.dropna(how="all") 
        
        
        
        
        # Sonucu ekrana yazdır
        
        
        
        #st.dataframe(veriler_data2)
        st.markdown("KARGO SEÇ")
        SUBELER = [
                "ARAS KARGO",
                "PTT",]
        
        kargo_tip = st.selectbox("Hangi Kargo",["ARAS KARGO","PTT",])
        
        Hangi_veri=""
        if kargo_tip=="ARAS KARGO":
            Hangi_veri=veriler_data
            sube_kodu="SUL"
            hangi_sube="aras_kargo"
        else:
            Hangi_veri=veriler_data2
            sube_kodu="155"
            hangi_sube="ptt_kargo"   
        
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
                bilgiler = st.text_area(label="ADRESLER*",value="",placeholder="Siparişi Buraya Yapıştır")
                st.markdown("**Zorunlu*")
                dugme= st.form_submit_button(label="Siparişi Kaydet")
                
                #dugme2 = st.selectbox("Hangi Kargo",options=SUBELER, index=None)
                
              
                sube_kodu =""
                if kargo_tip == "ARAS KARGO":
                    
                    sube_kodu ="SUL"
                else:
                   
                    sube_kodu ="155"      
                lines = bilgiler.title().split('\n')
                iller = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", 
                         "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", 
                         "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", 
                         "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", 
                         "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", 
                         "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]
                if len(lines) >= 6:
                            isim_soyisim = lines[0]
                            adres_bilgisi = lines[1]
                            ilce_il = lines[2].split()
                            
                            if len(ilce_il) == 2:
                                ilce = ilce_il[0]
                                il = ilce_il[1]
                                telefon = lines[3]
                                ucret = lines[4]
                                urun_bilgisi = '\n'.join(lines[6:])
        
                                   
                            elif len(ilce_il) == 1:
                                ilce = ilce_il[0]
                                il = lines[3].split()
                                il = il[0]
                                telefon = lines[4]
                                ucret = lines[5]
                                urun_bilgisi = '\n'.join(lines[7:])
        
                            
                            if il == "Istanbul":
                                    il = "İstanbul"
                            elif il == "i̇stanbul":
                                    il = "İstanbul"  
                            elif ilce == "Istanbul":
                                    ilce = "İstanbul"      
                            elif ilce=="i̇stanbul" :
                                    ilce = "İstanbul"
                            elif il =="Izmir":
                                    il ="İzmir"
                            elif il =="i̇zmir":
                                    il =  "İzmir"   
                            elif ilce == "i̇zmir":
                                    ilce="İzmir"                                     
                            elif ilce == "Izmir":
                                    ilce="İzmir"  
                        
                            if il not in iller:
                                    # Eğer şehir listede yoksa, 3. ve 4. satırları değiştir
                                  ilce, il = il, ilce
                        
                        
                            ilce_il = lines[2]
                            if il not in iller:
                               st.warning('İL DOĞRU DEĞİL KONTROL ET', icon="🚨" )  
                               st.warning("il ilçede bu yazıyor " + ilce_il)     
                               st.stop()
                            telefon.replace(" ", "")
                            St.warning("telefon")  
                            if len(telefon.strip()) == 11:
                              pass       
                            else:
                               st.warning('Telefon Numarası Hatalı '+ telefon ,icon="🚨")
                               st.stop() 
                                     
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
        
                        if kargo_tip == "ARAS KARGO":
                            updated_df = pd.concat([veriler_data, veri_Giris], ignore_index=True)
                            connect.update(worksheet="aras_kargo", data=updated_df)
                        else:
                            updated_df1 = pd.concat([veriler_data2, veri_Giris], ignore_index=True)
                            connect.update(worksheet="ptt_kargo", data=updated_df1)
                        
                        st.success("Sipariş Kaydedildi")
                        time.sleep(3)    
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        elif action == "Sipariş Güncelle":
            st.markdown("Sipariş Seçin Ve güncelleyin")
            SUBELER = [
                "ARAS KARGO",
                "PTT",]
        
            #dugme2 = st.selectbox(label="Hangi Kargo",options=SUBELER, index=None)
        
            vendor_to_update = st.selectbox(
             "Güncelleme", options=Hangi_veri["İSİM SOYİSİM"].tolist()    
            )
                
                        
            veri_Giris = Hangi_veri[Hangi_veri["İSİM SOYİSİM"] == vendor_to_update].iloc[
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
                  Hangi_veri.drop(
                        Hangi_veri[
                        Hangi_veri["İSİM SOYİSİM"] == vendor_to_update
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
                                    "ŞUBE KOD":sube_kodu,
                                    "MÜŞTERİ NO":"",
                                    "TUTAR":TUTAR,
                                    "ÜRÜN":ÜRÜN,
                                    "MİKTAR": "1",
                                    "GRAM": "800",
                                    "GTÜRÜ": "2",
                                    "ÜCRETTÜRÜ": "6",
                                    "EK HİZMET": "",
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
                  [Hangi_veri, updated_vendor_data], ignore_index=True
                        )
                  connect.update(worksheet=hangi_sube, data=updated_df)
                  st.success("GÜNCELLENDİ")
        
        elif action == "Siparişleri Göster":
            st.dataframe(Hangi_veri)          
        
        elif action == "Sipariş Sil":
            vendor_to_delete = st.selectbox(
                "Siparişi silindi", options=Hangi_veri["İSİM SOYİSİM"].tolist()
            )
        
            if st.button("SİL"):
                Hangi_veri.drop(
                    Hangi_veri[Hangi_veri["İSİM SOYİSİM"] == vendor_to_delete].index,
                    inplace=True,
                )
                connect.update(worksheet=hangi_sube, data=Hangi_veri)
                st.success("SİLİNDİ")
        tab1, tab2 = st.tabs(["Tab 1", "Sapariş Sayısı"]      )  
        dolu_hucreler = veriler_data['İSİM SOYİSİM'].dropna()
        dolu_hucreler2 = veriler_data2['İSİM SOYİSİM'].dropna()
        # A sütunundaki dolu hücrelerin sayısını hesapla
        dolu_hucre_sayisi = dolu_hucreler.shape[0]
        dolu_hucre_sayisi2 = dolu_hucreler2.shape[0]
        tab2.write(f"ARAS KARGO SİPARİŞ SAYISI:  {dolu_hucre_sayisi}")
        tab2.write(f"PTT KARGO SİPARİŞ SAYISI:  {dolu_hucre_sayisi2}")
        
with tab22: 
    st.title ("Sipariş Silme Ekranı")
    st.text("DİKKAT SİPARİŞLERİ YAZDIRDIĞINDAN EMİN OL")
    if st.button("Hepsini Sil"):
                            
            Hangi_veri.drop(Hangi_veri.index, inplace=True)
            connect.update(worksheet=hangi_sube, data=Hangi_veri)
            st.success("Tüm veri silindi!")        
