import streamlit as st
import numpy as np
import pandas as pd

def leer_estructura(file):
    return pd.read_excel(
        file,dtype={
            'Competencia':str,
            'Tema':str,
            'SubTema':str
        }
    )

def leer_respuestas(archivo,estructura,idlen=5):
    nitems = estructura.shape[0]
    cols = list(estructura['CodPregunta OCA'])
    df = pd.read_fwf(
        archivo,
        header=None,
        dtype=str,
        encoding='iso-8859-1',
        names= ['line'],
        widths= [idlen+nitems]
    )
    df['EXAMEN'] = df['line'].str[:5]
    df['line'] = df['line'].str[5:]
    df = df.set_index('EXAMEN').apply(lambda x: pd.Series(list(x['line'])),axis=1)
    df.columns = cols
    return df.fillna(' ')

def reordenar_claves(dat,est):
    orden = est.set_index('CodPregunta OCA')['Orden Alternativas']
    orden = orden.str[1:-1].str.split(' ',expand=True).T
    orden = orden.applymap(lambda x: chr(64+int(x)))
    vals = ['A','B','C','D']
    orden.index = vals
    res = dat.apply(lambda x: x.apply(lambda y: orden[x.name][y] if y in vals else y))
    return res

def main():
    st.title('Consolidar archivos')
    archivos_lec = st.file_uploader('Archivos de lectura',accept_multiple_files=True)
    versiones = []
    if archivos_lec:
        for arch in archivos_lec:
            version = {}
            version['lectura'] = arch
            version['estructura'] = st.file_uploader(f'Estructura para {arch.name}')
            if version['estructura']:
                versiones.append(version)
        ordenar_columnas = st.checkbox("Ordenar las columnas alfabeticamente")
    if archivos_lec and (len(versiones) == len(archivos_lec)):
        l = []
        for version in versiones:
            est = leer_estructura(version['estructura'])
            dat = leer_respuestas(version['lectura'],est)
            reord = reordenar_claves(dat,est)
            l.append(reord)
        res = pd.concat(l)
        if ordenar_columnas:
            res = res.sort_index(axis=1)
        st.write(res)
main()