import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
import time
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
st.set_page_config(layout="wide")
tab11, tab22 ,tab33= st.tabs(["Sipariş", "SİL","KARGO TAKİP"]  )
with tab11:

        st.title ("Sipariş Kaydetme Ekranı")
        
        
        
        connect = st.connection("gsheets",type=GSheetsConnection)
        veriler_data = connect.read(worksheet="aras_kargo", usecols=list(range(23)),ttl=5)
        veriler_data = veriler_data.dropna(how="all") 
        
        
        veriler_data2 = connect.read(worksheet="ptt_kargo", usecols=list(range(23)),ttl=5)
        veriler_data2 = veriler_data2.dropna(how="all") 
        
        
        
        
        # Sonucu ekrana yazdır
        
        
        
        #st.dataframe(veriler_data2)
        siparis_sayi = veriler_data['İSİM SOYİSİM'].dropna()
        siparis_sayi = siparis_sayi.shape[0]
        if siparis_sayi <= 5 :
                ico = "too_sad_26009.png"
        elif 6 <= siparis_sayi <= 10 :  
                ico = "h1.png"                
        elif 11 <= siparis_sayi <= 20 :
                ico = "money.png"               
        else:
                ico = "bmw.png"
        st.image(ico)
        SUBELER = [
                "ARAS KARGO",
                "PTT"]
        
        kargo_tip = st.selectbox("Hangi Kargo",["ARAS KARGO","PTT"])
        
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
        
                            telefon = telefon.replace(" ", "")
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
                            if len(telefon) == 11:
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
                        time.sleep(1)    
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
        
                    ÜRÜN = st.text_area(
                    
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

with tab33:
        st.title ("KARGO TAKİP ETME EKRANI")    
        st.image("aras.jpg",caption='ARAS KARGO KARGO TAKİP')

        kullanici_Adi = "seffafbutik@yesilkar.com"
        sifre = "Ma123456"

            # Giriş linki ve istek başlıkları
        login_link = "http://webpostman.yesilkarkargo.com:9999/user/login"
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
            }

            # Giriş isteği yap
        login_response = requests.get(login_link, headers=headers)

            # BeautifulSoup ile HTML'i ayrıştır
        bs = BS(login_response.content, 'html5lib')

            # Giriş form verileri ve token değerini al
        form_data = {
                "token": bs.find('input', attrs={'name': 'token'})['value'],
                "return_url": "/",
                "email": kullanici_Adi,
                "password": sifre
            }


        
        takip = st.text_input("Takip Kodu - Yada Telefon",placeholder='buraya yapıştır').strip()
        takip = "".join(takip.split())
        if len(takip) == 13:



            if takip:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
                url1 = f"https://kargotakip.araskargo.com.tr/mainpage.aspx?code={takip}"
                
                response = requests.get(url1,headers=headers)
                
                # HTML içeriğini BeautifulSoup kullanarak analiz edin
                soup = BS(response.content,"html5lib")
                
                link_veri = soup.findAll("a")
                for a_tag in link_veri:
                    href_attribute = a_tag['href']
                    if "CargoInfoWaybillAndDelivered.aspx" in href_attribute:
                        link_veri=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")
                        
                    if "CargoInfoTransactionAndRedirection.aspx" in href_attribute:
                        cıktı_sonuc=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")    
                            
                bilgiler =[]

                response=requests.get(link_veri)
                soup=BS(response.text,"html5lib")
                cıkıs_sube = soup.find("span",{"id":"cikis_subesi"}).text
                teslimat_sube = soup.find("span",{"id":"varis_subesi"}).text
                gonderim_Tarihi = soup.find("span",{"id":"cikis_tarihi"}).text
                son_durum = soup.find("span",{"id":"Son_Durum"}).text
                alici_adi = soup.find("span",{"id":"alici_adi_soyadi"}).text
                gonderi_tip = soup.find("span",{"id":"LabelGonTipi"}).text
                bilgiler.append({"Alıcı Adı":alici_adi,"Çıkış Şube":cıkıs_sube,"Teslimat Şubesi":teslimat_sube,"Gönderim Tarihi":gonderim_Tarihi,"Kargo Son durum":son_durum,"Gönderi tip":gonderi_tip  })
                response=requests.get(cıktı_sonuc)
                soup=BS(response.text,"html5lib")
                tablo = soup.find("table").findAll("tr")


                if son_durum == "TESLİM EDİLDİ" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ TESLİM EDİLDİ</h1>", unsafe_allow_html=True)

                elif son_durum == "YOLDA" :
                    st.markdown("<h1 style='color: blue; font-size: 36px;'>KARGONUZ YOLDADIR EN KISA SÜREDE SİZE GELECEK</h1>", unsafe_allow_html=True)    

                elif gonderi_tip == "İADE" :
                    st.markdown("<h1 style='color: red; font-size: 36px;'>KARGONUZ İADE EDİLMİŞTİR GERİ DÖNÜYOR</h1>", unsafe_allow_html=True)
                        
                elif son_durum == "TESLİMATTA" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ DAĞITIMA ÇIKMIŞ BUGÜN GELEBİLİR</h1>", unsafe_allow_html=True) 
                        
                else:
                    
                    st.markdown("<h1 style='color: orange; font-size: 25px;'>KARGONUZ ARAS KARGO ŞUBESİNDE EN KISA SÜREDE ALMANIZ GEREKİYOR</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='color: red; font-size: 36px;'>ARAS KARGO {teslimat_sube} ŞUBESİ</h1>", unsafe_allow_html=True)      


                st.dataframe(bilgiler)
                for td in tablo[0:2]:
                    ts = (td.text)
                    st.text(ts)              
        elif len(takip) == 11:
            if takip:
                tarih_baslangic = datetime.now()
                oncesi_15_gun = tarih_baslangic - timedelta(days=15)
                tarih_bitis = datetime.now().strftime("%d.%m.%Y")
                tarih_baslangic = oncesi_15_gun.strftime("%d.%m.%Y")
                
                giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
                kullanici = BS(giris.content, "html.parser")
                cookie = login_response.cookies
                cargo_link = f"http://webpostman.yesilkarkargo.com:9999/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno=&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
                print(cargo_link)
                cargo_response = requests.get(cargo_link, cookies=cookie)
                cargo_bs = BS(cargo_response.content, "html5lib")
                tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
                liste = []
                st.title("GÖNDERİLEN KARGOLAR")
                for satir in tablo:
                    sütunlar = satir.find_all("td")
                    veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                    liste.append({"TAKİP KODU":veriler[4], 
                    "İSİM SOYİSİM":veriler[5],
                    "TELEFON NU":"0"+veriler[19],
                    "SONUÇ":veriler[9],
                    "KARGO ŞUBESİ":veriler[10],
                    "ÜCRET":veriler[13]+" TL"  })    
                
                
                df = pd.DataFrame(liste)
                def arama(telefon_numarasi):
                    sonuc = df[df["TELEFON NU"] == telefon_numarasi]
                    if not sonuc.empty:
                        takip_kodu = sonuc.iloc[0]["TAKİP KODU"]
                        return takip_kodu
                    else:
                        st.warning("Telefon Numarası bulunamadı.")
                arama(takip)
                takip_kodu = arama(takip)
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
                url1 = f"https://kargotakip.araskargo.com.tr/mainpage.aspx?code={takip_kodu}"
                
                response = requests.get(url1,headers=headers)
                
                # HTML içeriğini BeautifulSoup kullanarak analiz edin
                soup = BS(response.content,"html5lib")
                
                link_veri = soup.findAll("a")
                for a_tag in link_veri:
                    href_attribute = a_tag['href']
                    if "CargoInfoWaybillAndDelivered.aspx" in href_attribute:
                        link_veri=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")
                        
                    if "CargoInfoTransactionAndRedirection.aspx" in href_attribute:
                        cıktı_sonuc=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")    
                            
                bilgiler =[]

                response=requests.get(link_veri)
                soup=BS(response.text,"html5lib")
                cıkıs_sube = soup.find("span",{"id":"cikis_subesi"}).text
                teslimat_sube = soup.find("span",{"id":"varis_subesi"}).text
                gonderim_Tarihi = soup.find("span",{"id":"cikis_tarihi"}).text
                son_durum = soup.find("span",{"id":"Son_Durum"}).text
                alici_adi = soup.find("span",{"id":"alici_adi_soyadi"}).text
                gonderi_tip = soup.find("span",{"id":"LabelGonTipi"}).text
                bilgiler.append({"Alıcı Adı":alici_adi,"Çıkış Şube":cıkıs_sube,"Teslimat Şubesi":teslimat_sube,"Gönderim Tarihi":gonderim_Tarihi,"Kargo Son durum":son_durum,"Gönderi tip":gonderi_tip  })
                response=requests.get(cıktı_sonuc)
                soup=BS(response.text,"html5lib")
                tablo = soup.find("table").findAll("tr")


                if son_durum == "TESLİM EDİLDİ" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ TESLİM EDİLDİ</h1>", unsafe_allow_html=True)

                elif son_durum == "YOLDA" :
                    st.markdown("<h1 style='color: blue; font-size: 36px;'>KARGONUZ YOLDADIR EN KISA SÜREDE SİZE GELECEK</h1>", unsafe_allow_html=True)    

                elif gonderi_tip == "İADE" :
                    st.markdown("<h1 style='color: red; font-size: 36px;'>KARGONUZ İADE EDİLMİŞTİR GERİ DÖNÜYOR</h1>", unsafe_allow_html=True)
                        
                elif son_durum == "TESLİMATTA" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ DAĞITIMA ÇIKMIŞ BUGÜN GELEBİLİR</h1>", unsafe_allow_html=True) 
                        
                else:
                    
                    st.markdown("<h1 style='color: orange; font-size: 25px;'>KARGONUZ ARAS KARGO ŞUBESİNDE EN KISA SÜREDE ALMANIZ GEREKİYOR</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='color: red; font-size: 36px;'>ARAS KARGO {teslimat_sube} ŞUBESİ</h1>", unsafe_allow_html=True)      

                st.text(f"TAKİP KODU : {takip_kodu}")
                st.dataframe(bilgiler)
                for td in tablo[0:2]:
                    ts = (td.text)
                    st.text(ts)               
