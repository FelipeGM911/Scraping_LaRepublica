import requests
import lxml.html as html
import os
import datetime
HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title" or @class="V_Trends"]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_ABSTRACT = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:

                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                abstract = parsed.xpath(XPATH_ABSTRACT)[0]
                body = parsed.xpath(XPATH_BODY)     
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(abstract)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:     # response.status_code -> atrubuto para obtener codigo de respuesta html
            home = response.content.decode('utf-8') # convierte caracteres espeiales (ñ) para evitar errores
            parsed = html.fromstring(home) #toma el cotenido html(home) y lo convierte a un documento especial para hacer XPHAT
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE) #obtiene la lista de los resultados de aplicar el XPATH_LINK_TO_ARTICLE
           # print(links_to_notices)
            
            today = datetime.date.today().strftime('%d-%m-%y') # guarda en today la fecha en formato D-M-Y
            if not os.path.isdir(today): # os.path.isdir(today) -> pregunta si hay una carpeta con el nombre que almacena la variable today
               os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today) # funcion para extraer la informacion del link


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()