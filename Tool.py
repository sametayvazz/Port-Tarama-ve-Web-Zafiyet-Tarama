from socket import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
tekrar = "1"

while(tekrar == "1"):

    print("*"*50)
    print("İşlemler")
    print("1) Port Tarama")
    print("2) SQL Injection Taraması")
    print("3) XSS Taraması")
    print("4) Çıkış")
    print("")

    secim = input("Seçiminiz: ")
    print("*"*50)

    if(secim == "4"):
        print("Çıkış Yapılıyor..!!")
        break

    if(secim == "1"):
        
        print("Örnek Host: google.com")
        HedefHost=input("Host Giriniz: ")
        def PortTarama(HedefPort):
            try:
                sock = socket(AF_INET,SOCK_STREAM)
                sock.connect((HedefHost,HedefPort))        
                return True
            except:       
                return False
            finally:
                sock.close()

        def HostTarama(HedefPort):            
            for x in HedefPort:
                if PortTarama(x):
                    print(f"[+] {x} => Açık")
                else:
                    print(f"[-] {x} => Kapalı")  

        def HostBilgi(HedefHost):
            try:
                HedefIP = gethostbyname(HedefHost)
                print("\n")
                print("*"*50)
                print(f"IP adresi: {HedefIP}")
                try:
                    HedefAd=gethostbyaddr(HedefIP)
                    print(f"Makine Adı: {HedefAd[0]}")
                    print("*"*50)
                    print()
                except:
                    print("makine adı bulunamadı")  
                    print("*"*50)
            except:
                print(f"Host bulunamadı: {HedefHost}")

        def main():
            tus=1
            while(tus>0):

                HedefBilgi = input("Hedef İp adres ve Makine adı öğrenmek ister misiniz? (y/n): ") 

                if(HedefBilgi == "y"):        
                    tus = 0
                elif(HedefBilgi == "n"):
                    tus = 0
                else:
                    print("Hatalı tuşlama yaptınız. Tekrar giriniz ")       

            HedefPort=[]
            tekrar=1

            while(int(tekrar)>0):
                b=input("port: ")
                HedefPort.append(int(b))
                tekrar=input("Başka port girmek için 1 and çıkış için 0 tuşlayınız : ")

                while(tekrar != 1 or tekrar != 0):
                    if(tekrar == "1"):
                        tekrar = 1
                        break
                    elif(tekrar == "0"):
                        tekrar = 0
                        break
                    else:
                        print("Hatalı tuşlama yaptınız. Tekrar giriniz ")

                    tekrar=input("Başka port girmek için 1 and çıkış için 0 tuşlayınız : ")

            if(HedefBilgi == "y"):
                HostBilgi(HedefHost)
            HostTarama(HedefPort)

        if __name__ == "__main__":
            main()

    if(secim == "2"):

        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        print("Örnek URL : https://google.com")
        HedefURL=input("URL Giriniz:  ")

        def FormGetir(url): #form çağırma
            soup = BeautifulSoup(s.get(url).content, "html.parser")
            return soup.find_all("form")

        def FormDetay(form):  #form içeriği
            FormDetaylari={}
            action = form.attrs.get("action")
            method = form.attrs.get("method", "get")
            inputs=[]

            for input_tag in form.find_all("input"):   #inputları alıyoruz
                input_type=input_tag.attrs.get("type", "text")
                input_name=input_tag.attrs.get("name")
                input_value=input_tag.attrs.get("value", "")
                inputs.append({
                    "type": input_type,
                    "name": input_name,
                    "value": input_value,
                })
            FormDetaylari['action'] = action
            FormDetaylari['method'] = method
            FormDetaylari['inputs'] = inputs
            return FormDetaylari
        
        def SQI_Tarama(url):
            sqlhata="\"'"
            forms = FormGetir(url)   
            print(" ")
            print(f"--> {url} sitesinde {len(forms)} form saptandı. <--")    
            print(" ")
            for form in forms:
                details = FormDetay(form)    
                target_url = urljoin(url,details["action"])
                for i in "\"'":
                    data = {}
                    for input_tag in details["inputs"]:
                        if input_tag["type"] == "hidden" or input_tag["value"]:
                            data[input_tag['name']]=input_tag["value"] + i                                             
                    
                    FormDetay(form)
                    if details["method"] == "post":
                        res = s.post(target_url, data=data)
                    elif details["method"] =="get":
                        res = s.get(target_url, params=data)

                    content = res.content.decode()
                    if sqlhata in content:
                        print("[+] SQL injection Zafiyeti Bulundu")
                        break
                
                    else:
                        print("[-] SQL injection Zafiyeti Bulunamadı")
                        break
                   
        if __name__ == "__main__":
            url = HedefURL
            SQI_Tarama(url)

    if(secim == "3"):

        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

        print("Örnek URL : https://google.com")
        HedefURL=input("URL Giriniz:  ")

        def FormGetir(url): #form çağırma
            soup = BeautifulSoup(s.get(url).content, "html.parser")
            return soup.find_all("form")

        def FormDetay(form):  #form içeriği
            FormDetaylari={}
            action = form.attrs.get("action")
            method = form.attrs.get("method", "get")
            inputs=[]

            for input_tag in form.find_all("input"):   #inputları alıyoruz
                input_type=input_tag.attrs.get("type", "text")
                input_name=input_tag.attrs.get("name")
                input_value=input_tag.attrs.get("value", "")
                inputs.append({
                    "type": input_type,
                    "name": input_name,
                    "value": input_value,
                })
            FormDetaylari['action'] = action
            FormDetaylari['method'] = method
            FormDetaylari['inputs'] = inputs
            return FormDetaylari
                    
        def XSS_Tarama(url):    
            XSSKod = "<script>alert('hi')</script>"   
            forms = FormGetir(url)         
            print(" ")
            print(f"--> {url} sitesinde {len(forms)} form saptandı. <--")    
            print(" ")
            data = {}           
            for form in forms:
                details = FormDetay(form)    
                target_url = urljoin(url,details["action"])
                for i in XSSKod:
                    for input in details["inputs"]:
                        if input["type"] == "text" or input["type"]== "search":            
                            input["value"] = XSSKod                            
                            input_name = input.get("name")
                            input_value = input.get("value")
                            if input_name and input_value:
                                data[input_name] = input_value
                        
                    FormDetay(form)
                    if details["method"] == "post":
                        res = requests.post(target_url,data=data)
                    elif details["method"] == "get":
                        res = requests.get(target_url,params=data)
                    
                    content = res.content.decode()
                    if XSSKod in content:
                        print("[+] XSS Zafiyeti Bulundu")
                        break
                    else:
                        print("[-] XSS Zafiyeti Bulunamadı")
                        break
                               
        if __name__ == "__main__":
            url = HedefURL
            XSS_Tarama(url)