#tarihe göre listeleme kargoları 



            # Giriş isteği yap
        tarih_baslangic = st.date_input(label="BAŞLANGIÇ TARİH")
        if tarih_baslangic:
            tarih_baslangic = (tarih_baslangic.strftime("%d.%m.%Y"))
        tarih_bitis = st.date_input(label="BİTİŞ TARİH")
        if tarih_bitis:
            tarih_bitis = (tarih_bitis.strftime("%d.%m.%Y"))    
            
        if st.button("ŞUBEDE BEKLEYEN KARGOLARI LİSTELE"):    
            giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
            kullanici = BS(giris.content, "html.parser")
            cookie = login_response.cookies
            cargo_link = f"http://webpostman.yesilkarkargo.com:9999/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno=&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
            
            cargo_response = requests.get(cargo_link, cookies=cookie)
            cargo_bs = BS(cargo_response.content, "html5lib")
            tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
            liste = []
            st.title("ŞUBEDE BEKLEYEN KARGOLAR")
            for satir in tablo:
                sütunlar = satir.find_all("td")
                veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                if veriler[8] == "Teslim" or veriler[8] == "Paketleme" or veriler[8] == "İade" or veriler[9] == "Yolda":
                    continue

                liste.append({"TAKİP KODU":veriler[4], 
                  "İSİM SOYİSİM":veriler[5],
                  "TELEFON NU":"0"+veriler[19],
                  "SONUÇ":veriler[9],
                  "KARGO ŞUBESİ":veriler[10],
                  "ÜCRET":veriler[13]+" TL"  })   
                
        
            db = st.dataframe(liste)
            sayı = len(liste)

            st.markdown(f"<h1 style='color: green; font-size: 36px;'>Aras Kargo Şubesinde  {sayı} Adet kargo bekliyor</h1>", unsafe_allow_html=True)

        if st.button(f"{tarih_baslangic} - {tarih_bitis} ARASI ÇIKMIŞ KARGOLARI LİSTELE"):
            giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
            kullanici = BS(giris.content, "html.parser")
            cookie = login_response.cookies
            cargo_link = f"http://webpostman.yesilkarkargo.com:9999/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno=&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
            
            cargo_response = requests.get(cargo_link, cookies=cookie)
            cargo_bs = BS(cargo_response.content, "html5lib")
            tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
            liste = []
            st.title("GÖNDERİLEN KARGOLAR")
            for satir in tablo:
                sütunlar = satir.find_all("td")
                veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                liste.append({"TAKİP KODU":veriler[4], 
                  "İSİM SOYİSİM":veriler[5],
                  "TELEFON NU":"0"+veriler[19],
                  "SONUÇ":veriler[9],
                  "KARGO ŞUBESİ":veriler[10],
                  "ÜCRET":veriler[13]+" TL"  })

            db = st.dataframe(liste) 
            sayı = len(liste)
            
            st.markdown(f"<h1 style='color: green; font-size: 36px;'>GÖNDERİLEN KARGO {sayı} </h1>", unsafe_allow_html=True)
