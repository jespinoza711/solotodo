import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'solonotebooks.settings'

from datetime import datetime
from fetch_scripts import *
from common_fetch_methods import *

'''Main and all-powerful updater script, probably the backbone of the whole
site, it grabs every single model of the stores with fetchers and inserts
them into the database, logging price changes, new models and disappearing
models'''
def main():
    try:
        p = NotebookCenter()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de NotebookCenter')
        logMessage('Error al obtener los notebooks de NotebookCenter')
    try:
        p = PackardBell()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Packard Bell')
        logMessage('Error al obtener los notebooks de Packard Bell')
    try:
        p = Bip()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Bip')
        logMessage('Error al obtener los notebooks de Bip')
    try:
        p = LaPolar()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de La Polar')
        logMessage('Error al obtener los notebooks de La Polar')
    try:
        p = Bym()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Bym')
        logMessage('Error al obtener los notebooks de Bym')
    try:
        p = Clie()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Clie')
        logMessage('Error al obtener los notebooks de Clie')
    try:
        p = ENotebook()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de E-Notebook')
        logMessage('Error al obtener los notebooks de E-Notebook')
    try:
        p = Falabella()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Falabella')
        logMessage('Error al obtener los notebooks de Falabella')
    try:
        p = FullNotebook()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de FullNotebook')
        logMessage('Error al obtener los notebooks de FullNotebook')
    try:
        p = Paris()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Paris')
        logMessage('Error al obtener los notebooks de Paris')
    try:
        p = PCFactory()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de PCFactory')
        logMessage('Error al obtener los notebooks de PCFactory')
    try:
        p = Sym()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Sym')
        logMessage('Error al obtener los notebooks de Sym')
    try:
        p = TecnoCl()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Tecno.cl')
        logMessage('Error al obtener los notebooks de Tecno.cl')
    try:
        p = Wei()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Wei')
        logMessage('Error al obtener los notebooks de Wei')
    try:
        p = Sistemax()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Sistemax')
        logMessage('Error al obtener los notebooks de Sistemax')
    try:
        p = Dell()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Dell')
        logMessage('Error al obtener los notebooks de Dell')
    try:
        p = Webco()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Webco')
        logMessage('Error al obtener los notebooks de Webco')
    try:
        p = Ripley()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Ripley')
        logMessage('Error al obtener los notebooks de Ripley')        
    try:
        p = Racle()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Racle')
        logMessage('Error al obtener los notebooks de Racle')        
    try:
        p = Magens()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Magens')
        logMessage('Error al obtener los notebooks de Magens')
    try:
        p = GlobalMac()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de GlobalMac')
        logMessage('Error al obtener los notebooks de GlobalMac')
    try:
        p = Syd()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de Syd')
        logMessage('Error al obtener los notebooks de Syd')
    try:
        p = MacOnline()
        analyzeStore(p)
    except:
        print('Error al obtener los notebooks de MacOnline')
        logMessage('Error al obtener los notebooks de MacOnline')
                
    updateAvailabilityAndPrice()
                
if __name__ == '__main__':
    print datetime.now()
    main()
    
