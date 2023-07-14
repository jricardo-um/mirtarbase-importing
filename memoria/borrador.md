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

{ #PROFE: La introducción la vamos a dejar para el final. Porque va a salir sola una vez que tengamos el resto de cosas. Tienes que ver la introducción como una introducción al problema que pretendemos resolver. Habría que describir mucho los mirnas y el impacto biológico que tienen. Luego habría que describir las bases de datos que hay de mirnas. No sólo está mirtarbase. Comentar sus debilidades y plantear el problema que nos da pie a escribir los objetivos. }

Los microRNA son moléculas de RNA no codificantes y de longitud reducida (de 18 a 26 nucleótidos) que hibridan con uno o varios mRNA para regular la expresión de los genes que los transcriben, produciendo cambios significativos en varios procesos fisiológicos y patológicos. La base de datos miRTarBase, que recopila información verificada manualmente sobre la interacción entre estos microRNA y los genes a los que regulan (MTI), ha crecido considerablemente en los últimos años a raíz del reciente interés de los MTI para el desarrollo de medicamentos.

Sin embargo, miRTarBase no posee funciones ni interfaces que permitan su uso adecuado con herramientas bioinformáticas. { #TODO: hablar de los principios FAIR y ligarlo con MongoDB y la API REST? }

{ #TODO: hablar de MongoDB, repetir lo que está en materiales > bases de datos? }

Los principios de la arquitectura REST son un diseño de intercambio de datos que permite a cualquier aplicación desarrollada con cualquier lenguaje que admita conexiones a internet recibir información de una manera estándar sin necesidad de implementaciones complejas o específicas.

Por esas características en este trabajo se ha usado MongoDB para almacenar los datos obtenidos de miRTarBase y una API REST para ponerlos a disposición de los investigadores mediante el uso de herramientas informáticas.

{ #TODO: tengo que alargarla más o darle otro enfoque? }

## Resumen y objetivos

{ #PROFE: El resumen lo dejamos también para el final. En esa parte sólo tienen que estar bien claros los objetivos. }

El objetivo principal de este trabajo es concer la función biológica de un determinado microRNA en base a los genes que regula, usando los MTI de miRTarBase como mecanismo para ello. Además, se pretende que el conjunto de scripts desarrollados puedan ser reutilizados para poder importar futuras versiones de miRTarBase con el mínimo de modificaciones posibles.

El portal de miRTarBase no posee ninguna API. Sólo se puede consultar mediante una GUI web o desgargar en formato `.xlsx` de Microsoft Excel. Para poder explotarla correctamente, se realizará un volcado de miRTarBase a MongoDB, una base de datos no relacional.

{ #TODO: reescribir siquiente párrafo, no se cómo enfocarlo... }

Después, se desarrollará un servicio REST que permita consultar la base de datos y, además, conecte con otras bases de datos para ofrecer la predicción funcional. Finalmente, se realizarán validaciones funcionales con HPO y GO.

# Desarrollo

## Materiales

### Bases de datos

Debido a la gran cantidad de conocimiento que se genera en relación con la biología, es necesario poder organizar, indexar y recuperar toda esa información. Las bases de datos, que son memorias informáticas en las que pueden integrarse datos dispuestos de modo que sean accesibles individualmente, cumplen exaxtamente esa función y han proliferado muchas diferentes para cada campo o tema de la biología.

Las primeras bases de datos que surgieron eran bases de datos relacionales. Empezaron a ganar popularidad después de 1970, fueron usadas en muchos ámbitos y usaban principalmente SQL para su manejo y consulta. De entre sus propiedades destacan:

- Tienen una estructura de datos rígida. Eso implica que hay que diseñar y definir su estructura antes de implementarla, pero fuerza a tener consistencia y permite otras características de este tipo de bases de datos.

- Sus implementaciones están diseñadas para tener un nodo centralizado en una máquina potente. Esto encaja con las necesidades conputacionales de su época.

Pero a partir del 2010 el crecimiento exponencial del tráfico de datos promovió el auge de la búsqueda de otros tipos de bases de datos que cubrieran las nuevas necesidades computacionales haciendo uso de el desarrollo de las tecnologías actuales. Surgieron así varias bases de datos llamadas NoSQL. Aunque hay muchas diferentes, suelen coincidir en que:

- Descartan la estructura rígida, puesto que la mayoría de usos no requieren esta complejidad. Se reemplazan con varios modelos de datos (de grafos, colecciones, documentos, llaves, columnas, *etc.*) que suelen permitir escalar las bases de datos horizontalmente, es decir, cambiar o añadir campos.

- Sus implementaciones permiten el servicio descentralizado, permitiendo escalar el hardware fácilmente y aumentar el rendimiento en conjunto. Además, reduce los costes del mismo.

La base de datos escogida para este proyecto es MongoDB, una base de datos con modelo de documentos. Las características que la hacen adecuada para este trabajo son:

- Como es documental, se basa en llaves que pueden tener valores u otras llaves anidadas. Esto permite definir estructuras con campos arbitrariamente relacionados. Además, esta estructura puede representarse bien en como JSON, que es el estándar para transacciones en internet, o como diccionarios de Python, que es el lenguaje más extendido en el campo de la biología.

- Permite el *sharding*, que es un método efectivo para distribuir dato en múltiples máquinas.
  
  - Su funcionamiento se basa en dividir la base de datos en varios *shards*, que contienen una porción de la base de datos y pueden replicarse y distribuirse en función de las necesidades de uso de cada una a lo largo del tiempo.
  
  - Esto ayuda a acomodar grandes cantidades de datos o a trabajar con recursos de harware limitados. También permite soportar grandes cargas de consultas a través de internet.

- { #TODO: añadir alguna propiedad más si es relevante }

### Fuentes de datos

{ #PROFE: Mirtarbase debería de tener su propio apartado y explicarlo detalladamente. }

Para obtener los MTI se ha usado miRTarBase.

{ #TODO: leer artículos y escribir sobre GO y HPO }

### Tecnologías Informáticas

> La parte de tecnologías informáticas hay que desarrollarlo un poco más.
> 
> Deberíamos tener otra sección de librerías en las que expliques lo que es una API y cuáles son las ventajas de una API REST. Y explicar más en detalle en que consiste una API REST y cuáles son los métodos que permite.
> 
> Para que te hagas una idea, esta parte debería de tener entre 4 y 5 páginas. Apoyate en artículos, en páginas web. 

Para desarrollar este trabajo se ha usado Python 3.10 como lenguaje, Visual Studio Code como editor y Ubuntu 22.04 como sistema operativo. Además de las librerías nativas de Python, se han usado las siguientes librerías externas junto con sus dependencias:

- `requests` librería que simplifica el envío de peticiones HTTP.

- `pandas` herramienta rápida y flexible de análisis y manipulación de datos.

- `pymongo` herramienta oficial recomendada por MongoDB para trabajar desde Python.

- `Flask` infraestructura ligera para desarrollo de aplicaciones web en Python.
  
  - Este paquete maneja la API REST. { #TODO: ya lo explico en la intro, está bien? }

- `gprofiler-official` interfaz oficial de g:Profiler para consultar desde Python.

## Métodos

### Carga de datos de miRTarBase a MongoDB

{ #PROFE: [...]. Problemas que has encontrado, que eso nos da juego para luego en la discusión hablar del estado actual de algunas bases de datos de bioinformática, etc. }

{ #PROFE: Pones los pasos pero yo lo apoyaría con un gráfico con el flujo de los datos. Si buscas data flowchart puedes ver algunos ejemplos. }

Para cargar los datos a MongoDB se han desarrollado scripts de python que realizan los siguientes pasos:

- Descarga de los ficheros `.xlsx` de miRTarBase a partir de una lista con sus URL.
  
  - Se ha realizado con un script simple usando la librería `requests`.

- Conversión de `.xlsx` a `.json`, que es el formato más adecuado para importar con MongoDB. Para esta conversión, es necesario:
  
  - Estudiar la estructura de la base de datos original.
  
  - Corregir las inconsistencias o los errores de la base de datos, si los hubieran.
  
  - Diseñar una nueva estructura que acomode los datos y permita su uso posterior.

- Instalación o configuración de MongoDB y subida de los ficheros `.json` generados.
  
  - En este trabajo se ha usado la instalación por defecto de MongoDB que ofrece `apt` en Ubuntu.
  
  - Se ha realizado la subida con un script simple usando la librería `pymongo`.

#### Estructura original de la base de datos

Para convertir la base de datos y optimizarla para nuestras herramientas y necesidades, es necesario analizar la estructura original de la base de datos original, que es una tabla con las siguientes cabeceras:

- `miRTarBase ID` es el identificador que asigna miRTarBase a cada MTI.

- `miRNA` es el identificador del microRNA, que hace referencia a otras bases de datos.

- `Species (miRNA)` es la especie en la cuál se ha identificado el microRNA.

- `Target Gene` es el gen a cuyo mRNA se adhiere el microRNA.

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

Puesto que hay varios 

#### Errores y aspectos a mejorar

Cuando un MTI tiene varios artículos se repite la fila cambiando las columnas que hacen referencia a cada uno \(`Experiments`, `Support Type` y `References (PMID)`\). Debido a esto, la base de datos original tiene mucha información repetida que la hace pesada.

El campo `Experiments` tiene varios problemas. Los nombres de las técnicas son inconsistentes, usando o no abreviaciones y sinónimos. Además, hay muchos errores de otrografía arbitrarios y diferentes en diferentes entradas de los nombres de cada técnica. Finalmente, los separadores cambian en algunas entradas. En la mayoría son dos barras `//` o punto y coma `;`.

{ #TODO: descarte de `gene_symbol` tipo `datetime.datetime` }

Por último, el campo `miRTarBase ID` debería ser un identificador único para cada MTI, pero en un análisis de `hsa_MTI.xlsx` he identificado más de 16 000 conflictos \(distintos pares de MTI a los que les han asignado el mismo ID\). Me pondré en contacto con el grupo que confecciona la base de datos para informarles una vez haya acabado este trabajo.

#### Estructura nueva para MongoDB

El mejor diseño que he considerado para los objetivos de este trabajo es la siguiente:

```python
entry = {
   "_id": "dre-miR-125b-5p_tp53", # miRNA + _ + Target Gene
   "mirtarbase_id": "MIRT000515", # miRTarBase ID
   "mirna_symbol": "dre-miR-125b-5p", # miRNA
   "mirna_specie": "Danio rerio", # Species (miRNA)
   "gene_symbol": "tp53", # Target Gene
   "gene_entrez": 30590, # Target Gene (Entrez ID)
   "gene_specie": "Danio rerio", #Species (Target Gene)
   "experiments": [
      "Luciferase reporter assay",
      "Western blot",
      "In situ hybridization",
      "qRT-PCR",
      "(etc.)",
   ], # Experiments
   "support_type": 4, # Support Type
   "pubmed_ids": [
      20216554,
      19293287,
      21935352,
   ], # References (PMID)
}
```

Bloque: ejemplo de entrada formateada para ser importada a MongoDB, basada en la tabla del ejemplo anterior.

Para permitir una integración más sencilla con otros programas y APIs, he renombrado los campos para que no contengan espacios ni caracteres especiales.

El campo `_id` es un identificador que necesita MongoDB para cada entrada. Aunque lo mejor sería usar `miRTarBase ID` como `_id`, para evitar los conflictos sin modificar los datos he tenido que usar un ínidce compuesto que debería caracterizar el MTI inequívocamente. Aún así, he descartado un conjunto pequeño de entradas que provocaban conflictos con este `_id`.

El campo `pubmed_ids` resulta de juntar en una lista todos los artículos que hacen referencia al mismo MTI, y el campo `support_type` es el valor más relevante de entre todos los correspondientes a esos artículos, simplificado a un número.

| MTI            | Strong | Weak | None |
| -------------- |:------:|:----:|:----:|
| Functional     | 4      | 3    |      |
| Non-Functional | 2      | 1    | 0    |

Tabla: asignación de variables numéricas para `support_type`.

Finalmente, el campo `experiments` corresponde a la lista de todos los experimentos de todos los artículos. Puesto que no es necesario para los objetivos de este trabajo, esta estructura descarta la relación entre cada conjunto de experimentos y su artículo, juntándolos todos para cada MTI.

Para poder lidiar con los otros problemas descritos anteriormente sobre este campo, he usado varios pasos:

- Para la separación de los elementos en la base de datos original, lo he implementado de manera que se intentan usar los dos separadores principales, `//` y `;`. El resto de entradas se dejan sin resolver en este paso.

- Para estandarizar los elementos de manera que se puedan usar programáticamente, además de para resolver algunos casos aislados de otros separadores como `/` o `,`, he desarrollado un diccionario de Python para corregirlos que he rellenado manualmente.
  
  - El script pregunta cómo corregir cada entrada al detectarla si no está ya presente en dicho diccionario. Esto será útil para las futuras versiones de las bases de datos que se tengan que importar.
  
  - Debido a la similitud de algunos nombres de técnicas y a la diversidad y cantidad de errores de otrografía, no he podido desarrollar ningún algoritmo para ayudar a corregir las entradas automáticamente.

### Recuperación de los datos

Para la consulta de los datos he desarrollado una sencilla API REST local, que luego se podrá desplegar en el servidor del grupo de investigación para el que hago este trabajo. Tiene dos rutas y la raíz `/`, que devuelve una pequeña ayuda sobre como usar el servicio.

En `/search` se recibe uno o varios argumentos (campos de la base de datos con valores para buscar) y se devuelven todos los MTI que lo contienen sus correspondientes parámetros. Esta ruta equivaldría a una API para consultar miRTarBase.

Ejemplos de consulta:

- `http://127.0.0.1:5000/search?gene_symbol=RAN` devuelve los MTI en los que participa el gen `RAN`, y consecuentemente los microRNA que lo regulan.

- `http://127.0.0.1:5000/search?mirna_symbol=hsa-miR-222-3p` devuelve los MTI que se conocen para el microRNA `hsa-miR-222-3p`, y consecuentemente los genes que regula.

- `http://127.0.0.1:5000/search?pubmed_ids=19438724` devuelve los MTI del los que el artículo `19438724` proporciona evidencia.

Ejemplo de respuesta:

```json
[
  {
    "_id": "hsa-miR-222-3p_BCL2L11",
    "experiments": [ "Luciferase reporter assay", "PAR CLIP", "Western blot" ],
    "gene_entrez": 10018, "gene_specie": "Homo sapiens", "gene_symbol": "BCL2L11",
    "mirna_specie": "Homo sapiens", "mirna_symbol": "hsa-miR-222-3p", "mirtarbase_id": "MIRT000134",
    "pubmed_ids": [ 33942856, 19438724, 23446348, 20371350 ], "support_type": 3
  },
  {
    "_id": "hsa-miR-221-3p_BCL2L11",
    "experiments": [
      "Real Time PCR (qPCR)", "Luciferase reporter assay", "PAR CLIP",
      "Western blot", "Cross-linking, Ligation, and Sequencing of Hybrids (CLASH)"
    ],
    "gene_entrez": 10018, "gene_specie": "Homo sapiens", "gene_symbol": "BCL2L11",
    "mirna_specie": "Homo sapiens", "mirna_symbol": "hsa-miR-221-3p", "mirtarbase_id": "MIRT000140",
    "pubmed_ids": [ 19438724, 23622248, 26503209, 23446348, 20371350 ], "support_type": 4
  },
  {
    "_id": "rno-miR-221-3p_Bcl2l11",
    "experiments": [ "Immunoblot", "Real Time PCR (qPCR)", "Reporter assay", "Luciferase reporter assay" ],
    "gene_entrez": 64547, "gene_specie": "Rattus norvegicus", "gene_symbol": "Bcl2l11",
    "mirna_specie": "Rattus norvegicus", "mirna_symbol": "rno-miR-221-3p", "mirtarbase_id": "MIRT004033",
    "pubmed_ids": [ 19438724 ], "support_type": 4
  },
  {
    "_id": "rno-miR-222-3p_Bcl2l11",
    "experiments": [ "Immunoblot", "Real Time PCR (qPCR)", "Reporter assay", "Luciferase reporter assay" ],
    "gene_entrez": 64547, "gene_specie": "Rattus norvegicus", "gene_symbol": "Bcl2l11",
    "mirna_specie": "Rattus norvegicus", "mirna_symbol": "rno-miR-222-3p", "mirtarbase_id": "MIRT004034",
    "pubmed_ids": [ 19438724 ], "support_type": 4
  }
]
```

Bloque: ejemplo de respuesta para los MTI descritos en el artículo `19438724`.

En `/detail` se recibe el identificador de un microRNA bajo su clave en la base de datos `mirna_symbol` y se devuelve la caracterización funcional de éste, basándose en los genes de sus MTI para deducirla. El concepto se explica en detalle en el siguiente apartado.

Un ejemplo de consulta sería `http://127.0.0.1:5000/detail?mirna_symbol=hsa-miR-664b-5p`, que devolvería la caracterización funcional del microRNA `hsa-miR-664b-5p`.

{ #TODO: discutir sobre la respuesta }

```json
{
  "Homo sapiens": [
    {
      "description": "\"Any process that modulates the frequency, rate or extent of the chemical reactions and pathways resulting in the formation of substances, carried out by individual cells.\" [GOC:mah]",
      "name": "regulation of cellular biosynthetic process",
      "native": "GO:0031326"
    }, "...",
    {
      "description": "\"The chemical reactions and pathways resulting in the formation of aromatic compounds, any substance containing an aromatic carbon ring.\" [GOC:ai]",
      "name": "aromatic compound biosynthetic process",
      "native": "GO:0019438"
    },
    {
      "description": "\"Any process that modulates the frequency, rate or extent of the chemical reactions and pathways by which individual cells transform chemical substances.\" [GOC:mah]",
      "name": "regulation of cellular metabolic process",
      "native": "GO:0031323"
    }
  ]
}
```

Bloque: ejemplo de respuesta para la caracterización funcional de `hsa-miR-664b-5p`.

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

| Abreviación   | Inglés                        | Español                                  |
| ------------- | ----------------------------- | ---------------------------------------- |
| RNA           | ribonucleic acid              | ácido ribonucléico                       |
| miRNA<br>μRNA | micro-RNA                     | micro RNA                                |
| mRNA          | messenger RNA                 | RNA mensajero                            |
| MTI           | miRNA-target interaction      | interacción del miRNA con su diana       |
| API           | application program interface | interfaz de programación de aplicaciones |
| GUI           | graphical user interface      | interfaz gráfica de usuario              |
| URL           | unique resource locator       | localizador de recurso único             |
| REST          | representation state transfer | transferencia de estado representado     |
| SQL           | structured query language     | lenguaje de consulta estructurada        |
| NoSQL         | not only SQL                  | no sólo SQL                              |

## Bibliografía

{ #TODO: revisar y añadir }

surgimiento de bases de datos nosql https://www.researchgate.net/profile/Jesus-Sanchez-Cuadrado/publication/257491810_A_repository_for_scalable_model_management/links/568baf0508ae051f9afc5857/A-repository-for-scalable-model-management.pdf

McKinney, W., & others. (2010). Data structures for statistical computing in python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51–56). https://doi.org/10.5281/zenodo.3509134

https://www.mongodb.com/docs/manual/sharding/

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
