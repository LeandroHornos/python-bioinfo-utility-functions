# MIS FUNCIONES
# Funciones generales para tareas cotidianas 
# de procesado de datos bioinformáticos

# DEPENDENCIAS
# ------------
# pandas
# Bio
# python-pptx
# matplotlib

import pandas as pd
from Bio import Entrez
from IPython.display import HTML, display
import os

from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
from io import BytesIO

#------------------------------------------------------------#

def summary(df):
    null_counts = df.isnull().sum()

    # Calcular el número total de valores no nulos en cada columna
    not_null_counts = df.notnull().sum()

    # Obtener los tipos de dato de cada columna
    data_types = df.dtypes

    # Crear un nuevo DataFrame con los números de valores NULL, valores no nulos y tipos de dato
    summary_df = pd.DataFrame({
        'Null_Count': null_counts,
        'Not_Null_Count': not_null_counts,
        'Data_Type': data_types
    })

    # Transponer el DataFrame para que las columnas originales se conviertan en índices de filas
    summary_df = summary_df.T

    # Mostrar el nuevo DataFrame
    return summary_df

#-------------------------------------------------------------#

def file_exists(nombre_archivo, ubicacion):
    ruta_completa = os.path.join(ubicacion, nombre_archivo)
    return os.path.exists(ruta_completa)
    
#-------------------------------------------------------------#

def check_duplicates(df, column):

    # Para contar los valores duplicados en la columna 'Ara':
    duplicates = df[column].value_counts()

    # Filtrar los valores que aparecen al menos dos veces:
    duplicates = duplicates[duplicates > 1]

    # Crear un nuevo DataFrame con los valores y sus recuentos:
    new_df = pd.DataFrame({f'{column}': duplicates.index, 'Counts': duplicates.values})

    # Imprimir el nuevo DataFrame:
    return new_df

#-------------------------------------------------------------#

def compare_row_indexes(df1,df2,df1_name='df_1',df2_name='df_2'):
    # Fusionar los dos DataFrames en función de sus índices
    merged_df = pd.merge(df1, df2, left_index=True, right_index=True, how='outer', indicator=True)

    # Crear las columnas booleanas "df1", "df2" y "both"
    merged_df[df1_name] = (merged_df['_merge'] == 'left_only') | (merged_df['_merge'] == 'both')
    merged_df[df2_name] = (merged_df['_merge'] == 'right_only') | (merged_df['_merge'] == 'both')
    merged_df['both'] = merged_df['_merge'] == 'both'

    # Eliminar la columna de indicador "_merge"
    merged_df.drop(columns=['_merge'], inplace=True)

    return merged_df[[df1_name,df2_name, 'both']]

#-------------------------------------------------------------#

def map_soy_to_ara(df, id_equivalences_df, df_index_id='LOC_ID'):
    print("Version 4")
    try:
        df[df_index_id] = df.index
        df_ara = df.merge(id_equivalences_df, on=df_index_id, how='left')
        # Elimino los genes no mapeados
        genes_before = len(df_ara)
        df_ara = df_ara.dropna()
        mapped_genes = len(df_ara)
        dups = check_duplicates(df_ara, "Ara")
        #Agrupo
        df_ara = df_ara.groupby("Ara", as_index=False).sum(numeric_only=True)
                 
        # Imprimo un reporte
        print(f'Se han mapeado los genes de soja a arabidopisis.\nDel total de {genes_before} genes se mapearon {mapped_genes} (Se eliminó el {(genes_before-mapped_genes)*100/genes_before}% de los genes).\nSe encontraron {len(dups)} genes de arabidopsis que mapean a más de un gen de soja.\nSe sumaron las counts de los genes de soja que mapean a un mismo gen.\nAl combinar los mapeos múltiples quedaron un total de {len(df_ara)} genes')
        
        # Retorno el df mapeado
        return df_ara
    except Exception as e:
        print(f'Ha ocurrido un error y el mapeo no se ha podido efecturar {e}')
        return pd.DataFrame()
    
#-------------------------------------------------------------#

