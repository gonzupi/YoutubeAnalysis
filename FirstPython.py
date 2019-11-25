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
from selenium.common.exceptions import TimeoutException as timeoutSelenium
import sys
from _ast import Try

##Iniciamos GOOGLE CHROME, la cabecera del dataFrame y la función de espera para cada parámetro.
driverGC = webdriver.Chrome()
dfGC = pd.DataFrame(columns = ['Link', 'Título','Categoría, si tiene', 'Descripción', 'Numero visualizaciones','Fecha', 'Me gusta', 'No me gusta','Canal', 'Link del canal', 'Num suscripciones','Navegador', 'Sesion iniciada', 'Anuncio si lo hay'])
waitGC = WebDriverWait(driverGC,8)
waitGC_Ads = WebDriverWait(driverGC,2)
waitGC_login = WebDriverWait(driverGC,2000)
#################
#Iniciamos sesión y nos vamos a YouTube
driverGC.maximize_window()
driverGC.get('https://accounts.google.com/signin/v2/identifier')
print('Vamos a iniciar sesion')
waitGC_login.until(EC.url_changes)
waitGC_login.until(EC.url_contains('myaccount.google.com'))
driverGC.get("http://www.youtube.com/")
user_dataGC = driverGC.find_elements_by_xpath('//*[@id="video-title"]')

#Obtengo los links de la página principal.
linksGC = []
for i in user_dataGC:
    linksGC.append(i.get_attribute('href'))
    
#Y ahora a extraer los datos de cada link.
v_navegador = 'Google Chrome'
v_sesionInit = 'True'
try:
    v_addPrintipalName_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer.complex-string a"))).text
    v_addPrintipalLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string.style-scope.ytd-video-masthead-ad-advertiser-info-renderer a"))).get_attribute('href')
except timeoutSelenium as e:
    print('No se ha obtenido anuncio del mainPage')
    v_addPrintipalName_GC='No hay anuncio principal'
    v_addPrintipalLink_GC = 'No hay anuncio principal'
dfGC.loc[len(dfGC)] = [v_addPrintipalLink_GC, v_addPrintipalName_GC,'0', 'ANUNCIO PAGINA PRINCIPAL','0','0','0','0','0','0','0', v_navegador, v_sesionInit, '0']   

numVideo = 0
for x in linksGC:    
    driverGC.get(x)
    v_id_GC = x.strip('https://www.youtube.com/watch?v=')
    
    #Título
    try:
        v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string.ytd-video-primary-info-renderer"))).text
    except timeoutSelenium as e:
        print('ERROR : No he podido obtener el título, segundo intento')
        try:
            v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except timeoutSelenium as e2:
            print('No ha funcionado el segundo intento')
            v_title_GC = 'ERROR'
    if v_title_GC=='' or v_title_GC==' ':
        try:
            print('Problemillas con el nombre, second try')
            v_title_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        except timeoutSelenium as e2:
            print('No ha funcionado el último intento')
            v_title_GC = 'ERROR'
    
    #Categoría
    
    try:
        waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"paper-button#more"))).click()
        print('Intento pulsar el botón de mostrar mas')
    except:
        print('No puedo pulsar el botón')
    try:    
        v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]/parent::h4/parent::ytd-metadata-row-renderer/div[@id='content']/yt-formatted-string/a"))).text
    except timeoutSelenium as e:
        print('ERROR : No he podido obtener la categoría, mostrar más?')
        try:
            v_category_GC = waitGC.until(EC.presence_of_element_located((By.XPATH,"//h4[@id='title']/yt-formatted-string[text()[contains(.,'Categoría')]]"))).text
        except timeoutSelenium as err:
            print('No lo he conseguido')
            v_category_GC = 'ERROR'   
    print(v_category_GC)
    #Descripción
    try:
        v_description_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
    except timeoutSelenium as e:
        print('ERROR : No he podido obtener la descripción')
        v_description_GC = 'ERROR'
    
    #Número de visualizaciones
    try:
        v_numVisualizacioness_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
    except timeoutSelenium as e:
        print('ERROR : No he podido obtener el número de visualizaciones')
        v_numVisualizacioness_GC = 'ERROR'
    
    #Fecha
    try:
        v_fecha_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
    except timeoutSelenium as e:
        print('No se pudo obtener la fecha')
        v_fecha_GC = 'ERROR'
    
    #Me gusta/no me gusta
    try:
        v_likes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label^='Me gusta']"))).text
    except timeoutSelenium as e:
        print('No se pudo obtener el número de me gusta')
        v_likes_GC='ERROR'
    try:
        v_dislikes_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#text[aria-label$='No me gusta']"))).text
    except timeoutSelenium as e:
        print('No se pudo obtener el número de NO me gusta')
        v_dislikes_GC='ERROR'
     
    #Nombre del canal
    try:
        v_channel_GC =  waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string a.yt-formatted-string"))).text
    except timeoutSelenium as e:
        print('ERROR : No he podido obtener el nombre del canal')
        v_channel_GC = 'ERROR'
    
    #Link del canal
    try:
        v_channelLink_GC = waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#text-container.style-scope.ytd-channel-name yt-formatted-string#text a"))).get_attribute('href')
    except timeoutSelenium as e :
        print ('No he podido obtener el link del canal')
        v_channelLink_GC='ERROR'
    
    #Num subs
    try:
        v_channelSubs_GC=waitGC.until(EC.presence_of_element_located((By.CSS_SELECTOR,"yt-formatted-string#owner-sub-count"))).text
    except timeoutSelenium as e:
        print('No se han podido obtener el número de subscripciones al canal')
        v_channelSubs_GC='Error'
    
    #Link del anuncio/nombre del anuncio
    try:
        v_addLink_GC = waitGC_Ads.until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[id^='visit-advertiser'] span.ytp-ad-button-text"))).text
    except timeoutSelenium as e :
        print('Intento de extraer anuncio fallido')
        v_addLink_GC='Error'
    print('Anuncio : ',v_addLink_GC)
    
    dfGC.loc[len(dfGC)] = [v_id_GC, v_title_GC, v_category_GC, v_description_GC, v_fecha_GC,v_numVisualizacioness_GC, v_likes_GC, v_dislikes_GC,v_channel_GC , v_channelLink_GC, v_channelSubs_GC, v_navegador, v_sesionInit, v_addLink_GC]   
    numVideo = numVideo +1
    print ('Extraido con sesión iniciada, número : ' , numVideo ,' de ', len(linksGC), ' llamado : ', v_title_GC)
#Cierro el navegador
driverGC.close()
print('Finalizado : recoger datos de google Chrome con sesión iniciada, ahora a iniciar sesión')

#############
print('Copiando datos al excel')
frames = [dfGC ]
df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
          keys=None, levels=None, names=None, verify_integrity=False,
          copy=True)
df_copy.to_csv('df_GC.csv', encoding='utf-8', index=False)
print('Extracción de datos con sesión iniciada terminada')
