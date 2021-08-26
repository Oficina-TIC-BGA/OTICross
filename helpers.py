import re
import pandas as pd
import numpy as np

def check_root_vars(root):
    """
    Función que crea el diccionario de parametros si no puede acceder a un valor es porque no esta definido
    Input: root del aplicativo
    Output: Diccionario de parámetros
    """
    # intenta crear el diccionario de parametros, en caso de no ser posible significa que hay un valor 
    # que no se definio en la GUI
    try:
        params = {'filenames':root.filename,
                'keys_left' : root.txt_1.strip().split(','), 
                'keys_right' : root.txt_2.strip().split(','),
                'sorting_vars_left' : root.txt_3.strip().split(','),
                'sorting_vars_right' : root.txt_4.strip().split(','),
                'duplicated_action': root.cmbx_1,
                'duplicated_target': root.cmbx_1_c,
                'type': root.cmbx_2
                }
    except:
        print('Hay pasos que no se llenaron!')
        params = {}
    return params    


def load_files(filenames_list):
    """
    Función que carga los dos archivos excel
    Input: La lista con la rutas absolutas de los archivos a leer seleccionadas por el usuario
    Return: Los dos archivos en formato pandas Dataframe
    """
    # TODO: Poder cargar archivos CSV
    try:
        # intentar lectura de archivos - La funcion siempre leera la primera sheet en el cuaderno excel
        print('Cargando archivos ...')
        file_left = pd.read_excel(filenames_list[0])
        file_right = pd.read_excel(filenames_list[1])
        print('Archivos cargados con exitosamente!')
        print('Archivo 1 con {} filas y {} columnas'.format(file_left.shape[0],
                                                            file_left.shape[1]))
        print('Archivo 2 con {} filas y {} columnas'.format(file_right.shape[0],
                                                            file_right.shape[1]))   

        return file_left, file_right                                                                                                     
    except:
        print('No se pudo cargar los archivos, revisar archivos')
        return None, None 

def files_preparation(file_left, file_right, params):
    """
    Función que aplica el preprocesamiento sobre las llaves de cada archivo
    Ordena los Dataframes por las variables indicadas (no se preprocesan variables)
    Elimina duplicados en cada archivo dependiendo de las opciones escogidas

    Input: Los dos archivos dataframes y los parametros con todas las opcines escogidas en la GUI
    Return: Los dos archivos preparados para el cruce
    """
    if isinstance(file_left, pd.DataFrame) and isinstance(file_right, pd.DataFrame): # verificar que los archivos son dataframes
        print('Prepocesamiento de las llaves ...')
        for k_left in params['keys_left']: # iterar sobre todas las keys left para preprocesar
            file_left[k_left] = file_left[k_left].astype(str).str.strip().str.upper() # convertir str y eliminar espacios
            file_left[k_left] = file_left[k_left].apply(lambda x: re.sub('\W+','',x)) # eliminar caracteres especiales

        for k_right in params['keys_right']: # iterar sobre todas las keys right para preprocesar
            file_right[k_right] = file_right[k_right].astype(str).str.strip().str.upper() # convertir str y eliminar espacios
            file_right[k_right] = file_right[k_right].apply(lambda x: re.sub('\W+','',x)) # eliminar caracteres especiales
        
        print('Ordenado de archivos ...') 
        # Para ordenar los archivos, si es una sola variable debe ser diferente al placeholder o a vacio
        # Ser varias variables
        # Archivo left
        if len(params['sorting_vars_left'])>1 or (params['sorting_vars_left'][0] != 'Nombre variables archivo 1' and params['sorting_vars_left'][0] != '') :
            file_left = file_left.sort_values(by=params['sorting_vars_left']) # ordenar dataframe por las var left indicadas x usuario
            print('Archivo 1 ordenado por {}'.format(params['sorting_vars_left']))
        else:
            print('Las variables para ordenar el archivo 1 son erroneas o no se especifican,, se continua sin ordenar')   

        # Archivo right
        if len(params['sorting_vars_right'])>1 or (params['sorting_vars_right'][0] != 'Nombre variables archivo 2' and params['sorting_vars_right'][0] != '') :
            file_right = file_right.sort_values(by=params['sorting_vars_right']) # ordenar dataframe por las var right indicadas x usuario
            print('Archivo 2 ordenado por {}'.format(params['sorting_vars_right']))
        else:
            print('Las variables para ordenar el archivo 2 son erroneas o no se especifican, se continua sin ordenar') 

        print('Eliminando duplicados ...') 
        # diccionario para convertir las opciones seleccionadas en el dropdown a las opciones de pandas duplicated
        dropdown = {
            'Eliminar últimos':'first',
            'Eliminar primeros':'last'
        }

        # Validacion para identificar que registros quiere eliminar además de en cuales archivos quiere eliminarlos
        if params['duplicated_action'] != 'No eliminar':
            if params['duplicated_target'] == 'En ambos archivos':
                print('Se van a {} repetidos en ambos archivos'.format(params['duplicated_action']))
                # Elimina los duplicados basados en la opcion escogida, eliminar ultimo significa mantener los primeros
                file_left = file_left.loc[~file_left[params['keys_left']].duplicated(keep=dropdown[params['duplicated_action']])]
                file_right = file_right.loc[~file_right[params['keys_right']].duplicated(keep=dropdown[params['duplicated_action']])]
                print('Registros duplicados eliminados en ambos archivos')

            elif params['duplicated_target'] == 'Solo en el archivo 1':
                print('Se van a {} repetidos en el archivo 1'.format(params['duplicated_action']))
                file_left = file_left.loc[~file_left[params['keys_left']].duplicated(keep=dropdown[params['duplicated_action']])]
                print('Registros duplicados eliminados en el archivo 1')

            elif params['duplicated_target'] == 'Solo en el archivo 2':
                print('Se van a {} repetidos en el archivo 2'.format(params['duplicated_action']))
                file_right = file_right.loc[~file_right[params['keys_right']].duplicated(keep=dropdown[params['duplicated_action']])]
                print('Registros duplicados eliminados en el archivo 2')

        else:
            # Para la opcion no eliminar
            print('No se elimina repetido de ningún archivo') 

        return file_left, file_right

    else:
        print('Error en los archivos')
        
        return None, None   


def crossing_files(file_left, file_right,params):
    """
    Función que ejecuta el cruce de los archivos preparados segun opciones escogidas por el usuario
    Input: Los dos pandas dataframes preparados y los parametros con las llaves y tipo de cruce
    Return: Archivo resultado del cruce
    """
    # Diccionario para pasar de las opciones de la GUI a las opciones de pandas merge
    dropdown2merge = {
        'Izquierda':'left',
        'Derecha':'right',
        'Interseccion':'inner',
        'Todos':'outer'
        }

    # ejecutar el cruce, si los archivos tiene columnas con el mismo nombre, las columnas del 
    # segundo archivo se les agregar el sufijo '_y'
    # se podria dependiendo de las opciones validar el cruce si es '1:1', '1:m', 'm:1', 'm:m'
    return file_left.merge(file_right, 
                    left_on=params['keys_left'], 
                    right_on=params['keys_right'], 
                    how=dropdown2merge[params['type']],
                    suffixes=('','_y'), 
                    )
    