def map_soy_to_glyma2(df, id_equivalences_df, df_index_id='LOC_ID'):
    print("Version 4")
    try:
        df[df_index_id] = df.index
        df_ara = df.merge(id_equivalences_df, on=df_index_id, how='left')
        # Elimino los genes no mapeados
        genes_before = len(df_ara)
        df_ara = df_ara.dropna()
        mapped_genes = len(df_ara)
        dups = check_duplicates(df_ara, "Glyma 2.0")
        #Agrupo
        df_ara = df_ara.groupby("Glyma 2.0", as_index=False).sum(numeric_only=True)
                 
        # Imprimo un reporte
        print(f'Se han mapeado los genes de soja a arabidopisis.\nDel total de {genes_before} genes se mapearon {mapped_genes} (Se eliminó el {(genes_before-mapped_genes)*100/genes_before}% de los genes).\nSe encontraron {len(dups)} genes de arabidopsis que mapean a más de un gen de soja.\nSe sumaron las counts de los genes de soja que mapean a un mismo gen.\nAl combinar los mapeos múltiples quedaron un total de {len(df_ara)} genes')
        
        # Retorno el df mapeado
        return df_ara
    except Exception as e:
        print(f'Ha ocurrido un error y el mapeo no se ha podido efecturar {e}')
        return pd.DataFrame()
#-----------------------------------------------------#


def map_entrez_to_other_id(df, id_equivalences_df, new_id="Glyma 2.0",df_index_id='LOC_ID', drop_unmapped=False, fill_unmapped_with_entrez=False, combine_dups=False):
    print("Version 4")
    try:
        df[df_index_id] = df.index
        df_mapped = df.merge(id_equivalences_df, on=df_index_id, how='left')
        # Elimino los genes no mapeados
        genes_before = len(df_mapped)
        if(drop_unmapped):
            df_mapped = df_mapped.dropna()
        elif (fill_unmapped_with_entrez):
            df_mapped[new_id].fillna(df_mapped[df_index_id], inplace=True)
        mapped_genes = len(df_mapped)
        dups = check_duplicates(df_mapped, new_id)
        if(combine_dups):
            df_mapped = df_mapped.groupby(new_id, as_index=False).sum(numeric_only=True)        
        # Retorno el df mapeado
        return df_mapped
    except Exception as e:
        print(f'Ha ocurrido un error y el mapeo no se ha podido efecturar {e}')
        return pd.DataFrame()
#-----------------------------------------------------#

def combine_entrez_and_glyma2(entrez, glyma2):
    if not isinstance(glyma2, str):
        return entrez
    gene_id = glyma2 if entrez.startswith("LOC") else entrez
    return gene_id

#-----------------------------------------------------#


def get_gene_from_ncbi(gene_name, email='user@email.com', verbose=False, organismo = "Glycine max"):
    # Esta funcion depende de la librería Bio. Importar Entrez como:
    # from Bio import Entrez
    # Es importante definir tu dirección de correo electrónico para usar la API de NCBI
    Entrez.email = email
    # Realizar una búsqueda en NCBI Gene
    query = f"{gene_name}"
    if(not gene_name.upper().startswith("LOC")):
        query = f"{organismo} {gene_name}"
    if verbose:
        print(f'Query: {query}')
    try:
        handle = Entrez.esearch(db="gene", term=query)
        record = Entrez.read(handle)

        # Verificar si se encontraron resultados
        if record["RetMax"] == "0":
            print("No se encontraron resultados para el gen especificado.")
            return ""
        else:
            # Obtener el ID del gen
            gene_id = record["IdList"][0]
            gene_handle = Entrez.efetch(db="gene", id=gene_id, rettype="gb", retmode="text")
            gene_info = gene_handle.read()
            if verbose:
                print(gene_info)
            return gene_info
    except Exception as e:
        msg = f'No se pudo obtener información del gen {gene_name}. Error: {e}'
        print(msg)
        return msg


#-----------------------------------------------------------------------------------------

def get_gene_batch_from_ncbi(gene_list, email, verbose=False, organismo = "Glycine max"  ):
    results = []
    for gene in gene_list:
        res = get_gene_from_ncbi(gene, email, verbose, organismo)
        results.append(res)
    return results


#-----------------------------------------------------------------------------------------

def read_excel_to_dict(file_path, index_col=0):
    # Crear un diccionario para almacenar los dataframes
    dfs = {}
    
    # Leer el archivo Excel
    xls = pd.ExcelFile(file_path)
    
    # Iterar a través de las hojas del archivo Excel
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=index_col)
        dfs[sheet_name] = df
    
    return dfs

# ------------------------------------------------------------------------------------------

def export_dict_to_excel(dfs_dict, file):
    # Crear un escritor de Excel
    with pd.ExcelWriter(file) as writer:
        # Iterar sobre el diccionario y escribir cada DataFrame en una hoja separada
        for hoja, dataframe in dfs_dict.items():
            dataframe.to_excel(writer, sheet_name=hoja, index=False)
    print(f'Se exportaron las tablas al archivo {file}')

# ------------------------------------------------------------------------------------------

