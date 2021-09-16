# OTICross
---
![Screenshot_2](https://user-images.githubusercontent.com/18648306/131130828-d8be5755-2164-4423-841e-b35b6fb9969b.png)

## Instrucciones - Versión 1.0
1. Paso: Seleccionar los dos archivos excel.
2. Paso: Ingresar las llaves de cruce para los dos archivos en cada casilla respectiva. 
   El nombre de cada llave debe ser exactamente igual a los nombres en cada archivo excel. 
   El programa elimina puntos, comas y demás carácteres especiales dentro de las llaves.
   En caso de ser varias llaves separar con comas (,) sin dejar espacios en blanco.
3. Paso: De manera similar al paso anterior, especificar si hay nombres de columnas por el 
   cual se requiere ordenar los datos.
   Las variables pueden ser tipo fecha o enteras/flotantes y se organizan de menor a mayor 
   o más antiguo al más reciente para el caso de fechas.
   Estas columnas ya deben estar previamente tratadas. 
4. Paso: Seleccionar que desea hacer con los registros duplicados (repetidos usando las llaves).
   El paso de ordenamiento es realizado para que complementariamente se escoja si desea eliminar
   los primeros repetidos o los últimos y en que archivos.
5. Finalmente, seleccionar el tipo de cruce que desea realizar entre estos archivos.

El programa ejecutará estos pasos e imprimirá cada paso en la GUI y en la pantalla negra paralelamente.
Al final guardara un archivo excel en la misma ruta donde se leyeron los archivos iniciales.

## Limitaciones
* En esta versión solo es posible leer archivos excel. 
* Aunque no hay limitaciones con el tamaño de los archivos, a mayor volumen de datos el programa demora
  más su ejecución dando la sensación de haberse bloqueado.

## Mejoras - TO DO:
* Habilitar la opción de leer archivos CSV. (ya se añadió, tambien txt)
* Ejecutar el proceso de cargue de archivos en un nuevo proceso para hacer más ligera la ejecución. (ya se añadió, pero se puede mejorar)
* Listar las variables que hay en cada archivo con el fin de seleccionarlas y no de ingresarlas manualmente.
* Hacer más testeo

## Requerimientos:
* Python 3
* Tkinter
* Pandas
* Numpy
* Pyinstaller
* xlsxwriter

Comando Pyinstaller para generar el .exe --> pyinstaller -n oticross --onefile --clean main.py
