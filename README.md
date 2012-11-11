SQLite Helper
=========

Python script to automatically generate code sqlite helper file for android AND/OR content provider code.

You can generate the sqlite helper class in case you do not need a content provider, or the content provider with a companion client class made of static methods.


Data description
-

You need to provide it an input file with the description of the data model you want to generate the code after

The structure of the input file is:
`CLASS ClassName
JavaType        FieldName
ENDCLASS`

`CLASS ClassName1
Date      BirthDate
String    Name
String    Surname
float     weight
ENDCLASS`


At the moment the only supported types are 
* Float
* Double
* Long
* Integer 
* Date (as in java.util.Date)
* float
* double
* long
* int

You can put more than one class in the same file.
Another improvement _could_ be to take a java Pojo as input file.

Usage
-

The usage is pretty simple. Provide the input file, the name of the class you want to create and the name of the package you want the class to belong to.

sql_lite_helper.py [-h] [-name NAME] [-i INFILE] [-db NAME]
\[-p PACKAGE] [-a AUTHORITY] [-d DBNAME]
                          [-c CPROVIDER]

Generates sqlite helper or content provider. The name of content provider
triggers the generation of the content provider as well

optional arguments:
  -h, --help            show this help message and exit
  -name NAME, --name NAME
                        Name of the dbhelper class
                        
  -i INFILE, --infile INFILE
                        file that contains classes definition
                        
  -db NAME, --dbhelper NAME
                        name of the dbhelper class
                        
  -p PACKAGE, --package PACKAGE
                        name of the package
                        
  -a AUTHORITY, --authority AUTHORITY
                        name of the authority of the content provider
                        
  -d DBNAME, --dbname DBNAME
                        name of the database file
                        
  -c CPROVIDER, --cprovider CPROVIDER
                        to enable generation of content provider


ie:
python sql_lite_helper.py -i sample.txt -n MyDbAdapter -p com.fede
or
python sql_lite_helper.py -i sample.txt -p com.fede -a com.fede.dbprovider -c DroidContentProvider
to generate the content provider as well

----

If you have any issue or question  please contact me at fedepaol@gmail.com