def set_background(color):    
    # Permite asignar un color de fondo a una celda de Jupyter Notebook
    script = (
        "var cell = this.closest('.jp-CodeCell');"
        "var editor = cell.querySelector('.jp-Editor');"
        "editor.style.background='{}';"
        "this.parentNode.removeChild(this)"
    ).format(color)
    
    display(HTML('<img src onerror="{}" style="display:none">'.format(script)))
def export_dfs_to_excel_book(df_list, sheetname_list, filename='dataframes.xlsx', path='./', index=True):
    with pd.ExcelWriter(f'{path}/{filename}') as writer:
        for idx, df in enumerate(df_list):
            df.to_excel(writer, sheet_name=sheetname_list[idx], index=index)
    print('Se guardaron las hojas con éxito')
    
 # -------------------------------------------------------------------------------
 
    
def missing_values_percent_df(dataframe):
    '''
    porcentaje_valores_nulos(dataframe) => dataframe.
    Esta función calcula el porcentaje de valores nulos
    en cada columna de un dataframe y devuelve otro
    indicando con los resultados
    '''
    # Calcular el porcentaje de valores nulos por columna
    porcentaje_missing = (dataframe.isnull().mean() * 100).round(2)

    # Crear un nuevo DataFrame con los resultados
    resultado = pd.DataFrame({'Column': porcentaje_missing.index, 'Missing[%]': porcentaje_missing.values})

    return resultado

# ------------------------------------------------------------------------------------

def comparar_columnas(df1, df2):
    # Obtener nombres de columnas de ambos dataframes
    cols_df1 = set(df1.columns)
    cols_df2 = set(df2.columns)
    
    # Crear un dataframe para almacenar los resultados
    resultados = pd.DataFrame(index=sorted(cols_df1.union(cols_df2)))
    
    # Verificar qué columnas están en cada dataframe
    resultados['DF_1'] = resultados.index.isin(cols_df1)
    resultados['DF_2'] = resultados.index.isin(cols_df2)
    
    # Verificar qué columnas están en ambos dataframes
    resultados['BOTH'] = resultados['DF_1'] & resultados['DF_2']
    
    return resultados
        
# ------------------------------------------------------------------------------------
 
def comparar_dos_listas(lista1, lista2, name1='Lista 1', name2='Lista 2'):
    # Obtener valores únicos de las listas combinadas
    valores_unicos = list( set(lista1).union(set(lista2)) )
    
    # Crear un DataFrame para almacenar los resultados
    resultados = pd.DataFrame(index=valores_unicos)
    
    # Verificar qué valores están en cada lista
    resultados[name1] = resultados.index.isin(lista1)
    resultados[name2] = resultados.index.isin(lista2)
    
    # Verificar qué valores están en ambas listas
    resultados['BOTH'] = resultados[name1] & resultados[name2]
    
    return resultados
 
 # ----------------------------------------------------------------------------------

def comparar_varias_listas(listas:list, nombres:list):

    if(len(listas) != len(nombres)):
        print('La longitud de la lista de listas y la lista de nombres deben ser iguales, sin embargo se observaron diferencias')
        return pd.DataFrame # Retorno dataframe vacío.
    
    # Obtener valores únicos de las listas combinadas
    vals = set()
    
    # Eliminar las repeticiones de cada lista
    for lista in listas:
        vals = vals.union( set(lista) )
        
    # Eliminar repeticiones entre listas
    valores_unicos = list( set(vals) )
    
    # Crear un DataFrame para almacenar los resultados
    resultados = pd.DataFrame(index=valores_unicos)
    
    # Verificar qué valores están en cada lista
    for idx, lista in enumerate(listas):
        resultados[nombres[idx]] = resultados.index.isin(lista)
    
    return resultados

# ----------------------------------------------------------------------------------------

def print_dictree(dc:dict, first=True):
    keys = list(dc)
    if( len(keys) == 0 ):
        return
    for key in keys:
        if(first):
            print(f'\n🐼 {key}') if ( type(dc[key]) == pd.core.frame.DataFrame ) else print(f'\n🔑 {key}')
        else:
            print(f'   🐼 {key}') if ( type(dc[key]) == pd.core.frame.DataFrame ) else print(f'   🗝️ {key}')
            
        if( type(dc[key]) == dict ):
            print_dictree(dc[key], first=False)
    return

# --------------------------------------------------------------------------------------------
def reorder_booldf_cols_by_true_count(df):
    # Calcula el número de valores verdaderos en cada columna
    true_counts = df.sum()
    
    # Ordena las columnas por el número de valores verdaderos de mayor a menor
    ordered_columns = true_counts.sort_values(ascending=False).index
    
    # Reordena el DataFrame de acuerdo a las columnas ordenadas
    reordered_df = df[ordered_columns]
    
    return reordered_df