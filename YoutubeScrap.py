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
################################################################################################################
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
start_time = time.time()

WithProxy=0 # WithProxy = 1;
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
################################################################################################################

#definicion de funciones
################################################################################################################
def youtubeBrowser(BrowserSelector, WithSesion):
    ##Iniciamos GOOGLE CHROME o MOZILLA FIREFOX, la cabecera del dataFrame y
    #la función de espera para cada parámetro, además de decidir si iniciamos o no sesión
    if BrowserSelector == "Chrome" :
        prefix = "GC_"
        print(prefix,'Iniciando Chrome')
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        if WithProxy==1 :
            driver = webdriver.Chrome(desired_capabilities=caps, proxy=proxy)
        if WithProxy==0 :
            driver = webdriver.Chrome(desired_capabilities=caps)
        v_navegador = 'Google Chrome'
    else:
        prefix = "MF_"
        print(prefix,'Iniciando Firefox')
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "normal"
        if WithProxy==1 :
            driver = webdriver.Firefox(desired_capabilities=caps,  proxy=proxy)
        if WithProxy == 0 :
                driver = webdriver.Firefox(desired_capabilities=caps)
        v_navegador = 'Mozilla Firefox'

    wait = WebDriverWait(driver,tiempoEspera)
    wait_name = WebDriverWait(driver,tiempoEspera_Nombre)
    wait_Ads = WebDriverWait(driver,tiempoEspera_Ad)
    wait_login = WebDriverWait(driver,tiempoEspera_Login)
    df = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción','Num comentarios', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
    driver.maximize_window()
    MiIp=host_ip

    if WithSesion == True :
        #Iniciamos sesión y nos vamos a YouTube
        driver.get('https://accounts.google.com/signin/v2/identifier')
        print(prefix,'Vamos a iniciar sesion')
        wait_login.until(EC.url_changes)
        wait_login.until(EC.url_contains('myaccount.google.com'))
        v_sesionInit = 'True'
    else:
        v_sesionInit = 'False'
        prefix = prefix + 'SS_'

    #Obtengo los links de cada vídeo que he conseguido del mainPage.
    user_data = getMainVideos(driver, wait)
    links = getLinks(user_data, prefix)
    for i in user_data:
        try:
            links.append(i.get_attribute('href'))
        except:
            print(prefix , 'EEROR : Link ERROR')

        #Y ahora a extraer los datos de cada link.

    #Trato de obtener el anuncio del mainPage.
    try:
        v_addPrintipalName = wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
        v_addPrintipalLink = wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
    except:
        print(prefix,'No se ha obtenido anuncio del mainPage')
        v_addPrintipalName='No hay anuncio principal'
        v_addPrintipalLink = 'No hay anuncio principal'
    df.loc[len(df)] = [v_addPrintipalLink, v_addPrintipalName,MiIp, 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0','0', v_navegador, v_sesionInit, '0']

    #Recorro link a link extrayendo los datos.
    numVideo = 0
    for x in links:
        driver.get(x)
        v_id = x.strip('https://www.youtube.com/watch?v=')
        #Datos del vídeo
        v_title =getTitle(wait_name,wait)
        v_numComments = getNumComments(wait, prefix)
        v_category = getCategory(wait, prefix)
        v_description=getDescription(wait, prefix)
        v_numVisualizacioness = getNumVis(wait, prefix)
        v_fecha = getDate(wait, wait_Ads, prefix)
        v_likes = getLikes(wait, prefix)
        v_dislikes=getDislikes(wait, prefix)
        #Datos del canal
        v_channel=getChannelName(wait, wait_Ads, prefix)
        v_channelLink=getChannelLink(wait, prefix)
        v_channelSubs=getChannelSub(wait, prefix)
        #Anuncio
        v_adLink=getAdLink(wait, wait_Ads, prefix)

        df.loc[len(df)] = [v_id, v_title, v_category, v_description,v_numComments, v_fecha,v_numVisualizacioness, v_likes, v_dislikes,v_channel , v_channelLink, v_channelSubs, v_navegador, v_sesionInit, v_adLink]

        numVideo = numVideo +1
        print (prefix,'Extraido vídeo ' , numVideo ,' de ', len(links), ' llamado : ', v_title)

    #Cierro el navegador
    driver.close()
    print(prefix,'Finalizado : recoger datos')
    #############
    print(prefix,'Iniciando : Copia de datos al excel')
    frames = [df ]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)


    df_copy.to_csv(r'C:\Users\YoutubeProject\eclipse-workspace\YoutubePython\src\Datos\Datos_' + prefix + MiIp + '.csv', encoding='utf-8', index=False)
    print(prefix,'Finalizado : Copia de datos al excel')

    #Calculate elapsed time
    printElapsedTieme(start_time, prefix)

