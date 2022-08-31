from bs4 import BeautifulSoup
import json
import requests

# URL do site
url = 'https://storage.googleapis.com/infosimples-public/commercia/case/product.html'
response = requests.get(url)

# Dic
resposta_final = {}
# Parse do responses
parsed_html = BeautifulSoup(response.content, 'html.parser')

resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()
resposta_final['brand'] = parsed_html.select_one('.brand').get_text()

cate = parsed_html.select('.current-category')
categorias = []

for a in cate:
    if a.select_one('a') != None:
        categorias.append(a.get_text(strip = True).replace(">",';'))


resposta_final['categoria'] = categorias
resposta_final['description'] = parsed_html.select_one('.product-details p').get_text(strip = True)

sku = parsed_html.select('.card-container')


class Pato:
    def __init__(self, name, currentPrice, oldPrice, available):
        self.n = name
        self.cP = currentPrice
        self.oP = oldPrice
        self.a = available


patinhos = []

for div in sku:
    patoObj = Pato(None, None, None, None)

    # try:
    if div.select_one('.sku-name') != None:
        for classe in div.select_one('.sku-name'):
            patoObj.name = classe.strip()
    else:
        patoObj.name = None

    if div.select_one('.sku-current-price') != None:
        for classe in div.select_one('.sku-current-price'):
            patoObj.currentPrice = float(classe.strip()[1:])
    else:
        patoObj.currentPrice = None

    if div.select_one('.sku-old-price') != None:
        for classe in div.select_one('.sku-old-price'):
            patoObj.oldPrice = float(classe.strip()[1:])
    else:
        patoObj.oldPrice = None

    if patoObj.currentPrice == None:
        patoObj.available = False
    else:
        patoObj.available = True

    # except TypeError:
    # pass
    patinhos.append(patoObj)

resposta_final['sku'] = patinhos

props = parsed_html.select('tr')



class Propriedade:
    def __init__(self, label, value):
        self.l = label
        self.v = value


propriedades = []

for tr in props:
    propObj = Propriedade(None, None)

    if tr.select_one('td') != None:
        for dado in tr.select_one('td'):
            propObj.label = dado.get_text()
            tr.select_one('td')
            propObj.value = dado.find_next('td').text.strip()
    else:
        propObj.label = None

    propriedades.append(propObj)

resposta_final['properties'] = propriedades

revs = parsed_html.select('.review-box')


class Review:
    def __init__(self, name, date, score, text):
        self.n = name
        self.d = date
        self.s = score
        self.t = text


reviews = []

for div in revs:
        revObj = Review(None, None, None, None)

        if div.select_one('.review-username') != None:
            for span in div.select_one('.review-username'):
                revObj.name = span.get_text()

        else:
            revObj.name = None

        if div.select_one('.review-date') != None:
            for span in div.select_one('.review-date'):
                revObj.date = span.get_text()

        if div.select_one('.review-stars') != None:
            for span in div.select_one('.review-stars'):
                revObj.score = span.get_text().count('★')

        if div.select_one('p') != None:
            for span in div.select_one('p'):
                revObj.text = span.get_text()
        reviews.append(revObj)

resposta_final['reviews'] = reviews

media = 0
for i in range(len(reviews)):
    media = reviews[i].score + media
media = media/len(reviews)

resposta_final['reviews_average_score'] = media
resposta_final['url'] = url
# ---------------------------------------- JSON Part -----------------------------------

# The customEncoder idea was not mine. For more details: https://linuxpip.org/object-of-type-is-not-json-serializable/
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__

# Serialize it with encoder
json_resposta_final = json.dumps(resposta_final, indent=4, cls=CustomEncoder)
print(json_resposta_final)

# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w') as arquivo_json:
     arquivo_json.write(json_resposta_final)
