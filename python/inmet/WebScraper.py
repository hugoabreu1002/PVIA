from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO
import pandas as pd
from tqdm import tqdm
import pickle

class InmetWS:
    def __init__(self, login='admin', senha='admin'):
        self.list_cidades = ['ACARAU','AGUA BRANCA','ALAGOINHAS','ALTO PARNAIBA','APODI','ARACAJU','ARCOVERDE','AREIA','BACABAL',
                'BALSAS','BARBALHA','BARRA','BARRA DO CORDA','BARREIRAS','BOM JESUS DA LAPA','BOM JESUS DO PIAUI',
                'CABROBO','CAETITE','CALDEIRAO','CAMPINA GRANDE','CAMPOS SALES','CANAVIEIRAS','CARACOL','CARAVELAS',
                'CARINHANHA','CAROLINA','CAXIAS','CEARA MIRIM','CHAPADINHA','CIPO','COLINAS','CORRENTINA','CRATEUS',
                'CRUZ DAS ALMAS','CRUZETA','ESPERANTINA','FEIRA DE SANTANA','FLORANIA','FLORIANO','FORTALEZA',
                'GARANHUNS','GUARAMIRANGA','GUARATINGA','IGUATU','IMPERATRIZ','IRECE','ITABAIANINHA','ITABERABA',
                'ITIRUCU (JAGUAQUARA)','ITUACU','JACOBINA','JAGUARUANA','JOAO PESSOA','LENCOIS',
                'LUZILANDIA(LAG.DO PIAUI)','MACAU','MACEIO','MONTE SANTO','MONTEIRO','MORADA NOVA','MORRO DO CHAPEU',
                'NATAL','OURICURI','PALMEIRA DOS INDIOS','PAO DE ACUCAR','PARNAIBA','PATOS','PAULISTANA',
                'PAULO AFONSO','PETROLINA','PICOS','PIRIPIRI','PORTO DE PEDRAS','PROPRIA','QUIXERAMOBIM',
                'RECIFE (CURADO)','REMANSO','S?O GONCALO','SALVADOR (ONDINA)','SAO JOAO DO PIAUI','SAO LUIS',
                'SENHOR DO BONFIM','SERIDO (CAICO)','SERRINHA','SOBRAL','STa. R. DE CASSIA (IBIPETUBA)','SURUBIM',
                'TAUA','TERESINA','TRIUNFO','TURIACU','VALE DO GURGUEIA (CRISTIANO CASTRO)','VITORIA DA CONQUISTA',
                'ZE DOCA']
        self.login = login
        self.senha = senha
    
    def get_data_from_str(self, string):

        s1 = 'Latitude  (graus) : '
        s1_f = '\nLongitude'
        s2 = 'Longitude (graus) : '
        s2_f = '\nAltitude'
        s3 = 'Altitude  (metros): '

        latitude = string[string.find(s1)+len(s1):string.find(s1_f)]
        longitude = string[string.find(s2)+len(s2):string.find(s2_f)]
        altitude = string[string.find(s3)+len(s3):string.find(s3)+len(s3)+5]

        substring_data = string[string.find('Estacao'):string.find('\n</pre>')]
        TESTDATA = StringIO(substring_data)
        df = pd.read_csv(TESTDATA, sep=";")
        dict_llad = {'Latitude':latitude, 'Longitude':longitude, 'Altitude': altitude, 'Dados':df}

        return dict_llad

    def scrap(self):

        self.lista_dados = []

        for cidade in tqdm(self.list_cidades):
            while True:
                try:
                    #enter the link to the website you want to automate login.
                    website_link="http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php"
                    options = webdriver.ChromeOptions()
                    options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')

                    browser = webdriver.Chrome('chromedriver.exe', options=options)	#for macOS users[for others use chrome vis chromedriver]
                    browser.get(website_link)	

                    browser.find_element_by_name("mCod").send_keys(self.login)	
                    browser.find_element_by_name("mSenha").send_keys(self.senha)
                    browser.find_element_by_xpath('//input[@type="submit" and @value=" Acessar "]').click()
                    browser.implicitly_wait(3)

                    page1 = open('inmet/page1.html','w')
                    page1.write(browser.page_source)
                    page1.close()

                    #--------------------------------------------------------------------#

                    browser.find_element_by_xpath('//a[@href="form_mapas_mensal.php"]').click()
                    browser.implicitly_wait(3)

                    page2 = open('inmet/page2.html','w')
                    page2.write(browser.page_source)
                    page2.close()

                    #--------------------------------------------------------------------#

                    browser.find_element_by_xpath('//input[@name="mRelDtInicio"]').send_keys('01/01/1999')
                    browser.find_element_by_xpath('//input[@name="mRelDtFim"]').send_keys('31/12/2015')
                    browser.find_element_by_xpath('//select[@name="mRelRegiao"]/option[text()="Nordeste"]').click()

                    for i in range(2, 18):
                        browser.find_element_by_xpath('//input[@name="mOpcaoAtribX"]'.replace("X",str(i))).click()

                    browser.find_element_by_xpath('//input[@name="btnProcesso1"]').click()
                    browser.switch_to.alert.accept()
                    browser.implicitly_wait(3) 

                    page3 = open('inmet/page3.html','w')
                    page3.write(browser.page_source)
                    page3.close()

                    #--------------------------------------------------------------------#

                    browser.find_element_by_link_text('_'.replace('_', cidade)).click()

                    page4 = open('inmet/page4.html','w')
                    page4.write(browser.page_source)
                    page4.close()

                    #-------------------------------------------------------------------#

                    browser.find_element_by_xpath('//img[@alt="Dados"]').click()

                    window_after = browser.window_handles[1]
                    browser.switch_to.window(window_after)

                    page5 = open('inmet/page5.html','w')
                    page5.write(browser.page_source)
                    page5.close()

                    str_browser_dados = browser.page_source
                except:
                    continue
                break
            
        #--------------------------------------------------------------------#
            self.lista_dados.append(self.get_data_from_str(str_browser_dados))

        pickle.dump(self.lista_dados, open("lista_dados.pckl", "wb" ))