def printElapsedTieme(started_time, prefix):
    temp = time.time() - started_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print(prefix,'SS_Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))

def getMainVideos(driver, wait):
    driver.get("http://www.youtube.com/")
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
    except:
        time.sleep(sleepTime)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))
            driver.find_elements_by_xpath('//*[@id="video-title"]')
        except:
            time.sleep(sleepTime)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#video-title')))

    return driver.find_elements_by_xpath('//*[@id="video-title"]')
    #Obtengo los links de la página principal.

def getLinks(user_data, prefix):
    links = []
    for i in user_data:
        try:
            links.append(i.get_attribute('href'))
        except:
            print(prefix , 'EEROR : Link ERROR')
    return links

def getTitle(wait_name,wait):
    #Título
    try:
        v_title = wait_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
    except:
        try:
            time.sleep(sleepTime)
            v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except:
            try:
                time.sleep(sleepTime)
                v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                v_title = 'ERROR'

    if v_title==None or v_title=='':
        try:
            time.sleep(sleepTime)
            v_title = wait_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except:
            try:
                time.sleep(sleepTime)
                v_title = wait_name.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            except:
                v_title = 'ERROR'
        return v_title

def getNumComments(wait, prefix):
    try:
        v_numComments = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
    except:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            time.sleep(sleepTime)
            v_numComments = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
        except:

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
                time.sleep(sleepTime)
                v_numComments = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer"))).text
            except:
                print(prefix,'ERROR : No he podido obtener el número de comentarios')
                v_numComments = 'ERROR'
    return v_numComments

def getCategory(wait, prefix):
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
    except:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
        except:
            print(prefix,'ERROR : Boton ver más')
    try:
        v_category = wait.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
    except:
        time.sleep(sleepTime)
        try:
            v_category = wait.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
        except:
            time.sleep(sleepTime)
            try:
                v_category = wait.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
            except:
                print(prefix,'ERROR : No he podido obtener la categoría')
                v_category = 'ERROR'
    return v_category

def getChannelName(wait, wait_Ads, prefix):
    try:
        v_channel =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_channel =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
        except:
            print(prefix,'ERROR : Nombre del canal')
            v_channel = 'ERROR'
    try:
        wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    except:
        print(prefix,'ERROR : PAGE UP')
    ##RESETEO A POSICION DE ARRIBA
    return v_channel

def getChannelLink(wait, prefix):
    try:
        v_channelLink = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
    except :
        print ('ERROR : link del canal')
        v_channelLink='ERROR'
    return v_channelLink

def getChannelSub(wait, prefix):
    try:
        v_channelSubs=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
    except :
        print(prefix,'ERROR :  número de subscripciones al canal')
        v_channelSubs='Error'

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    except:
        print(prefix,"ERROR : subir página")
    return v_channelSubs

def getAdLink(wait, wait_Ads, prefix):
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    except:
        print(prefix,'ERROR:Page up')
    try:
        v_addLink = wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
    except :
        v_addLink='ERROR'

    if v_addLink != 'ERROR' :
        print(prefix,'Anuncio : ',v_addLink)
    return v_addLink

def getLikes(wait, prefix):
    try:
        v_likes =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_likes =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
        except:
            print(prefix,'ERROR : me gusta')
            v_likes='ERROR'
    return v_likes

def getDislikes(wait, prefix):
    try:
        v_dislikes =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_dislikes =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
        except:
            print(prefix,'ERROR : me gusta')
            v_dislikes='ERROR'
    return v_dislikes

def getDate(wait, wait_Ads, prefix):
    try:
        v_fecha =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_fecha =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
        except:
            print(prefix,'ERROR : la fecha')
            v_fecha = 'ERROR'

    try:
        wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        wait_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    except:
        print(prefix,"ERROR : subir página")
    return v_fecha

def getNumVis(wait, prefix):
    #Número de visualizaciones
    try:
        v_numVisualizacioness = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
            v_numVisualizacioness = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
        except:
            print(prefix,'ERROR : número de visualizaciones')
            v_numVisualizacioness = 'ERROR'
    ##RESETEO A POSICION DE ARRIBA
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    except:
        print(prefix,"ERROR : subir página")
    return v_numVisualizacioness

def getDescription(wait, prefix):
    try:
        v_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
    except:
        print(prefix,'ERROR : descripción')
        v_description = 'ERROR'
    return v_description
################################################################################################################

#mainCode
################################################################################################################

print('Iniciando...')
print("IP del dispositivo : ",host_ip)

ChromeThread = threading.Thread(target=youtubeBrowser, args=("Chrome", True,))
FirefoxThread = threading.Thread(target=youtubeBrowser, args=("Firefox", True,))
FirefoxThread.start()
ChromeThread.start()


FirefoxThread.join()
ChromeThread.join()

ChromeThread_SS = threading.Thread(target=youtubeBrowser, args=("Chrome", False,))
ChromeThread_SS.start()

FirefoxThread_SS = threading.Thread(target=youtubeBrowser, args=("Firefox", False,))
FirefoxThread_SS.start()

ChromeThread_SS.join()
FirefoxThread_SS.join()

print('Fin del programa.')
################################################################################################################
