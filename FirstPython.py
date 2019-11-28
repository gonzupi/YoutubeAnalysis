# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2019

@author: Gonzalo Bueno Santana
Programa pensado para extraer datos de la plataforma YouTube usando diferentes navegadores : Google Chrome, Mozilla Firefox, Microsoft Edge y Opera
El programa extrae información con sesión iniciada y sin la sesión iniciada para después compararla
'''
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import threading
from selenium.webdriver.chrome import service
import socket
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.opera import options
import os
from selenium.webdriver.common.proxy import *
from scipy import integrate

#Variables globales
#######################################
host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name) 
print("IP : ",host_ip) 
start_time = time.time()

WithProxy=0
# WithProxy = 1;
myProxy = None # "http://149.215.113.110:70"
proxy = Proxy({
'proxyType': ProxyType.MANUAL,
'httpProxy': myProxy,
'ftpProxy': myProxy,
'sslProxy': myProxy,
'noProxy':''})

tiempoEspera = 12
tiempoEspera_Nombre = 12
tiempoEspera_Ad = 1
tiempoEspera_Login = 30000
sleepTime = 3
####################################

def ChromeFunc():
    ##Iniciamos GOOGLE CHROME, la cabecera del dataFrame y la función de espera para cada parámetro.
    #driverGC = webdriver.Chrome()
    print('GC_Iniciando Chrome')
    caps = DesiredCapabilities().CHROME
    
#     Proxy proxy = new Proxy();
#     proxy.setHttpProxy("127.0.0.1:1234");
#     caps.setCapability("proxy", proxy);
 
    caps["pageLoadStrategy"] = "normal"
    if WithProxy==1 :
        driverGC = webdriver.Chrome(desired_capabilities=caps, proxy=proxy)
    if WithProxy==0 :
        driverGC = webdriver.Chrome(desired_capabilities=caps)
    dfGC = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    waitGC = WebDriverWait(driverGC,tiempoEspera)
    waitGC_name = WebDriverWait(driverGC,tiempoEspera_Nombre)
    waitGC_Ads = WebDriverWait(driverGC,tiempoEspera_Ad)
    waitGC_login = WebDriverWait(driverGC,tiempoEspera_Login)
    driverGC.maximize_window() 
    MiIp_GC=host_ip
    
    #Iniciamos sesión y nos vamos a YouTube
    driverGC.get('https://accounts.google.com/signin/v2/identifier')
    print('GC_Vamos a iniciar sesion')
    waitGC_login.until(EC.url_changes)
    waitGC_login.until(EC.url_contains('myaccount.google.com')) 
    driverGC.get("http://www.youtube.com/")
    try:
        waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    except:
        time.sleep(sleepTime)
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
            driverGC.find_elements_by_xpath('//*[@id="video-title"]')
        except:
            time.sleep(sleepTime)
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))

    user_dataGC=driverGC.find_elements_by_xpath('//*[@id="video-title"]')
    print('GC_A extraer ', len(user_dataGC), ' vídeos')
    
    #Obtengo los links de la página principal.
    linksGC = []
    for i in user_dataGC:
        try:
            linksGC.append(i.get_attribute('href'))
        except:
            print('GC_EEROR : Link ERROR')
        
    #Y ahora a extraer los datos de cada link.
    v_navegador_GC = 'Google Chrome'
    v_sesionInit_GC = 'True'
    try:
        v_addPrintipalName_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print('GC_No se ha obtenido anuncio del mainPage')
        v_addPrintipalName_GC='No hay anuncio principal'
        v_addPrintipalLink_GC = 'No hay anuncio principal'
    dfGC.loc[len(dfGC)] = [v_addPrintipalLink_GC, v_addPrintipalName_GC,MiIp_GC, 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador_GC, v_sesionInit_GC, '0']   
    
    numVideo_GC = 0
    for x in linksGC:    
        driverGC.get(x)
        v_id_GC = x.strip('https://www.youtube.com/watch?v=')

        #Título
        try:
            v_title_GC = waitGC_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except:
            try:
                time.sleep(sleepTime)
                v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                try:
                    time.sleep(sleepTime)
                    v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    v_title_GC = 'ERROR'
        if v_title_GC==None or v_title_GC=='':
            try:
                time.sleep(sleepTime)
                v_title_GC = waitGC_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                try:
                    time.sleep(sleepTime)
                    v_title_GC = waitGC_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    print('GC_ERROR : No título')
                    v_title_GC = 'ERROR'
        
        #Número de comentarios
        try:
            v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
        except:
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(sleepTime)
                v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except:
                
                try:
                    waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                    time.sleep(sleepTime)
                    v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                except:
                    print('GC_ERROR : No he podido obtener el número de comentarios')
                    v_numComments = 'ERROR'
                 
        #Categoría    
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
        except:
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
            except:
                print('GC_ERROR : Boton ver más')
        try:
            v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
        except: 
            time.sleep(sleepTime)    
            try:
                v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except:
                time.sleep(sleepTime)    
                try:
                    v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
                except:
                    print('GC_ERROR : No he podido obtener la categoría')
                    v_category_GC = 'ERROR'   
        
        #Descripción
        try:
            v_description_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
        except:
            print('GC_ERROR : descripción')
            v_description_GC = 'ERROR'
        
        #Número de visualizaciones
        try:
            v_numVisualizacioness_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                v_numVisualizacioness_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text   
            except:
                print('GC_ERROR : número de visualizaciones')
                v_numVisualizacioness_GC = 'ERROR'
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
        except:
            print("GC_ERROR : subir página")
        ##RESETEO A POSICION DE ARRIBA
        #Fecha
        try:
            v_fecha_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_fecha_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
            except:
                print('GC_ERROR : la fecha')
                v_fecha_GC = 'ERROR'
        
        try:
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print("GC_ERROR : subir página")
            
        ##RESETEO A POSICION DE ARRIBA

        #Me gusta/no me gusta
        try:
            v_likes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_likes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
            except:
                print('GC_ERROR : me gusta')
                v_likes_GC='ERROR'
        try:
            v_dislikes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_dislikes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
            except:
                print('GC_ERROR : me gusta')
                v_dislikes_GC='ERROR'
         
        #Nombre del canal
        try:
            v_channel_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_channel_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
            except:    
                print('GC_ERROR : Nombre del canal')
                v_channel_GC = 'ERROR'
        try:
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print('GC_ERROR : PAGE UP')
        ##RESETEO A POSICION DE ARRIBA 
               
        #Link del canal
        try:
            v_channelLink_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
        except :
            print ('ERROR : link del canal')
            v_channelLink_GC='ERROR'
        
        #Num subs
        try:
            v_channelSubs_GC=waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
        except :
            print('GC_ERROR :  número de subscripciones al canal')
            v_channelSubs_GC='Error'
        
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print("GC_ERROR : subir página")
        ##RESETEO A POSICION DE ARRIBA 
               
        #Link del anuncio/nombre del anuncio
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print('GC_ERROR:Page up')
        try:
            v_addLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
        except :
            v_addLink_GC='ERROR'
        
        if v_addLink_GC != 'ERROR' :
            print('GC_Anuncio : ',v_addLink_GC)
        
        dfGC.loc[len(dfGC)] = [v_id_GC, v_title_GC, v_category_GC, v_description_GC,v_numComments, v_fecha_GC,v_numVisualizacioness_GC, v_likes_GC, v_dislikes_GC,v_channel_GC , v_channelLink_GC, v_channelSubs_GC, v_navegador_GC, v_sesionInit_GC, v_addLink_GC]   
        numVideo_GC = numVideo_GC +1
        print ('GC_Extraido con sesión iniciada, número : ' , numVideo_GC ,' de ', len(linksGC), ' llamado : ', v_title_GC)
    
    #Cierro el navegador
    driverGC.close()
    print('GC_Finalizado : recoger datos de google Chrome con sesión iniciada')
    
    #############
    print('GC_Copiando datos al excel')
    frames = [dfGC ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    
    
    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + MiIp_GC + '_GC.csv', encoding='utf-8', index=False)
    print('GC_Extracción de datos con sesión iniciada terminada')

    #Calculate elapsed time
    temp = time.time() - start_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('MF_SS_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))
    print('GC_Recuerda, tu ip es : ', MiIp_GC)

def ChromeFuncNoSesion():
    ##Iniciamos GOOGLE CHROME, la cabecera del dataFrame y la función de espera para cada parámetro.
    #driverGC = webdriver.Chrome()
    print('GC_SS_Iniciando Chrome')    
    caps = DesiredCapabilities().CHROME
    
#     Proxy proxy = new Proxy();
#     proxy.setHttpProxy("127.0.0.1:1234");
#     caps.setCapability("proxy", proxy);

    
    caps["pageLoadStrategy"] = "normal"
    if WithProxy==1 :
        driverGC = webdriver.Chrome(desired_capabilities=caps, proxy=proxy)
    if WithProxy==0 :
        driverGC = webdriver.Chrome(desired_capabilities=caps)
    dfGC = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    waitGC = WebDriverWait(driverGC,tiempoEspera)
    waitGC_name = WebDriverWait(driverGC,tiempoEspera_Nombre)
    waitGC_Ads = WebDriverWait(driverGC,tiempoEspera_Ad)
    #waitGC_login = WebDriverWait(driverGC,2000)
    driverGC.maximize_window()
    #################
    
    MiIp_GC=host_ip
    print('GC_Mi ip es :', MiIp_GC)
    
    #Iniciamos sesión y nos vamos a YouTube
#     driverGC.get('https://accounts.google.com/signin/v2/identifier')
#     print('GC_Vamos a iniciar sesion')
#     waitGC_login.until(EC.url_changes)
#     waitGC_login.until(EC.url_contains('myaccount.google.com'))
#     
    driverGC.get("http://www.youtube.com/")
    try:
        waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    except:
        time.sleep(sleepTime)
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
            driverGC.find_elements_by_xpath('//*[@id="video-title"]')
        except:
            time.sleep(sleepTime)
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))

    user_dataGC=driverGC.find_elements_by_xpath('//*[@id="video-title"]')
    print('GC_Extraidos : ', len(user_dataGC), ' vídeos')
    #Obtengo los links de la página principal.
    linksGC = []
    for i in user_dataGC:
        try:
            linksGC.append(i.get_attribute('href'))
        except:
            print('GC_SS ERROR :Link ERROR')
        
    #Y ahora a extraer los datos de cada link.
    v_navegador_GC = 'Google Chrome'
    v_sesionInit_GC = 'False'
    try:
        v_addPrintipalName_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print('GC_No se ha obtenido anuncio del mainPage')
        v_addPrintipalName_GC='No hay anuncio principal'
        v_addPrintipalLink_GC = 'No hay anuncio principal'
    dfGC.loc[len(dfGC)] = [v_addPrintipalLink_GC, v_addPrintipalName_GC,'0', 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador_GC, v_sesionInit_GC, '0']   
    
    ### EMPIEZO LA EXTRACCION
    numVideo_GC = 0
    for x in linksGC:    
        driverGC.get(x)
        v_id_GC = x.strip('https://www.youtube.com/watch?v=')
        if numVideo_GC == 0:
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
            except:
                time.sleep(sleepTime)
                try:
                    waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
                except:
                    print('MF_SS_ERROR : No he podido pulsar el botón de privacidad')
        #Título
        try:
            v_title_GC = waitGC_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except:
            try:
                time.sleep(sleepTime)
                v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                v_title_GC = 'ERROR'
        if v_title_GC==None or v_title_GC=='':
            try:
                time.sleep(sleepTime)
                v_title_GC = waitGC_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                print('GC_SS_ERROR : No título')
                v_title_GC = 'ERROR'
        
        #Número de comentarios
        try:
            v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
        except:
            
            try:
                waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(sleepTime)
                v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except: 
                try:
                    waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                    time.sleep(sleepTime)
                    v_numComments = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                except:
                    print('GC_SS_ERROR : No he podido obtener el número de comentarios')
                    v_numComments = 'ERROR'
                 
        #Categoría    
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
        except:
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
            except:
                print('GC_SS_ERROR : Boton ver más')
        try:
            v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
        except: 
            time.sleep(sleepTime)    
            try:
                v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except:
                print('GC_SS_ERROR : No he podido obtener la categoría')
                v_category_GC = 'ERROR'   
        
        #Descripción
        try:
            v_description_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
        except:
            print('GC_SS_ERROR : descripción')
            v_description_GC = 'ERROR'
        
        #Número de visualizaciones
        try:
            v_numVisualizacioness_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                v_numVisualizacioness_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text   
            except:
                print('GC_SS_ERROR : número de visualizaciones')
                v_numVisualizacioness_GC = 'ERROR'
        try:
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
        except:
            print("GC_SS_ERROR : subir página")
        ##RESETEO A POSICION DE ARRIBA
        #Fecha
        try:
            v_fecha_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_fecha_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
            except:
                print('GC_SS_ERROR : la fecha')
                v_fecha_GC = 'ERROR'
        try:
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print("GC_ERROR : subir página")
            
        ##RESETEO A POSICION DE ARRIBA

        #Me gusta/no me gusta
        try:
            v_likes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_likes_GC =  waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
            except:
                print('GC_SS_ERROR : me gusta')
                v_likes_GC='ERROR'
        try:
            v_dislikes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_dislikes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
            except:
                print('GC_SS_ERROR : me gusta')
                v_dislikes_GC='ERROR'
         
        #Nombre del canal
        try:
            v_channel_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
        except :
            try:
                waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                v_channel_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
            except:    
                print('GC_SS_ERROR : Nombre del canal')
                v_channel_GC = 'ERROR'
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print('GC_SS_ERROR : PAGE UP')
        ##RESETEO A POSICION DE ARRIBA 
               
        #Link del canal
        try:
            v_channelLink_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
        except :
            print ('GC_SS_ERROR : link del canal')
            v_channelLink_GC='ERROR'
        
        #Num subs
        try:
            v_channelSubs_GC=waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
        except :
            print('GC_SS_ERROR :  número de subscripciones al canal')
            v_channelSubs_GC='Error'
        try:
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print("GC_ERROR : subir página")
        ##RESETEO A POSICION DE ARRIBA 
               
        #Link del anuncio/nombre del anuncio
        try:
            v_addLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
        except :
            v_addLink_GC='ERROR'
        
        if v_addLink_GC != 'ERROR' :
            print('GC_SS_Anuncio : ',v_addLink_GC)
        
        dfGC.loc[len(dfGC)] = [v_id_GC, v_title_GC, v_category_GC, v_description_GC,v_numComments, v_fecha_GC,v_numVisualizacioness_GC, v_likes_GC, v_dislikes_GC,v_channel_GC , v_channelLink_GC, v_channelSubs_GC, v_navegador_GC, v_sesionInit_GC, v_addLink_GC]   
        numVideo_GC = numVideo_GC +1
        print ('GC_SS_Extraido con sesión iniciada, número : ' , numVideo_GC ,' de ', len(linksGC), ' llamado : ', v_title_GC)
    
    #Cierro el navegador
    driverGC.close()
    print('GC_SS_Finalizado : recoger datos de google Chrome con sesión iniciada')
    
    #############
    print('GC_SS_Copiando datos al excel')
    frames = [dfGC ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    
    
    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + MiIp_GC + '_GC_SS.csv', encoding='utf-8', index=False)
    print('GC_Extracción de datos con sesión iniciada terminada')

    #Calculate elapsed time
    temp = time.time() - start_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('MF_SS_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))
    print('GC_Recuerda, tu ip es : ', MiIp_GC)

def FirefoxFunc():
    ##Iniciamos Firefox, la cabecera del dataFrame y la función de espera para cada parámetro.
    #driverGC = webdriver.Chrome()
    print('MF_Iniciando Firefox')
    caps_MF = DesiredCapabilities().FIREFOX
    caps_MF["pageLoadStrategy"] = "normal"
    if WithProxy==1 :
        driverMF = webdriver.Firefox(desired_capabilities=caps_MF,  proxy=proxy)
    if WithProxy == 0 :
            driverMF = webdriver.Firefox(desired_capabilities=caps_MF)

    dfMF = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    waitMF = WebDriverWait(driverMF,tiempoEspera)
    waitMF_name = WebDriverWait(driverMF,tiempoEspera_Nombre)
    waitMF_Ads = WebDriverWait(driverMF,tiempoEspera_Ad)
    waitMF_login = WebDriverWait(driverMF,tiempoEspera_Login)
    driverMF.maximize_window()
    #################
    
    MiIp_MF = host_ip
    print('MF_Mi ip es :', MiIp_MF)
    
    #Iniciamos sesión y nos vamos a YouTube
    driverMF.get('https://accounts.google.com/signin/v2/identifier')
    print('MF_Vamos a iniciar sesion')
    waitMF_login.until(EC.url_changes)
    waitMF_login.until(EC.url_contains('myaccount.google.com'))
 

    driverMF.get("http://www.youtube.com/")
    try:
        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    except:
        time.sleep(sleepTime)
        try:
            waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
            driverMF.find_elements_by_xpath('//*[@id="video-title"]')
        except:
            time.sleep(sleepTime)
            waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))

    user_dataMF=driverMF.find_elements_by_xpath('//*[@id="video-title"]')
    print('MF_Extraidos : ', len(user_dataMF), ' vídeos')
    #Obtengo los links de la página principal.
    linksMF = []
    for i in user_dataMF:
        try:
            linksMF.append(i.get_attribute('href'))
        except:
            try:
                linksMF.append(i.get_attribute('href')) 
            except:
                print('MF_ERROR:Link error') 
    #Y ahora a extraer los datos de cada link.
    v_navegador_MF = 'Mozilla Firefox'
    v_sesionInit_MF = 'True'
    try:
        v_addPrintipalName_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print('MF_ERROR: anuncio del mainPage')
        v_addPrintipalName_MF='No hay anuncio principal'
        v_addPrintipalLink_MF = 'No hay anuncio principal'
    dfMF.loc[len(dfMF)] = [v_addPrintipalLink_MF, v_addPrintipalName_MF,'0', 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador_MF, v_sesionInit_MF, '0']   
    
    ### EMPIEZO LA EXTRACCION
    numVideo_MF = 0
    for x in linksMF: 
        try:   
            driverMF.get(x)
            v_id_MF = x.strip('https://www.youtube.com/watch?v=')
            if numVideo_MF == 0:
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
                except:
                    time.sleep(sleepTime)
                    try:
                        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
                    except:
                        print('MF_ERROR : No he podido pulsar el botón de privacidad')
            #Título
            try:
                v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                try:
                    time.sleep(sleepTime)
                    v_title_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    v_title_MF = 'ERROR'
            if v_title_MF==None or v_title_MF=='':
                try:
                    time.sleep(sleepTime)
                    v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    print('MF_ERROR : No título')
                    v_title_MF = 'ERROR'
            
            #Número de comentarios
            try:
                v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except:
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                    time.sleep(sleepTime)
                    v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                except:
                    try:
                        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                        time.sleep(sleepTime)
                        v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                    except:
                        print('MF_ERROR : No he podido obtener el número de comentarios')
                        v_numComments = 'ERROR'
                     
            #Categoría    
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
            except:
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
                except:
                    print('MF_ERROR : Boton ver más')
            try:
                v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except: 
                time.sleep(sleepTime)    
                try:
                    v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
                except:
                    print('MF_ERROR : No he podido obtener la categoría')
                    v_category_MF = 'ERROR'   
            
            #Descripción
            try:
                v_description_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
            except:
                print('MF_ERROR : descripción')
                v_description_MF = 'ERROR'
            
            #Número de visualizaciones
            try:
                v_numVisualizacioness_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                    v_numVisualizacioness_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text   
                except:
                    print('MF_ERROR : número de visualizaciones')
                    v_numVisualizacioness_MF = 'ERROR'
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            except:
                print('MF_ERROR : Page up')
            ##RESETEO A POSICION DE ARRIBA
            #Fecha
            try:
                v_fecha_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_fecha_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
                except:
                    print('MF_ERROR : la fecha')
                    v_fecha_MF = 'ERROR'
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_ERROR:Page up')
            ##RESETEO A POSICION DE ARRIBA
    
            #Me gusta/no me gusta
            try:
                v_likes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_likes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
                except:
                    print('MF_ERROR : me gusta')
                    v_likes_MF='ERROR'
            try:
                v_dislikes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_dislikes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
                except:
                    print('MF_ERROR : me gusta')
                    v_dislikes_MF='ERROR'
             
            #Nombre del canal
            try:
                v_channel_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
               
                    v_channel_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
                except:    
                    print('MF_ERROR : Nombre del canal')
                    v_channel_MF = 'ERROR'
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_ERROR : Page up')
            ##RESETEO A POSICION DE ARRIBA 
                   
            #Link del canal
            try:
                v_channelLink_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
            except :
                print ('MF_ERROR : link del canal')
                v_channelLink_MF='ERROR'
            
            #Num subs
            try:
                v_channelSubs_MF=waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
            except :
                print('MF_ERROR :  número de subscripciones al canal')
                v_channelSubs_MF='Error'
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_ERROR:Page up')
            ##RESETEO A POSICION DE ARRIBA 
                   
            #Link del anuncio/nombre del anuncio
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_ERROR:PAGE UP')
            try:
                v_addLink_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
            except :
                v_addLink_MF='ERROR'
            
            if v_addLink_MF != 'ERROR' :
                print('MF_Anuncio : ',v_addLink_MF)
            
            dfMF.loc[len(dfMF)] = [v_id_MF, v_title_MF, v_category_MF, v_description_MF,v_numComments, v_fecha_MF,v_numVisualizacioness_MF, v_likes_MF, v_dislikes_MF,v_channel_MF , v_channelLink_MF, v_channelSubs_MF, v_navegador_MF, v_sesionInit_MF, v_addLink_MF]   
            numVideo_MF = numVideo_MF +1
            print ('MF_Extraido con sesión iniciada, número : ' , numVideo_MF ,' de ', len(linksMF), ' llamado : ', v_title_MF)
        except:
            print('MF_ERROR:Link raro')
    #Cierro el navegador
    driverMF.close()
    print('MF_Finalizado : recoger datos de google Chrome con sesión iniciada')
    
    #############
    print('MF_Copiando datos al excel')
    frames = [dfMF ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    
    
    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + MiIp_MF + '_MF.csv', encoding='utf-8', index=False)
    print('MF_Extracción de datos con sesión iniciada terminada')

    #Calculate elapsed time
    temp = time.time() - start_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('MF_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))
    print('MF_Recuerda, tu ip es : ', MiIp_MF)

def FirefoxFuncNoSesion():
    ##Iniciamos Firefox, la cabecera del dataFrame y la función de espera para cada parámetro.
    #driverMF = webdriver.Chrome()
    print('MF_SS_Iniciando Firefox')
    caps_MF = DesiredCapabilities().FIREFOX
    caps_MF["pageLoadStrategy"] = "normal"
    if WithProxy == 1 :
        driverMF = webdriver.Firefox(desired_capabilities=caps_MF,  proxy=proxy)
    if WithProxy == 0 :
            driverMF = webdriver.Firefox(desired_capabilities=caps_MF)
    dfMF = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    waitMF = WebDriverWait(driverMF,tiempoEspera)
    waitMF_name = WebDriverWait(driverMF,tiempoEspera_Nombre)
    waitMF_Ads = WebDriverWait(driverMF,tiempoEspera_Ad)
    #waitMF_login = WebDriverWait(driverMF,tiempoEspera_Ad)
    driverMF.maximize_window()    
    MiIp_MF = host_ip
    print('MF_SS_Mi ip es :', MiIp_MF)
    
    #Iniciamos sesión y nos vamos a YouTube
    driverMF.get("http://www.youtube.com/")
    try:
        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    except:
        time.sleep(sleepTime)
        try:
            waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
            driverMF.find_elements_by_xpath('//*[@id="video-title"]')
        except:
            time.sleep(sleepTime)
            waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))

    user_dataMF=driverMF.find_elements_by_xpath('//*[@id="video-title"]')
    print('MF_SS_Extraidos : ', len(user_dataMF), ' vídeos')
    #Obtengo los links de la página principal.
    linksMF = []
    for i in user_dataMF:
        try:
            linksMF.append(i.get_attribute('href'))
        except:
            time.sleep(sleepTime)
            try:
                linksMF.append(i.get_attribute('href')) 
            except:
                print('MF_SS_ERROR:Link error')          
        
    #Y ahora a extraer los datos de cada link.
    v_navegador_MF = 'Mozilla Firefox'
    v_sesionInit_MF = 'False'
    try:
        v_addPrintipalName_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print('MF_SS_ERROR: anuncio del mainPage')
        v_addPrintipalName_MF='No hay anuncio principal'
        v_addPrintipalLink_MF = 'No hay anuncio principal'
    dfMF.loc[len(dfMF)] = [v_addPrintipalLink_MF, v_addPrintipalName_MF,'0', 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador_MF, v_sesionInit_MF, '0']   
    
    ### EMPIEZO LA EXTRACCION
    numVideo_MF = 0
    for x in linksMF:    
        try:
            driverMF.get(x)
            v_id_MF = x.strip('https://www.youtube.com/watch?v=')
            if numVideo_MF == 0:
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
                except:
                    time.sleep(sleepTime)
                    try:
                        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
                    except:
                        print('MF_SS_ERROR : No he podido pulsar el botón de privacidad')
            #Título
            try:
                v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                try:
                    time.sleep(sleepTime)
                    v_title_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    v_title_MF = 'ERROR'
            if v_title_MF==None or v_title_MF=='':
                try:
                    time.sleep(sleepTime)
                    v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
                except:
                    print('MF_SS_ERROR : No título')
                    v_title_MF = 'ERROR'
            
            #Número de comentarios
            try:
                v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except:
                
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                    time.sleep(sleepTime)
                    v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                except:
                    try:
                        waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                        time.sleep(sleepTime)
                        v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
                    except:
                        print('MF_SS_ERROR : No he podido obtener el número de comentarios')
                        v_numComments = 'ERROR'
                     
            #Categoría    
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
            except:
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
                except:
                    print('MF_SS_ERROR : Boton ver más')
            try:
                v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except: 
                time.sleep(sleepTime)    
                try:
                    v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
                except:
                    print('MF_SS_ERROR : No he podido obtener la categoría')
                    v_category_MF = 'ERROR'   
            
            #Descripción
            try:
                v_description_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
            except:
                print('MF_SS_ERROR : descripción')
                v_description_MF = 'ERROR'
            
            #Número de visualizaciones
            try:
                v_numVisualizacioness_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
                    v_numVisualizacioness_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text   
                except:
                    print('MF_SS_ERROR : número de visualizaciones')
                    v_numVisualizacioness_MF = 'ERROR'
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
            except:
                print('MF_SS_ERROR:Page up')
            ##RESETEO A POSICION DE ARRIBA
            #Fecha
            try:
                v_fecha_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_fecha_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
                except:
                    print('MF_SS_ERROR : la fecha')
                    v_fecha_MF = 'ERROR'
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_SS_ERROR : PAGE UP')
            ##RESETEO A POSICION DE ARRIBA
    
            #Me gusta/no me gusta
            try:
                v_likes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_likes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
                except:
                    print('MF_SS_ERROR : me gusta')
                    v_likes_MF='ERROR'
            try:
                v_dislikes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_dislikes_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
                except:
                    print('MF_SS_ERROR : me gusta')
                    v_dislikes_MF='ERROR'
             
            #Nombre del canal
            try:
                v_channel_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
            except :
                try:
                    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)  
                    v_channel_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
                except:    
                    print('MF_SS_ERROR : Nombre del canal')
                    v_channel_MF = 'ERROR'
    
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_SS_ERROR : Page up')
            ##RESETEO A POSICION DE ARRIBA 
                   
            #Link del canal
            try:
                v_channelLink_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
            except :
                print ('MF_SS_ERROR : link del canal')
                v_channelLink_MF='ERROR'
            
            #Num subs
            try:
                v_channelSubs_MF=waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
            except :
                print('MF_SS_ERROR :  número de subscripciones al canal')
                v_channelSubs_MF='Error'
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)  
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_SS_ERROR:PAGE UP')
            ##RESETEO A POSICION DE ARRIBA 
                   
            #Link del anuncio/nombre del anuncio
            try:
                waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            except:
                print('MF_SS_ERROR : PAGE UP')
            try:
                v_addLink_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
            except :
                v_addLink_MF='ERROR'
            
            if v_addLink_MF != 'ERROR' :
                print('MF_SS_Anuncio : ',v_addLink_MF)
            
            dfMF.loc[len(dfMF)] = [v_id_MF, v_title_MF, v_category_MF, v_description_MF,v_numComments, v_fecha_MF,v_numVisualizacioness_MF, v_likes_MF, v_dislikes_MF,v_channel_MF , v_channelLink_MF, v_channelSubs_MF, v_navegador_MF, v_sesionInit_MF, v_addLink_MF]   
            numVideo_MF = numVideo_MF +1
            print ('MF_SS_Extraido con sesión iniciada, número : ' , numVideo_MF ,' de ', len(linksMF), ' llamado : ', v_title_MF)
        except:
            print('MF_SS_ERROR:Link error')
    #Cierro el navegador
    driverMF.close()
    print('MF_SS_Finalizado : recoger datos de google Chrome con sesión iniciada')
    
    #############
    print('MF_SS_Copiando datos al excel')
    frames = [dfMF ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    
    
    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + MiIp_MF + '_MF_SS.csv', encoding='utf-8', index=False)
    print('MF_Extracción de datos con sesión iniciada terminada')

    #Calculate elapsed time
    temp = time.time() - start_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('MF_SS_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))
    print('MF_Recuerda, tu ip es : ', MiIp_MF)

def OtherFunc():
    ##Iniciamos Firefox, la cabecera del dataFrame y la función de espera para cada parámetro.
    #driverGC = webdriver.Chrome()
    print('MF_Iniciando Edge')
    ##########
    # create new Edge session
    #driver.get("http://www.opera.com")# success
    optionsop = webdriver.ChromeOptions()
    optionsop.binaty_location = "C:\\Users\\YoutubeProject\\AppData\\Local\\Programs\\Opera\\65.0.3467.48_0\\opera.exe"
    driverMF = webdriver.Opera(options = optionsop)
    ##################    
    dfMF = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    waitMF = WebDriverWait(driverMF,tiempoEspera)
    waitMF_name = WebDriverWait(driverMF,tiempoEspera_Nombre)
    waitMF_Ads = WebDriverWait(driverMF,tiempoEspera_Ad)
    waitMF_login = WebDriverWait(driverMF,tiempoEspera_Login)
    driverMF.maximize_window()
    #################
    
    MiIp_MF = host_ip
    print('MF_Mi ip es :', MiIp_MF)
    
    #Iniciamos sesión y nos vamos a YouTube
    driverMF.get('https://accounts.google.com/signin/v2/identifier')
    print('MF_Vamos a iniciar sesion')
    waitMF_login.until(EC.url_changes)
    waitMF_login.until(EC.url_contains('myaccount.google.com'))
    
    driverMF.get("http://www.youtube.com/")
    waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    #time.sleep(sleepTime)
    user_dataMF=driverMF.find_elements_by_xpath('//*[@id="video-title"]')
    print('MF_Extraidos : ', len(user_dataMF), ' vídeos')
    #Obtengo los links de la página principal.
    linksMF = []
    for i in user_dataMF:
        linksMF.append(i.get_attribute('href'))
        
    #Y ahora a extraer los datos de cada link.
    v_navegador_MF = 'Mozilla Firefox'
    v_sesionInit_MF = 'True'
    try:
        v_addPrintipalName_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print('MF_ERROR: anuncio del mainPage')
        v_addPrintipalName_MF='No hay anuncio principal'
        v_addPrintipalLink_MF = 'No hay anuncio principal'
    dfMF.loc[len(dfMF)] = [v_addPrintipalLink_MF, v_addPrintipalName_MF,'0', 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador_MF, v_sesionInit_MF, '0']   
    
    numVideo = 0
    for x in linksMF:    
        driverMF.get(x)
        v_id_MF = x.strip('https://www.youtube.com/watch?v=')
        #waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        #Título
        time.sleep(sleepTime)
        if numVideo == 0:
            try:
                waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"ytd-button-renderer#remind-me-later-button"))).click()
            except:
                print('MF_SS_ERROR : No he podido pulsar el botón de privacidad')
        try:
            v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except :
            print('MF_ERROR : No he podido obtener el título, segundo intento')
            try:
                v_title_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except :
                v_title_MF = 'ERROR'
        if v_title_MF=='' or v_title_MF==None:
            try:
                time.sleep(sleepTime)
                v_title_MF = waitMF_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                print('MF_ERROR : Título')
                v_title_MF = 'ERROR'
        
        #Número de comentarios
        try:
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        except:
            print('MF_ERROR:PAGE DOWN')
        time.sleep(sleepTime)
        try:
            v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
        except:
            time.sleep(sleepTime)
            try:
                v_numComments = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except:
                print('MF_ERROR : No he podido obtener el número de comentarios')
                v_numComments = 'ERROR'
            
        #Categoría    
        try:
            waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
        except:
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            try:
                waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
            except:
                print('MF_ERROR : No puedo pulsar el botón de mostrar más')
        try:    
            v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
        except :
            try:
                v_category_MF = waitMF.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except :
                print('MF_ERROR : Categoría')
                v_category_MF = 'ERROR'   
        
        #Descripción
        try:
            v_description_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
        except:
            print('MF_ERROR : No he podido obtener la descripción')
            v_description_MF = 'ERROR'
        
        #Número de visualizaciones
        try:
            v_numVisualizacioness_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
        except:
            print('MF_ERROR : No he podido obtener el número de visualizaciones')
            v_numVisualizacioness_MF = 'ERROR'
            
        #Fecha
        try:
            v_fecha_MF =  waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
        except :
            print('MF_ERROR : fecha')
            v_fecha_MF = 'ERROR'
        
        #Me gusta/no me gusta
        try:
            v_likes_MF =  waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
        except:
            print('MF_ERROR : Me gusta')
            v_likes_MF='ERROR'
        try:
            v_dislikes_MF =  waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
        except:
            print('MF_Error : NO me gusta')
            v_dislikes_MF='ERROR'
         
        #Nombre del canal
        try:
            v_channel_MF =  waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
        except :
            print('MF_ERROR : No he podido obtener el nombre del canal')
            v_channel_MF = 'ERROR'
        
        #Link del canal
        try:
            v_channelLink_MF = waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
        except :
            print ('No he podido obtener el link del canal')
            v_channelLink_MF='ERROR'
        
        #Num subs
        try:
            v_channelSubs_MF=waitMF.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
        except :
            print('MF_No se han podido obtener el número de subscripciones al canal')
            v_channelSubs_MF='Error'
        
        #Link del anuncio/nombre del anuncio
        try:
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        except:
            print('MF_ERROR:PAGE UP')
        try:
            v_addLink_MF = waitMF_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
        except :
            v_addLink_MF='ERROR'
        if v_addLink_MF != 'ERROR' :
            print('MF_Anuncio : ',v_addLink_MF) 
        
        dfMF.loc[len(dfMF)] = [v_id_MF, v_title_MF, v_category_MF, v_description_MF,v_numComments, v_fecha_MF,v_numVisualizacioness_MF, v_likes_MF, v_dislikes_MF,v_channel_MF , v_channelLink_MF, v_channelSubs_MF, v_navegador_MF, v_sesionInit_MF, v_addLink_MF]   
        numVideo = numVideo +1
        print ('MF_Extraido con sesión iniciada, número : ' , numVideo ,' de ', len(linksMF), ' llamado : ', v_title_MF)
    
    #Cierro el navegador
    driverMF.close()
    print('MF_Finalizado : recoger datos de Mozilla Firefox con sesión iniciada')
    
    #############
    print('MF_Copiando datos al excel')
    frames = [dfMF ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + MiIp_MF+'_MF.csv', encoding='utf-8', index=False)
    print('MF_Extracción de datos con sesión iniciada terminada')
    

    temp = time.time() - start_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('MF_SS_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))
    print('MF_Recuerda, tu ip es : ', MiIp_MF)

print('Iniciando Navegadores Web')

# OtherThread = threading.Thread(target=OtherFunc)
# OtherThread.start()
# OtherThread.join()

ChromeThread = threading.Thread(target=ChromeFunc)
ChromeThread.start()
   
FirefoxThread = threading.Thread(target=FirefoxFunc)
FirefoxThread.start()


FirefoxThread.join()   
ChromeThread.join()

ChromeThread_SS = threading.Thread(target=ChromeFuncNoSesion)
ChromeThread_SS.start() 

FirefoxThread_SS = threading.Thread(target=FirefoxFuncNoSesion())
FirefoxThread_SS.start()  

ChromeThread_SS.join()
FirefoxThread_SS.join()

print('Fin del programa.')

