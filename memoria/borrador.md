{ #INFO: longitud actual ~ 4 700 palabras = ~ 16 páginas }

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

En 1993 se descubrió por primera vez un microRNA en _C. Elegans_, llamado _lin-4_, junto con algunas mutaciones que provocaban pérdidas de función. Y no fue hasta el 2000 que se descubrió otro más, también en _C. Elegans_ y de función parecida. Desde entonces se han descubierto más funciones de estas moléculas y más mutaciones involucradas en patologías. También se han desarrollado técnicas que los emplean diagnóstico e investigación.

Estos microRNA son moléculas de RNA no codificantes y de longitud reducida (de 18 a 26 nucleótidos) que hibridan con uno o varios mRNA para regular la expresión de los genes que los transcriben, produciendo cambios significativos en varios procesos fisiológicos y patológicos. A medida que se han ido descubriendo más de éstos, han surgido diversas bases de datos que recopilan deferentes aspectos de estas moléculas.

Una de esas bases de datos es miRTarBase, que recopila información verificada manualmente sobre la interacción entre estos microRNA y los genes a los que regulan (MTI). A midida que esta base de datos ha ido creciendo, ha obtenido datos suficientes como para poder describir o predecir las funciones biológicas que regulan.

Sin embargo, miRTarBase no posee funciones ni interfaces que permitan su uso adecuado con herramientas bioinformáticas. Además, al descargarla su formato tampoco permite su uso directo por dichas herramientas. Para poder hacerlo, habría que importar los datos en un sistema que permitiera su explotación computerizada.

{ #TODO: no sé como ligarlo bien con MongoDB y lo de las APIS, o si explicarlo más para la parte de objetivos y métodos }

MongoDB es sistema para bases de datos que está diseñado para poder ser explotado de manera efectiva.

## Resumen y objetivos

{ #PROFE: El resumen lo dejamos también para el final. En esa parte sólo tienen que estar bien claros los objetivos. }

El objetivo principal de este trabajo es concer la función biológica de un determinado microRNA en base a los genes que regula, usando los MTI de miRTarBase como mecanismo para ello. Además, se pretende que el conjunto de scripts desarrollados puedan ser reutilizados para poder importar futuras versiones de miRTarBase con el mínimo de modificaciones posibles.

El portal de miRTarBase no posee ninguna API. Sólo se puede consultar mediante una GUI web o desgargar en formato `.xlsx` de Microsoft Excel. Para poder explotarla correctamente, se realizará un volcado de miRTarBase a MongoDB, una base de datos no relacional.

{ #TODO: reescribir siquiente párrafo, no se cómo enfocarlo... }

Después, se desarrollará un servicio REST que permita consultar la base de datos y, además, conecte con otras bases de datos para ofrecer la predicción funcional. Finalmente, se realizarán validaciones funcionales con HPO y GO.

# Desarrollo

## Materiales

### Fuentes de datos sobre microRNAS

Existen muchas bases de datos que recogen información relacionada com microRNAs. Algunas de ellas son:

- miRBase recoge secuencias de RNA y localizaciones cromosómicas de dichas moléculas. Además, recoge anotaciones y referencias a otras herramientas y bases de datos.
  
  - No posee una API para consumo computerizado. Las secuencias se pueden descargar en formato fasta, las localizaciones cromosómicas en un archivo `.gff3` y el resto de datos en un archivo con formato EMBL.

- TarDB recoge predicciones de MTI de plantas e información relacionada de sus funciones.
  
  - Tampoco posee una API, pero se pueden descargar los datos en `.cons`, una tabla con alineaciones.

- miRmap recoge predicciones computerizadas sobre los MTI.
  
  - Posee una API, interfaz web con muchas opciones, y pueden descargarse los datos en formato libre `.csv`.

- miR2Disease recoge los MTI implicados en diversas enfermedades humanas.
  
  - No posee una API, se puede descargar una tabla en `.txt`.

- miRTarBase recoge evidencias experimentales de los MTI de muchas especies.
  
  - Tampoco posee una API, se puede descargar como una tabla `.xlsx`.

{ #PROFE: añadir referencias, tabla comparativa, frecuencia de actualización, num de especies y mirnas }

#### miRTarBase

Puesto que los objetivos de este trabajo requieren partir de evidencias experimentales, y se pretende aplicar al máximo de entradas posibles, se ha escogido miRTarBase para obtener información de los MTIs. Esta base de datos surgió en 2011, y durante la última década ha ido recogiendo manualmente imformación sobre MTIs creciendo su tamaño exponencialmente.

Desde su inicio y hasta ahora, la única manera de consultarla ha sido mediante su interfaz web, que han mejorado con cada actualización de la base de datos. Devuelve una tabla con varios campos, que incluyen:

- Un identificador asignado para cada entrada, que corresponde a un MTI

- Los microRNA implicados, junto con la especie del mismo

- Los genes a los que regulan, junto con la especie del mismo

- Los experimentos que demuestran cada MTI, desglosados según la evidencia
  
  - Asignan evidencia "fuerte" al _reporter assay_, al _western blot_ y al _qPCR_, y muestran uno en cada columna.
  - También muestran por separado el _microarray_, la _NGS_, el _pSILAC_ y el _CLIP-Seq_.
  - El resto de experimentos apareden como _Other_.

- El conteo de los experimentos y de los artículos publicados donde aparecen.

Por desgracia, no han implementado una API que permita el análisis y la consulta computerizadas, y la única manera de descargarlo es en formato `.xlsx`, que es propietario y no orientado a la programación. Para explotar la información que contiene habrá que exportarlo a la base de datos que hemos escogido.

### Fuentes de datos sobre funciones de genes

Para los objetivos de este trabajo también se necesitan fuentes de información sobre funciones celulares de los genes. Para ello se usará g:Profiler, un servidor web para análisis de enriquecimiento funcional. Su uso para este trabajo será recuperar una lista de funciones en términos `GO` en función de una lista de genes que se obtendrán de miRTarBase.

Gene Ontology es el recurso más completo y ampliamente utilizado que provee información sobre las funciones de los genes y sobre sus productos. Además de estar diseñado para proveer la información de manera computerizable, usa una ontología formal y bien definida para su estructura. Se basa en términos llamados `GO`, que tienen un significado concreto y pueden estar definidos usando otros `GO`.

{ #TODO: no tengo claro que hacer o como hablar del Human Phenotype Ontology, ya me lo explicará con lo de la validación funcional con GO / HPO }

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

### Tecnologías Informáticas

#### Entorno

Este trabajo se ha desarrollado con Ubuntu 22.04 LTS, una distribución de Linux, como sistema operativo. Como editor se ha empleado Visual Studio Code Community Edition, que permite visualizar código de una manera más clara y provee de funciones que ayudan a escribirlo, formatearlo y corregirlo.

#### Lenguage

Como lenguage de programación se ha usado Python 3.10, un lenguage interpretado de alto nivel. A diferencia de los lenguages compilados, permite programar sin necesidad de tener que interaccionar con el hardware y a diferencia de los lenguages de bajo nivel, permite una sintaxis más legible y sencilla, lo que lo ha convertido en el lenguage más empleado en el campo de la biología.

Para desarrollar este trabajo, además de las librerías nativas de Python, se han usado otras librerías externas junto con sus dependencias.

La librería `requests` simplifica, con respecto a la librería nativa, el envío de peticiones HTTP y el procesamiento de sus respuestas. En este trabajo se ha usado para la descarga automatizada de ficheros y para pruebas de conexión.

La librería `pandas` es una herramienta rápida y flexible de análisis y manipulación de datos. Permite importar, modificar y exportar bases de datos de y a diferentes formatos. Se ha usado para trabajar con los ficheros descargados de miRTarBase.

La librería `pymongo` es la herramienta oficial recomendada por MongoDB para trabajar desde Python. Permite administrar instalaciones locales o remotas de MongoDB y guardar o recuperar datos de ellas. En este trabajo se ha usado tanto para guardar y servir los datos de miRTarBase.

`Flask` infraestructura ligera para desarrollo de aplicaciones web en Python. Aunque para la implementación final se usarán otros recursos, en este trabajo se ha usado para montar un prototipo para la API REST final.

Finalmente la librería `gprofiler-official` es interfaz oficial de g:Profiler para consultar desde Python. En este trabajo se usa para consultar g:Profiler sin tener que escribir una gran cantidad de código con `requests`.

#### API REST

Para poder enviar a través de internet las funciones de los microRNAs que se soliciten, se ha usado una API REST. Las APIs son interfaces para los programas que permiten comunicarse con otros programas y automatizar procesos que requieran varios de ellos, tanto en local como a través de internet.

Con respecto a REST, es una arquitectura cuyo diseño de intercambio de datos permite a cualquier aplicación desarrollada con cualquier lenguaje información de una manera estándar sin necesidad de implementaciones complejas o específicas. Permite una variedad de ventajas con respecto a la principal alternativa SOAP.

|             | REST        | SOAP        |
| ----------- | ----------- | ----------- |
| acceso      | recursos    | operaciones |
| API pública | única       | múltiple    |
| interfaz    | consistente | variable    |
| formatos    | varios      | sólo `XML`  |
| caché       | permitida   | absente     |

Tabla: comparación entre REST y SOAP.

Así, las ventajas de tener una API REST comprenden desde el rendimiento hasta la consistencia en el uso. Además, suele ser implementada con HTTP, que permite conexiones a internet, y JSON, que también puede utilizarse con la API de MongoDB.

## Métodos

### Carga de datos de miRTarBase a MongoDB

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

Puesto que hay varios artículos que hacen referencia al mismo MTI, y varios experimentos que hacen referencia a los mismos artículos, los autores han usado las dos soluciones más comunes para forzar ese tipo de datos en una tabla:

- Para los campos de los artículos (`Support Type` y `References (PMID)`) han copiado las filas a las que hacen referencia y han variado esas columnas.

- Para el campo `Experiments` han usado una secuencia de caracteres como separados entre los ítems, que han juntado en la misma celda.

#### Errores y aspectos a mejorar

Puesto que las columans de los artículos repiten cada MTI al que hacen referencia, la base de datos original tiene la información de los MTI muy repetida y la hace innecesariamente pesada.

El campo `Experiments` tiene varios problemas. Los nombres de las técnicas son inconsistentes, usando o no abreviaciones y sinónimos. Además, hay muchos errores de otrografía arbitrarios y diferentes en diferentes entradas de los nombres de cada técnica. Finalmente, los separadores cambian en algunas entradas. En la mayoría son dos barras `//` o punto y coma `;`.

El campo `Target Gene` recoge genes cuyos nombres suelen estar compuestos por pocas letras y números. Puesto que la base de datos se ha guardado en `.xlsx`, y que Excel puede reemplazar conjuntos de letras y números por fechas, cambiando no sólo la representación sino el valor (se reemplaza por una estampa de tiempo), estas entradas pierden la información irreversiblemente. Además, hay unps pocos `Target Gene` que tienen diferentes `Target Gene (Entrez ID)` asociados.

Finalmente, el campo `miRTarBase ID` debería ser un identificador único para cada MTI, pero en un análisis de `hsa_MTI.xlsx` he identificado más de 16 000 conflictos (distintos pares de MTI a los que les han asignado el mismo ID). Me pondré en contacto con el grupo que confecciona la base de datos para informarles una vez haya acabado este trabajo.

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

- Para estandarizar los elementos de manera que se puedan usar programáticamente, además de para resolver algunos casos aislados de otros separadores como `/` o `,`, he desarrollado un diccionario de Python que relaciona los elementos con sus correcciones y lo he rellenado manualmente.
  
  - El script pregunta cómo corregir cada entrada al detectarla si no está ya presente en dicho diccionario, y actualiza el diccionario al recibir esas correcciones. Esto será útil para las futuras versiones de las bases de datos que se tengan que importar.
  
  - Debido a la similitud de algunos nombres de técnicas y a la diversidad y cantidad de errores de otrografía, no he podido desarrollar ningún algoritmo para ayudar a corregir las entradas automáticamente.

### Recuperación de los datos

Para la consulta de los datos he desarrollado una sencilla API REST local, que luego se podrá desplegar en el servidor del grupo de investigación para el que hago este trabajo. Tiene dos rutas y la raíz `/`, que devuelve una pequeña ayuda sobre como usar el servicio.

En `/search` se recibe uno o varios argumentos (campos de la base de datos con valores para buscar) y se devuelven todos los MTI que lo contienen sus correspondientes parámetros. Esta ruta equivaldría a una API para consultar miRTarBase.

Ejemplos de consulta:

- `http://127.0.0.1:5000/search?mirna_symbol=hsa-miR-222-3p` devuelve los MTI que se conocen para el microRNA `hsa-miR-222-3p`, y consecuentemente los genes que regula.

- `http://127.0.0.1:5000/search?gene_symbol=RAN&experiments=Western%20blot` devuelve los MTI en los que participa el gen `RAN`, y consecuentemente los microRNA que lo regulan. Además, limita los resultados a los MTI cuyas evidancias experimentales incluyan `Western blot`.

- `http://127.0.0.1:5000/search?pubmed_ids=19438724` devuelve los MTI para los que el artículo `19438724` proporciona evidencia.

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

En `/detail` se recibe el identificador de un microRNA bajo su clave en la base de datos `mirna_symbol`. Además, también se acepta como patámetro opcional el `support_type` para limitar los resultados. Esta ruta devuelve la caracterización funcional del microRNA, basándose en los genes de sus MTI con evidencia suficiente para deducirla. El concepto se explica en detalle en el siguiente apartado.

{ #TODO: añadir `support type`, valores repetidos o comas }

Un ejemplo de consulta sería `http://127.0.0.1:5000/detail?mirna_symbol=hsa-miR-664b-5p`, que devolvería la caracterización funcional del microRNA `hsa-miR-664b-5p`.

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

El objetivo principal de este trabajo es poder ofrecer una predicción de caracterización funcional de un microRNA en base a a los genes que regula, que se ofrecerá a través de una API REST. En la implementación actual corresponde a la ruta `/detail` y recibe el nombre del microRNA como argumento `mirna_symbol`.

Al recibir la petición se recuperan las entradas correspondientes a ese `mirna_symbol` en la base de datos importada, de manera equivalente a lo que sucedería en `/search`. Pero en vez de devolver los resultados, se agrupan los genes de esas entradas en función de la especie del gen.

Después, para cada grupo de genes se hace una consulta en tiempo real a g:Profiler para recibir la predicción funcional de éstos, que correspondería a la predicción de la función del microRNA. Esta consulta se hace a través del paquete `gprofiler-official`, la librería de Python que g:Profiler provee.

Finalmente se devuelve una lista simplificada de las predicciones funcionales para cada especie de esos genes, tal y como se aprecia en el apartado anterior.

### Carga de la bibliopedia

{ #TODO: hablar de cómo haremos lo de la bibliopedia, aunque lo haga después de entregar la memoria }

# Resultados

## Descriptivo de la carga de mirtarbase

En total se han importado 455087 entradas, la mayoría siendo MTIs de microRNA humano. En total hay 23 especies, y las que tienen más entradas son:

| mirna_specie           | Count  |
| ---------------------- | ------:|
| Homo sapiens           | 394973 |
| Mus musculus           | 55012  |
| Caenorhabditis elegans | 3236   |
| Rattus norvegicus      | 796    |
| Bos taurus             | 298    |

A pesar de la gran cantidad de MTIs registrados en la base de datos, los microRNAs que los componen son muy limitados, siendo 4993 en total. De entre éstos, los que tienen más entradas son:

| mirna_symbol   | Count |
| -------------- | -----:|
| hsa-miR-335-5p | 2705  |
| hsa-miR-26b-5p | 1935  |
| hsa-miR-16-5p  | 1606  |
| hsa-miR-124-3p | 1527  |

Finalmente los genes son algo más variados, llegando a 24429 distintos. Los que tienen más entradas son:

| gene_symbol | Count |
| ----------- | -----:|
| ZNF460      | 359   |
| CDKN1A      | 335   |
| NUFIP2      | 331   |
| AGO2        | 308   |

{ #TODO: esto tiene que ver con lo de la página web y el diagrama de Sankey, no? tendrá que explicármelo }

## Casos de validación funcional

{ #TODO: necesito saber que tengo que hacer para esto }

# Discusión

{ #TODO: discutir más, no estoy seguro de como enfocarlo }

Tal y como se puede apreciar al consultar la base de datos miRTarBase, contiene varios errores y no está optimizada para el uso computerizado. Es por ello que ha sido necesario rediseñar, corregir y reimplementar dicha base de datos para poder hacer consultas complejas o automatizadas.

Y es que a pesar de que hoy en día las tecnologías informáticas y sus correspondientes bases de datos han llegado a un punto de su desarrollo que están integradas en una infinidad de servicios que usamos a diario, muchas de las bases de datos bioinformáticas están estancadas. Algunos de los motivos más probables son que no hay interés por parte de los investigadores de escribir sus artículos y publicar su información de manera que pueda ser aprovechada de manera automática, o bien porque los investigadores del campo de la biología no tienen conocimiento informático suficiente como para hacerlo.

# Conclusiones

{ #TODO: al final }

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
| MTI           | miRNA-target interaction      | interacción de miRNA con su diana        |
| API           | application program interface | interfaz de programación de aplicaciones |
| GUI           | graphical user interface      | interfaz gráfica de usuario              |
| URL           | unique resource locator       | localizador de recurso único             |
| SOAP          | simple object access protocol | protocolo de acceso a objeto simple      |
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

https://www.sciencedirect.com/science/article/pii/S0027510711000613

Khan, M. W., & Abbasi, E. (2015). Differentiating Parameters for 
Selecting Simple Object Access Protocol (SOAP) vs. Representational 
State Transfer (REST) Based Architecture. *Journal of Advances in Computer Networks*, *3*(1), 63-6. https://www.researchgate.net/profile/Eram-Abbasi-3/publication/280736421_Differentiating_Parameters_for_Selecting_Simple_Object_Access_Protocol_SOAP_vs_Representational_State_Transfer_REST_Based_Architecture/links/597e0be2a6fdcc1a9accb0fe/Differentiating-Parameters-for-Selecting-Simple-Object-Access-Protocol-SOAP-vs-Representational-State-Transfer-REST-Based-Architecture.pdf

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
