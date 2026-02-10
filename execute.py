import funciones as sa
import yfinance as yf
import json
import contextlib
import io
import os

# Set directory
if not os.path.isdir('landing'):
    os.makedirs('landing')
    for name in ('historical','metadata'):
        os.makedirs(f'landing/{name}')

sa.exchanges()
sa.diccionario()
sa.get_tinker()
sa.shuffle()

f = open(f'landing/metadata/catalogo.json','r')
catalogo=json.loads(f.read())

for ct in catalogo:
    # We set a break to avoid a complete but heavy load
    if ct['country'] == 'Austria':
        break
    os.makedirs(f'landing/historical/{ct['country']}',exist_ok=True)
    sf=ct['sufix']
    failed=0
    i=0

    # We set a limit to avoid a complete but heavy load
    while i < 20:
        buffer=io.StringIO()
        ac=ct['symbols'][i]

        with contextlib.redirect_stdout(buffer),contextlib.redirect_stderr(buffer):

            tc = yf.download(ac+sf,start='1900-01-01')
            ct['symbols'][i]=[ac,tc.info]

            historial=tc.to_csv(path_or_buf=f'landing/historical/{ct['country']}/{ac}.csv',sep=';',index=True)

        msj=buffer.getvalue()
        if 'Failed download' in msj:
            if failed == 0:
                print('Failed download')
            failed=failed+1
            print(ac)

        i=i+1