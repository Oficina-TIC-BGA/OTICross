#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jefferson Rodríguez - Oficina TIC Bucaramanga

############ importar librerias #########################
import os
import re
import sys
import time

from numpy import result_type
import helpers
import warnings
import xlsxwriter
import unicodedata
import pandas as pd
import tkinter as tk
from tkinter import ttk
from codecs import decode
from functools import partial
from tkinter import filedialog
warnings.filterwarnings('ignore')

def main():
    """
    Main function: Ejecuta todo el aplicativo 
    Esta función es la que se empaqueta para crear el ejecutable win
    """
    def create_initial_gui():
        """
        Inicializar GUI 
        """
        def open_files():
            """
            Función que selecciona los archivos excel y almacena la ruta de los
            archivos en el objeto root del aplicativo
            Input: Ninguno, recibe el objeto root como variable global
            Output: No se retorna nada pero si se almacena los direcciones en el objeto root
            """
            # función para abrir el cuadro de dialogo y seleccionar varios archivos de tipo excel
            root.filename = filedialog.askopenfilenames(
                                            initialdir = '/',
                                            title = 'Seleccione los archivos',
                                            filetypes=(("xlsx files","*.xlsx"),("all files","*.*")))
            if len(root.filename)>0:
                tk.Label(root, text='Archivos seleccionados').place(x=320,y=70)
                tk.Label(root, text='Primer archivo {}'.format(root.filename[0])).place(x=320,y=90)
                tk.Label(root, text='Segundo archivo {}'.format(root.filename[1])).place(x=320,y=110)
            else:
                tk.Label(root, text='No se han cargado archivos').place(x=520,y=70)

        def clear_entry(event, entry, name):
            """
            Función que se ejecuta como evento sobre los cuadros de texto
            Cada vez que le de click sobre el cuadro, se elimina el placeholder 
            Input: El nombre (name) del evento, el objeto cuadro Texto a limpiar  (entry)
            """
            # el 0 indica que se borre desde el caracter con posición 0 hasta el final (tk.END)
            entry.delete(0, tk.END)
            # unbind es una funcion para manejar eventos
            entry.unbind(name)   

        def callback1(eventObject):
            """
            Función que captura el valor del objeto desplegable (eliminar duplicados) cada vez que se selecciona un valor.
            Este valor se almacena en la variable root para ser usado despues.
            Input: Objeto en el que se aplica el evento
            """
            # Del evento se captura el valor y se almacena en la variable root
            root.cmbx_1 =  eventObject.widget.get()

        def callback1c(eventObject):
            """
            Función que captura el valor del objeto desplegable (archivos donde se eliminaran) cada vez que se selecciona un valor.
            Este valor se almacena en la variable root para ser usado despues.
            Input: Objeto en el que se aplica el evento
            """
            # Del evento se captura el valor y se almacena en la variable root
            root.cmbx_1_c =  eventObject.widget.get()            

        def callback2(eventObject):
            """
            Función que captura el valor del objeto desplegable (tipo de cruce) cada vez que se selecciona un valor.
            Este valor se almacena en la variable root para ser usado despues.
            Input: Objeto en el que se aplica el evento
            """
            # Del evento se captura el valor y se almacena en la variable root
            root.cmbx_2 =  eventObject.widget.get()  

        def callback3(var):
            """
            Función que toma el valor de la variable texto (llaves archivo 1) y la almacena en el root 
            cada vez que se escribe algo en el texto.
            Input: variable de texto
            """
            # Se obtiene el texto de la variable cada vez que se ingresa un valor
            root.txt_1 = var.get()

        def callback4(var):
            """
            Función que toma el valor de la variable texto (llaves archivo 2) y la almacena en el root 
            cada vez que se escribe algo en el texto.
            Input: variable de texto            
            """
            # Se obtiene el texto de la variable cada vez que se ingresa un valor
            root.txt_2 = var.get()   

        def callback5(var):
            """
            Función que toma el valor de la variable texto (llaves a ordenar archivo 1) y la almacena en el root 
            cada vez que se escribe algo en el texto.
            Input: variable de texto              
            """
            # Se obtiene el texto de la variable cada vez que se ingresa un valor
            root.txt_3 = var.get()

        def callback6(var):
            """
            Función que toma el valor de la variable texto (llaves a ordenar archivo 2) y la almacena en el root 
            cada vez que se escribe algo en el texto.
            Input: variable de texto             
            """
            # Se obtiene el texto de la variable cada vez que se ingresa un valor
            root.txt_4 = var.get() 

        def callbacksep(var):
            """
            Función que toma el valor de la variable texto (llaves archivo 2) y la almacena en el root 
            cada vez que se escribe algo en el texto.
            Input: variable de texto            
            """
            # Se obtiene el texto de la variable cada vez que se ingresa un valor
            root.txt_sep = var.get()             

        def exe():
            """
            Función que ejecuta todo el programa 
            """
            print('El programa se esta ejecutando ..')
            lbl_7['text'] = 'El programa se esta ejecutando ..'
            # verificar que todas las variables se puedan acceder y crear el 
            # diccionario de parametros globalmente
            lbl_8 = tk.Label(root, text='1. Verificando variables ..')
            lbl_8.place(x=540,y=340)
            params = helpers.check_root_vars(root)
            if len(params)!=0:
                # ejecutar operaciones con pandas 
                # 1. Cargar archivos
                print('Cargando archivos')
                lbl_9 = tk.Label(root, text='2. Cargando archivos')
                lbl_9.place(x=540,y=360)
                file_left, file_right = helpers.load_files(root) 
                print('Archivos cargados exitosamente')
                lbl_10 = tk.Label(root, text='Archivos cargados exitosamente!')
                lbl_10.place(x=540,y=380)
                lbl_11 = tk.Label(root, text='Archivo 1 con {} filas y {} columnas'.format(file_left.shape[0],
                                                            file_left.shape[1]))
                lbl_11.place(x=540,y=400)
                lbl_12 = tk.Label(root, text='Archivo 2 con {} filas y {} columnas'.format(file_right.shape[0],
                                                            file_right.shape[1])) 
                lbl_12.place(x=540,y=420)                                            
                # 2. limpieza y preparación de archivos
                print('Limpiando y preparando archivos')
                lbl_13 = tk.Label(root, text='3. Limpiando y preparando archivos')
                lbl_13.place(x=540,y=440)
                file_left, file_right = helpers.files_preparation(file_left, file_right, params)
                # 3. Cruzar los archivos
                print('Cruzando archivos')
                lbl_14 = tk.Label(root, text='4. Cruzando archivos')
                lbl_14.place(x=540,y=460)
                result = helpers.crossing_files(file_left, file_right, params)
                # 4. almacenar el resultado como excel
                # TODO: habilitar la opción de almacenar csv 
                # se crea el path tomando la direccion base de uno de los archivos y agregando el nombre del resultado
                path = root.filename[0].split('/')[:-1]
                # se usa xlsxwriter porque es más eficiente para crear excel grandes
                print('Almacenando el resultado')
                lbl_15 = tk.Label(root, text='5. Se esta almacenando el resultado en {}'.format('/'.join(path+['resultado_cruce.xlsx'])))
                lbl_15.place(x=540,y=480)

                # guardar excel si es muy grande se guarada csv
                if result.shape[0]>1000000:
                    result.to_csv('/'.join(path+['resultado_cruce.xlsx']) ,index=False,)
                else:
                    result.to_excel('/'.join(path+['resultado_cruce.xlsx']) ,index=False, engine='xlsxwriter')
                     
                lbl_16 = tk.Label(root, text='El archivo resultante tiene {} filas y {} columnas'.format(result.shape[0], result.shape[1]))
                lbl_16.place(x=540,y=500)
                print('Proceso finalizado')
            else:
                print('Aplicación no procesada, seleccione todos los valores correctamente en cada paso')                          

        # GUI
        root.state('zoomed') # Para agrandar toda la pantalla
        root.title('OTICross - Oficina TIC Alcaldía de Bucaramanga') # Para poner titulo en el banner
        # definir variables por defecto
        root.cmbx_1 = 'No eliminar' # accion de eliminados a ejecutar por defecto
        root.cmbx_1_c = 'En ambos archivos' # target de archivo para aplicar la función por defecto
        root.cmbx_2 = 'Izquierda' # tipo de cruce por defecto
        root.txt_sep = ',' 

        # Seleccionar el tipo de separador para los archivo csv o txt en caso de seleccionarlos
        txt_var_sep = tk.StringVar()
        txt_var_sep.trace("w", lambda name, index,mode, var=txt_var_sep: callbacksep(txt_var_sep))
        txt_entry_key_sep = tk.Entry(root, width=20,textvariable=txt_var_sep)
        txt_entry_key_sep.place(x=520,y=45)
        txt_entry_key_sep.insert(0,'Separador para txt, csv')
        txt_entry_key_sep.bind("<Button-1>", lambda event: clear_entry(event, txt_entry_key_sep, "<Button-1>"))

        # cargar archivos
        greet = tk.Label(root, text='Aplicativo para cruzar archivos excel',
                         font=("Verdana", 18)).pack() # Para poner el titulo dentro de la GUI
        btn_open = tk.Button(root, text='Cargar archivos', command=open_files, 
                             font=("Verdana", 12)) # Boton que permite seleccionar los archivos
        btn_open.place(x=660,y=40)
        lbl_2 = tk.Label(root,text='Paso 1 - Cargar archivos:',font=("Verdana", 14))
        lbl_2.place(x=260,y=40)   

        # TODO: Modularizar la creación de cuadro de texto para reusar código                                               
        ## cuadro de texto para colocar el nombre de las keys
        # Cuadro de texto de la izquierda
        txt_var_1 = tk.StringVar() # se crea la variable texto a ir en el objeto cuadro de texto
        # Se hace siguiente a la variable de escritura  y se ejecuta el callback para capturar su valor cada vez que cambie
        txt_var_1.trace("w", lambda name, index,mode, var=txt_var_1: callback3(txt_var_1)) 
        txt_entry_key_1 = tk.Entry(root, width=30, textvariable=txt_var_1) #se crea el campo de texto y se le asigna esa var texto
        txt_entry_key_1.place(x=500,y=150) # posiciona el objeto 
        txt_entry_key_1.insert(0,'Nombre llaves archivo 1') # Se inserta un placeholder o pista
        # se hace la asignación del evento <button-1> al cuadro de texto a traves de la funcion bind que maneja eventos 
        txt_entry_key_1.bind("<Button-1>", lambda event: clear_entry(event, txt_entry_key_1, "<Button-1>"))
        
        # Se genera el cuadro de texto de manera igual que el anterior, este cuadro de texto es para las 
        # llaves del archivo 2
        # Cuadro texto de la derecha
        txt_var_2 = tk.StringVar()
        txt_var_2.trace("w", lambda name, index,mode, var=txt_var_2: callback4(txt_var_2))
        txt_entry_key_2 = tk.Entry(root, width=30,textvariable=txt_var_2)
        txt_entry_key_2.place(x=700,y=150)
        txt_entry_key_2.insert(0,'Nombre llaves archivo 2')
        txt_entry_key_2.bind("<Button-1>", lambda event: clear_entry(event, txt_entry_key_2, "<Button-1>"))
        
        
        # TODO: modularizar tambien estos objetos labels
        # label 3 instruccion 2
        lbl_3 = tk.Label(root,text='Paso 2 - Definir llaves:',font=("Verdana", 12))
        lbl_3.place(x=260,y=145)
        # label 4 instruccion 3
        lbl_4 = tk.Label(root,text='Paso 3 - Ordenar por:',font=("Verdana", 12))
        lbl_4.place(x=260,y=175)

        # TODO: Seguir modularizando el aplicativo 
        ## cuadro de texto para colocar el nombre de las variables para ordenar
        # mismo proceso que el de los cuadro de texto anteriores
        # izquierda
        txt_var_3 = tk.StringVar()
        txt_var_3.trace("w", lambda name, index,mode, var=txt_var_3: callback5(txt_var_3))
        txt_entry_key_3 = tk.Entry(root, width=30, textvariable=txt_var_3)
        txt_entry_key_3.place(x=500,y=180)
        txt_entry_key_3.insert(0,'Nombre variables archivo 1')
        txt_entry_key_3.bind("<Button-1>", lambda event: clear_entry(event, txt_entry_key_3, "<Button-1>"))
        # Cuadro de la Derecha
        txt_var_4 = tk.StringVar()
        txt_var_4.trace("w", lambda name, index,mode, var=txt_var_4: callback6(txt_var_4))
        txt_entry_key_4 = tk.Entry(root, width=30, textvariable=txt_var_4)
        txt_entry_key_4.place(x=700,y=180)
        txt_entry_key_4.insert(0,'Nombre variables archivo 2')
        txt_entry_key_4.bind("<Button-1>", lambda event: clear_entry(event, txt_entry_key_4, "<Button-1>"))

        # label 5 instruccion 4
        lbl_5 = tk.Label(root,text='Paso 4 - Eliminar repetidos:',font=("Verdana", 12))
        lbl_5.place(x=260,y=205)

        # Creación de objetos combobox o lista desplegables
        # lista desplegable 1 (acción de eliminación)
        cmbx_1 = ttk.Combobox(root) # instanciar el objeto combobox en el objeto root
        cmbx_1.place(x=500,y=205)  # posicionar este objeto
        cmbx_1["values"] = ['Eliminar primeros', 'Eliminar últimos', 'No eliminar'] # definir los valores en la lista
        cmbx_1.current(2) # deja como valor predefinido el último elemento
        cmbx_1.bind("<<ComboboxSelected>>", callback1) # asignar el evento para capturar el valor a traves del de bind y el callback
        # lista desplegable complementaria o target de archivos a eliminar
        cmbx_1_c = ttk.Combobox(root)
        cmbx_1_c.place(x=650,y=205)
        cmbx_1_c["values"] = ['En ambos archivos', 'Solo en el archivo 1', 'Solo en el archivo 2']
        cmbx_1_c.current(0) # deja como valor predefinido el primer elemento
        cmbx_1_c.bind("<<ComboboxSelected>>", callback1c)

        # label 6 instruccion 5
        lbl_6 = tk.Label(root,text='Paso 5 - Tipo de cruce:',font=("Verdana", 12))
        lbl_6.place(x=260,y=235)
        # lista desplegable 2
        cmbx_2 = ttk.Combobox(root)
        cmbx_2.place(x=500,y=235)
        cmbx_2["values"] = ['Izquierda', 'Derecha', 'Interseccion', 'Todos']
        cmbx_2.current(0) # deja como valor predefinido el primer elemento
        cmbx_2.bind("<<ComboboxSelected>>", callback2)

        # Boton cruzar
        lbl_7 = tk.Label(root, text='Pulsar para ejecutar')
        lbl_7.place(x=540,y=320)
        btn_cross = tk.Button(root, text='Ejecutar', 
                             font=("Verdana", 12),
                             command=exe)
        btn_cross.place(x=550,y=290)                     

    # crear la app
    root = tk.Tk()
    # crea la GUI y ejecuta todo el programa
    create_initial_gui()
    # captura todo lo que pasa en la GUI
    root.mainloop()                    
    
if __name__ == '__main__':
    main()