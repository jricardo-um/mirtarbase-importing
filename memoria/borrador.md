{ #INFO: longitud actual ~ 2 300 palabras = ~ 9 páginas }

{ #TODO: poner título y ajustar formato en el documento final }

Trabajo de fin de máster de Jorge Ricardo Alonso Fernández

## Índice

{ #TODO: actualizar índice en el documento final }

1. Introducción y objetivos (3 páginas)
   - Introducción
   - Resumen
     - Objetivo principal. Uso de mirtarbase como mecanismo para concer la función biológica de un determinado mirna en base a los genes que regula.
     - Volcado de MIRTARBASE a MONGODB
     - Desarrollo de servidios de REST de consulta a MONGODB
     - Validación funcional con HPO
     - Validación funcional con GO
2. Materiales y métodos (10 pág.)
   - Materiales
     - Base de datos (MONGODB)
     - Tecnologías Informáticas. Las librarías de PYTHON, IDE desarrollos, API REST.
     - Fuentes de datos (Mirtarbase, HPO human phenotype ontology, GO gene ontology)
     - Herramientas Bioinformáticas (gprofiler2)
   - Métodos
     - De carga de mirtarbase a mongodb
     - Recuperación de las datos
     - Integración con gprofiler2
3. Resultados (4\~5 pág.)
   - Descriptivo de la carga de mirtarbase
   - Caso de validación con GO
   - Caso de validación con HPO
4. Discusión (2 pág.)
5. Conclusiones (1 pág.)
6. Referencias
   - Abreviaciones
   - Bibliografía

# Extracto

## Introducción

Los μRNA son moléculas de RNA no codificantes y de longitud reducida (de 18 a 26 nucleótidos) que hibridan con uno o varios mRNA para regular la expresión de los genes que los transcriben, produciendo cambios significativos en varios procesos fisiológicos y patológicos. La base de datos miRTarBase, que recopila información verificada manualmente sobre la interacción entre estos μRNA y los genes a los que regulan (MTI), ha crecido considerablemente en los últimos años a raíz del reciente interés de los MTI para el desarrollo de medicamentos.

Sin embargo, miRTarBase no posee funciones ni interfaces que permitan su uso adecuado con herramientas bioinformáticas. { #TODO: hablar de los principios FAIR y ligarlo con MongoDB y la API REST? }

{ #TODO: hablar de MongoDB, repetir lo que está en materiales > bases de datos? }

Los principios de la arquitectura REST son un diseño de intercambio de datos que permite a cualquier aplicación desarrollada con cualquier lenguaje que admita conexiones a internet recibir información de una manera estándar sin necesidad de implementaciones complejas o específicas.

Por esas características en este trabajo se ha usado MongoDB para almacenar los datos obtenidos de miRTarBase y una API REST para ponerlos a disposición de los investigadores mediante el uso de herramientas informáticas.

{ #TODO: tengo que alargarla más o darle otro enfoque? }

## Resumen y objetivos

El objetivo principal de este trabajo es concer la función biológica de un determinado μRNA en base a los genes que regula, usando los MTI de miRTarBase como mecanismo para ello. Además, se pretende que el conjunto de scripts desarrollados puedan ser reutilizados para poder importar futuras versiones de miRTarBase con el mínimo de modificaciones posibles.

El portal de miRTarBase no posee ninguna API. Sólo se puede consultar mediante una GUI web o desgargar en formato `.xlsx` de Microsoft Excel. Para poder explotarla correctamente, se realizará un volcado de miRTarBase a MongoDB, una base de datos no relacional.

{ #TODO: reescribir siquiente párrafo, no se cómo enfocarlo... }

Después, se desarrollará un servicio REST que permita consultar la base de datos y, además, conecte con otras bases de datos para ofrecer la predicción funcional. Finalmente, se realizarán validaciones funcionales con HPO y GO.

# Desarrollo

## Materiales

### Base de datos

Como base de datos para este proyecto se ha escogido MongoDB, una base de datos NoSQL (no relacional). Éstas difieren de las bases de datos SQL en varios aspectos: son más rápidas, de cógido abierto, no necesitan esquemas previos, permiten un crecimiento horizontal de las bases de datos, etc. Y por esas ventajas se utilizan se utilizan para análisis semántico, de redes sociales y bioinformático, que crecen rápidamente y necesitan supervisaje contínuo. 

### Tecnologías Informáticas

Para desarrollar este trabajo se ha usado Python 3.10 como lenguaje, Visual Studio Code como editor y Ubuntu 22.04 como sistema operativo. Además de las librerías nativas de Python, se han usado las siguientes librerías externas junto con sus dependencias:

- `requests` librería que simplifica el envío de peticiones HTTP.

- `pandas` herramienta rápida y flexible de análisis y manipulación de datos.

- `pymongo` herramienta oficial recomendada por MongoDB para trabajar desde Python.

- `Flask` infraestructura ligera para desarrollo de aplicaciones web en Python.
  
  - Este paquete maneja la API REST. { #TODO: ya lo explico en la intro, está bien? }

- `gprofiler-official` interfaz oficial de g:Profiler para consultar desde Python.

### Fuentes de datos

Para obtener los MTI se ha usado miRTarBase, tal y como se describe anteriormente.

{ #TODO: leer artículos y escribir sobre GO y HPO }

## Métodos

### Carga de datos de miRTarBase a MongoDB

Para cargar los datos a MongoDB se han desarrollado scripts de python que realizan los siguientes pasos:

- Descarga de los ficheros `.xlsx` de miRTarBase a partir de una lista con sus URL. Realizado con `requests`.

- Conversión de `.xlsx` a `.json`, que es el formato más adecuado para importar con MongoDB. Para esta conversión, han hecho falta muchos ajustes y modificaciones.

- Subida de los ficheros `.json` generados a MongoDB. Realizado con `pymongo`.

#### Estructura original de la base de datos

Para convertir la base de datos y optimizarla para nuestras herramientas y necesidades, es necesario analizar la estructura original de la base de datos original, que es una tabla con las siguientes cabeceras:

- `miRTarBase ID` es el identificador que asigna miRTarBase a cada MTI.

- `miRNA` es el identificador del μRNA, que hace referencia a otras bases de datos.

- `Species (miRNA)` es la especie en la cuál se ha identificado el μRNA.

- `Target Gene` gen a cuyo mRNA se adhiere el μRNA.

- `Target Gene (Entrez ID)` identificador Entrez para el gen anterior.

- `Species (Target Gene)` especie para el gen anterior.

- `Experiments` lista de experimentos que usan en un artículo para investigar el MTI.

- `Support Type` evaluación de los autores de miRTarBase sobre los experimentos.

- `References (PMID)` identificador de PubMed para un artículo que describe un MTI.

| miRTarBase ID | miRNA           | Species (miRNA) | Target Gene | Target Gene (Entrez ID) | Species (Target Gene) | Experiments                                                | Support Type   | References (PMID) |
| ------------- | --------------- | --------------- | ----------- | ----------------------- | --------------------- | ---------------------------------------------------------- | -------------- | ----------------- |
| MIRT000515    | dre-miR-125b-5p | Danio rerio     | tp53        | 30590                   | Danio rerio           | Luciferase reporter assay//Western blot                    | Functional MTI | 20216554          |
| MIRT000515    | dre-miR-125b-5p | Danio rerio     | tp53        | 30590                   | Danio rerio           | In situ hybridization//Luciferase reporter assay//*(etc.)* | Functional MTI | 19293287          |
| MIRT000515    | dre-miR-125b-5p | Danio rerio     | tp53        | 30590                   | Danio rerio           | Luciferase reporter assay//qRT-PCR//Western blot           | Functional MTI | 21935352          |

Tabla: ejemplo de una entrada MTI en el fichero `.xlsx` de miRTarBase.

Cuando un MTI tiene varios artículos se repite la fila cambiando las columnas que hacen referencia a cada uno \(`Experiments`, `Support Type` y `References (PMID)`\). Debido a esto, la base de datos original tiene mucha información repetida que la hace pesada.

El campo `Experiments` tiene varias inconsistencias. Los nombres de las técnicas son inconsistentes, usando o no abreviaciones y sinónimos. Además, hay muchos errores de otrografía en los nombres de las técnicas. Finalmente, los separadores difieren en algunas entradas. En la mayoría son doble barras (`//`) o punto y coma (`;`).

Por último, el campo `miRTarBase ID` debería ser un identificador único para cada MTI, pero en un análisis de `hsa_MTI.xlsx` he identificado más de 16 000 conflictos \(distintos pares de MTI a los que les han asignado el mismo ID\). Me pondré en contacto con el grupo que confecciona la base de datos para informarles una vez haya acabado este trabajo.

#### Estructura nueva para MongoDB

El mejor diseño que he considerado para los objetivos de este trabajo es la siguiente:

```python
entry = {
   "_id": 999, # random number
   "miRTarBase ID": "MIRT000515",
   "miRNA": "dre-miR-125b-5p",
   "Species (miRNA)": "Danio rerio",
   "Target Gene": "tp53",
   "Target Gene (Entrez ID)": 30590,
   "Species (Target Gene)": "Danio rerio",
   "Experiments": [
      "Luciferase reporter assay",
      "Western blot",
      "In situ hybridization",
      "qRT-PCR",
      "(etc.)",
   ],
   "Support Type": "Functional MTI",
   "References (PMID)": [
      20216554,
      19293287,
      21935352,
   ],
}
```

Bloque: ejemplo de entrada formateada para ser importada a MongoDB, basada en el ejemplo de la tabla anterior.

El campo `_id` es un identificador que necesita MongoDB para cada entrada. Aunque lo mejor sería usar `miRTarBase ID` como `_id`, para evitar los conflictos sin modificar los datos he tenido que usar un ínidce al azar.

El campo `References (PMID)` resulta de juntar en una lista todos los artículos que hacen referencia al mismo MTI, y el campo `Support Type` es el valor más relevante de entre todos los artículos.

Finalmente, el campo `Experiments` corresponde a la lista de todos los experimentos de todos los artículos. Para poder lidiar con los problemas descritos anteriormente, he usado varios pasos:

- Para la separación de los elementos en la base de datos original, lo he implementado de manera que se intentan usar los dos separadores principales, `//` y `;`. El resto de entradas se dejan sin resolver en este paso.

- Para estandarizar los elementos de manera que se puedan usar programáticamente, además de para resolver algunos casos aislados de otros separadores como `/` o `,`, he desarrollado un diccionario de Python para corregirlos que he rellenado manualmente.
  
  - El script pregunta cómo corregir cada entrada al detectarla si no está ya presente en dicho diccionario. Esto será útil para las futuras versiones de las bases de datos que se tengan que importar.
  
  - Debido a la similitud de algunos nombres de técnicas y a la diversidad y cantidad de errores de otrografía, no he podido desarrollar ningún algoritmo para ayudar a corregir las entradas automáticamente.

### Recuperación de los datos

Para la consulta de los datos he desarrollado una sencilla API REST local, que luego se podrá desplegar en el servidor del grupo de investigación para el que hago este trabajo. Tiene varias rutas:

{ #TODO: discutir sobre las rutas y los argumentos }

- La raíz `/` devuelve una pequeña ayuda sobre como usar el servicio.

- En `/mtbase` se recibe un identificador de MTI y se devuelve la correspondiente entrada de la base de datos. Esto sería el equivalente a una API para miRTarBase, pero con las correcciones y mejoras descritas anteriormente.

- En `/search` se recibe uno o varios argumentos y se devuelven todos los identificadores de MTI que lo contienen sus correspondientes parámetros. Los argumentos corresponden a las etiquetas de la base de datos.

- En `/detail` se recibe un identificador de MTI o μRNA y se devuelve la caracterización funcional. \(explicado en el siguiente apartado\).

### Integración con gProfiler2

{ #TODO: alargar esto? }

Para la caracterización funcional el propio servicio REST hace una consulta en tiempo real a g:Profiler con los identificadores de los genes a través del paquete `gprofiler-official`.

### Carga de la bibliopedia

{ #TODO: hablar de la bibliopedia aunque lo haga después de entregar? lo digo para alargar el trabajo si se queda corto... }

# Resultados

## Descriptivo de la carga de mirtarbase

{ #TODO: consultar base de datos después de corregir el código }

{ #TODO: esto tiene que ver con lo de la página web y el diagrama de Sankey, no? }

## Caso de validación con GO

{ #TODO: hablar con profe }

## Caso de validación con HPO

{ #TODO: hablar con profe }

# Discusión

{ #TODO: discutir más, no estoy seguro de como enfocarlo }

Tal y como se puede apreciar al consultar la base de datos miRTarBase, contiene varios errores y no está optimizada para el uso computerizado. Es por ello que ha sido necesario rediseñar, corregir y reimplementar dicha base de datos para poder hacer consultas complejas o automatizadas.

# Conclusiones (1 pág.)

{ #TODO: hablar con profe }

# Referencias

## Trabajo propio

Todo el código escrito para este trabajo está disponible en el siguiente repositorio de github:

https://github.com/jricardo-um/mirtarbase-importing

## Abreviaciones

| Abreviación | Inglés                        | Español                                  |
| ----------- | ----------------------------- | ---------------------------------------- |
| RNA         | ribonucleic acid              | ácido ribonucléico                       |
| μRNA        | micro-RNA                     | micro RNA                                |
| mRNA        | messenger RNA                 | RNA mensajero                            |
| MTI         | μRNA-target interaction       | interacción μRNA diana                   |
| API         | application program interface | interfaz de programación de aplicaciones |
| GUI         | graphical user interface      | interfaz gráfica de usuario              |
| URL         | unique resource locator       | localizador de recurso único             |
| REST        | representation state transfer | transferencia de estado representado     |
| SQL         | structured query language     | lenguaje de consulta estructurada        |
| NoSQL       | not only SQL                  | no sólo SQL                              |

## Bibliografía

{ #TODO: revisar y añadir }

McKinney, W., & others. (2010). Data structures for statistical computing in python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51–56). https://doi.org/10.5281/zenodo.3509134

Grinberg, M. (2018). *Flask web development: developing web applications with python*. O'Reilly Media, Inc. https://dl.acm.org/doi/book/10.5555/2621997

Requests documentation https://requests.readthedocs.io/en/stable/

PyMongo documentation https://pymongo.readthedocs.io/en/stable/

GProfiler on PyPI https://pypi.org/project/gprofiler-official/

---

**Links para añadir a la bibliografía:**

- MIRTARBASE: [NLM](https://pubmed.ncbi.nlm.nih.gov/34850920/). [NAR](https://academic.oup.com/nar/article/50/D1/D222/6446528?login=false).
- MongoDB: [Link](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=72d51350e7082d6aac9079ed4d44adade2d3012a).
- API REST: [Este paper](https://academic.oup.com/bioinformatics/article/31/1/143/2366240?login=false) te va a ayudar a expresar las bondades de tener una api rest. La intrdoccuón está bastante bien. Y tienes referencia sobre REST.
- HPO: [Link](https://academic.oup.com/nar/article/49/D1/D1207/6017351?login=false).
- Gene Ontology: [Link](https://academic.oup.com/nar/article/47/D1/D330/5160994?login=false).
- G-Profiler: [Article](https://academic.oup.com/nar/article/47/W1/W191/5486750?login=false). [Home](https://biit.cs.ut.ee/gprofiler/gost). [PyPI](https://pypi.org/project/gprofiler-official/).
- PARA DISCUSION COMPARANDO CON OTRAS HERRAMIENTAS: [Link](https://academic.oup.com/bioinformatics/article/33/15/2421/3072087?login=false#118773415).
- Otras herramientas: [Studio3T](https://studio3t.com/), [Plotly](https://plotly.com/python/)'s [sankey diagram](https://plotly.com/python/sankey-diagram/).

---

**INFORMACIÓN SOBRE LA ELABORACIÓN DE LA MEMORIA** (guía docente)

El trabajo se concluirá con la elaboración de una memoria, que deberá tener la estructura de un trabajo científico (resumen, introducción, materiales y métodos, resultados, discusión, conclusiones, referencias) y una extensión máxima de 25 páginas en formato de 1 columna. Las 25 páginas incluyen desde el resumen hasta las referencias, excluyendo las páginas en blanco intermedias que se pudieran usar por cuestiones de formato. Se recomienda una orientación vertical y espaciado vertical sencillo, con unos márgenes mínimos de 2 cm (superior e inferior) y de 2.5 cm (izquierdo y derecho), letra Arial-10 o Arial Narrow-10 (texto) y Arial Narrow-10 (bibliografía).

La memoria se podrá escribir en inglés o en español. Si el estudiante opta por escribir la memoria en inglés, ésta deberá incluir una traducción al español del apartado “Resumen”.

Si la investigación realizada ha dado lugar a resultados recogidos en algún Trabajo de Investigación (publicado o no) o Comunicación a Congreso, se hará constar en la Memoria.

Cuando el trabajo haya sido realizado en el seno de una entidad externa, el estudiante deberá asegurarse de que no incumple ningún contrato de confidencialidad ni viola ningún derecho de propiedad intelectual. En este caso se deberá incluir en la memoria la autorización expresa por parte de la empresa para realizar y presentar el trabajo y la citada memoria. La Universidad de Murcia se exime de cualquier responsabilidad derivada del no cumplimiento de este reglamento por parte del estudiante.

La memoria se entregará en formato PDF a través de la [plataforma TF](http://tf.um.es) en las fechas establecidas a tal efecto y cumpliendo las limitaciones de tamaño vigentes en la plataforma.
