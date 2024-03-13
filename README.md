# MIS FUNCIONES

Este repositorio contiene un conjunto de funciones útiles para el procesamiento de datos bioinformáticos en Python.

## Dependencias

Asegúrate de tener instaladas las siguientes bibliotecas antes de utilizar estas funciones:

- pandas
- Bio
- python-pptx
- matplotlib

## Uso en proyectos

**1.** Clonar el repositorio desde github<br>
**2.** Identificar la ruta completa al archivo functions.py en el respositorio clonado<br>
**3.** Editar el archivo ~/.bashrc y agregar la siguiente función (editar la ruta al archivo!):

```bash
    function update_py_functions() {
    if [ -f "functions.py" ]; then
        echo "Ya existe una copia local de functions.py. Sobreescribiendo..."
    fi
    
    cp /full/path/to/functions.py ./functions.py
    
    echo "Archivo functions.py actualizado correctamente."
}

```
**4.** Volver a cargar el archivo .bashrc

```bash
source ~/.bashrc
```

**5.** Para agregar las funciones a un proyecto, desde el nivel superior de la carpeta del proyecto ejecutar en un terminal:

```bash
source ~/.bashrc
update_py_functions
```
Si el archivo no existe se creará una copia, y si existe se actualizará a la última versión.

**6.** Luego se pueden importar las funciones desde un script de python o un jupyter notebook que se encuentren en la misma carpeta (o en un nivel inferior)

```python
from functions import (
    read_excel_to_dict,
    print_dictree,
    reorder_booldf_cols_by_true_count
)
```

## Funciones Disponibles

### 1. `summary(df)`

Esta función genera un resumen de un DataFrame que incluye el recuento de valores nulos, valores no nulos y tipos de datos para cada columna.

### 2. `file_exists(nombre_archivo, ubicacion)`

Verifica si un archivo existe en una ubicación específica.

### 3. `check_duplicates(df, column)`

Encuentra y cuenta los valores duplicados en una columna específica de un DataFrame.

### 4. `compare_row_indexes(df1, df2, df1_name='df_1', df2_name='df_2')`

Compara los índices de dos DataFrames y muestra si un índice está presente en uno, en el otro o en ambos.

### 5. `map_soy_to_ara(df, id_equivalences_df, df_index_id='LOC_ID')`

Mapea los genes de soja a arabidopsis utilizando un DataFrame de equivalencias.

### 6. `map_soy_to_glyma2(df, id_equivalences_df, df_index_id='LOC_ID')`

Mapea los genes de soja a glyma2 utilizando un DataFrame de equivalencias.

### 7. `map_entrez_to_other_id(df, id_equivalences_df, new_id="Glyma 2.0", df_index_id='LOC_ID', drop_unmapped=False, fill_unmapped_with_entrez=False, combine_dups=False)`

Mapea los identificadores Entrez a otros identificadores utilizando un DataFrame de equivalencias.

### 8. `combine_entrez_and_glyma2(entrez, glyma2)`

Combina los identificadores Entrez y glyma2.

### 9. `get_gene_from_ncbi(gene_name, email='user@email.com', verbose=False, organismo='Glycine max')`

Obtiene información sobre un gen de NCBI Gene.

### 10. `get_gene_batch_from_ncbi(gene_list, email, verbose=False, organismo='Glycine max')`

Obtiene información sobre un lote de genes de NCBI Gene.

### 11. `read_excel_to_dict(file_path, index_col=0)`

Lee un archivo Excel y devuelve un diccionario de DataFrames.

### 12. `export_dict_to_excel(dfs_dict, file)`

Exporta un diccionario de DataFrames a un archivo Excel.

### 13. `set_background(color)`

Asigna un color de fondo a una celda de Jupyter Notebook.

### 14. `export_dfs_to_excel_book(df_list, sheetname_list, filename='dataframes.xlsx', path='./', index=True)`

Exporta una lista de DataFrames a un libro de Excel.

### 15. `missing_values_percent_df(dataframe)`

Calcula el porcentaje de valores nulos en cada columna de un DataFrame.

### 16. `comparar_columnas(df1, df2)`

Compara las columnas de dos DataFrames y muestra qué columnas están presentes en cada uno.

### 17. `comparar_dos_listas(lista1, lista2, name1='Lista 1', name2='Lista 2')`

Compara dos listas y muestra qué elementos están presentes en cada una.

### 18. `comparar_varias_listas(listas: list, nombres: list)`

Compara múltiples listas y muestra qué elementos están presentes en cada una.

### 19. `print_dictree(dc: dict, first=True)`

Imprime recursivamente la estructura de un diccionario.

### 20. `reorder_booldf_cols_by_true_count(df)`

Reordena las columnas de un DataFrame booleano por el número de valores verdaderos.

### 21. `calculate_true_percent(df)`

Esta función toma un DataFrame de Pandas que contiene solo valores booleanos y devuelve un nuevo DataFrame con el porcentaje de valores verdaderos en cada columna.

