def exhanges():
    import requests
    import json

    url = 'https://api.twelvedata.com/exchanges'

    rq=requests.get(url).text
    exchanges=json.loads(rq)
    for e in exchanges['data']:
        e['country']=e['country'] if e['country'] !='United States' else e['country'] + ' of America'
        e['title']=e['title'] if e['country'] !='Canada' or e['title'][:12] != 'NEO Exchange' else e['title'][:12]
        e['title']=e['title'] if e['title'] != 'Deutsche Börse Xetra' else 'Deutsche Boerse XETRA'
        e['title']=e['title'] if e['title'] != 'Indian National Stock Exchange' else 'National Stock Exchange of India'
        e['title']=e['title'] if e['title'] != 'Korea Exchange (KOSDAQ)' else 'KOSDAQ'
        e['title']=e['title'] if e['title'] != 'South Korea Stock Exchange' else 'Korea Stock Exchange'

    with open(f'landing/metadata/exhanges.json','a') as f:
        f.write(json.dumps(exchanges['data'],ensure_ascii=True,indent=4))

def diccionario():
    import requests
    import json
    from bs4 import BeautifulSoup as bs

    url = 'https://lists.gnucash.org/docs/C/gnucash-manual/fq-spec-yahoo.html'

    rq = requests.get(url).text
    soup=str(bs(rq,'html.parser').tbody)
    soup = bs(soup,'html.parser').find_all('p')
    linea, dicc = [], []
    i = 0
    while i < len(soup):
        if i != 0 and i % 4 ==0:
            linea[1] = linea[1] if not (linea[1] == 'London Stock Exchange' and linea[2] == '.L') else linea[1] + ' - AIM MTF'
            dicc.append(
                {
                    'country':linea[0],
                    'title':linea[1],
                    'sufix':linea[2]
                }
            )
            linea=[]
        elemento = str(soup[i]).replace('<p>','').replace('</p>','').strip()
        elemento = elemento.split(' (')[0].replace(' Index','')
        elemento = elemento if elemento != 'Canadian Securities ExchangeToronto Stock Exchange' else 'Canadian National Stock Exchange'
        elemento = elemento if elemento != 'Italian Stock Exchange, former Milano' else 'Italian Stock Exchange'
        linea.append(elemento)
        i+=1

    with open(f'landing/metadata/diccionario.json','a') as f:
        f.write(json.dumps(dicc,ensure_ascii=True,indent=4))

def shuffle():
    import json

    match, sin_match, repetidos, paises=[], [], [], []

    f = open(f'landing/metadata/diccionario.json','r')
    diccionario=json.loads(f.read())
    f = open(f'landing/metadata/exhanges.json','r')
    exhanges=json.loads(f.read())
    f = open(f'landing/metadata/tinkers.json','r')
    stocks=json.loads(f.read())

    for dc in diccionario:
        if dc['country'] not in paises:
            paises.append(dc['country'])
        else:
            repetidos.append(dc['country'])
        for bl in exhanges: 
            if bl['country'] == dc['country'] and bl['title'] == dc['title']:
                match.append(dc)

    for dc in diccionario:
        if dc not in match:
            sin_match.append(dc)

    repetidos=list(set(repetidos))
    catalogo=[]
    for bl in exhanges:
        if bl['country'] == 'United States of America':
            catalogo.append({'country':bl['country'],'title':bl['title'],'name':bl['name'],'code':bl['code'],'sufix':''})
            continue
        for dc in diccionario: 
            if dc['country'] == bl['country']:
                if dc['country'] in repetidos and dc['title'] == bl['title']:
                    catalogo.append({'country':bl['country'],'title':bl['title'],'name':bl['name'],'code':bl['code'],'sufix':dc['sufix']})
                elif dc['country'] not in repetidos:
                    catalogo.append({'country':bl['country'],'title':bl['title'],'name':bl['name'],'code':bl['code'],'sufix':dc['sufix']})

    for ct in catalogo:
        ct['symbols']=[]
        for st in stocks:
            if '.' in st['symbol']:
                continue
            if st['exchange'] == ct['name'] and st['mic_code'] == ct['code']:
                ct['symbols'].append(st['symbol'])
    
    with open(f'landing/metadata/catalogo.json','a') as f:
        f.write(json.dumps(catalogo,ensure_ascii=True,indent=4))

def get_tinker():
    import requests
    import json

    url=f'https://api.twelvedata.com/stocks?exchanges'
    rq=requests.get(url).text
    acciones=json.loads(rq)
    acciones=acciones['data']
    simbolos=[]
    for ac in acciones:
        simbolos.append(ac)

    with open(f'landing/metadata/tinkers.json','a') as f:
        f.write(json.dumps(simbolos,ensure_ascii=True,indent=4))
    return simbolos