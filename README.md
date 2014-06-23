SQLite Helper
=========

*Describe your data and generate the content provider automagically*

Still Beta. Please report any issues you might have.


Python 2.x script to automatically generate code sqlite helper file for android AND/OR content provider code.

You can generate the sqlite helper class in case you do not need a content provider, or the content provider with a companion client class made of static methods.

Writing a content provider is boring, and it often include writing a lot of boilerplate code. 

Even if there are a couple of fully working orms for android, using a content provider is the suggested and only way to export your data to other apps. 
Moreover, it makes your life easier if you want to take advantage of content observer and / or a loader. 



Data description
-

You need to provide it an input file with the description of the data model you want to generate the code after

The structure of the input file is:
    
    CLASS ClassName
    JavaType        FieldName
    ENDCLASS


    CLASS ClassName1
    Date      BirthDate
    String    Name
    String    Surname
    double     Weight
    ENDCLASS


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


    sql_lite_helper.py [-h] [-name NAME] [-f INFILE] [-p PACKAGE] [-a AUTHORITY] [-v DBVERSION]

Generates a sqlite helper class, a content provider and a content provider client.

ie:
>python sql_lite_helper.py -f sample.txt -n SampleGenerate -p com.whiterabbit -a com.whiterabbit.provider


Requirements
-

This script uses jinja2 template engine in order to generate the various files, so it must be installed in the current environment. 
The best way to install it is through pip or easy_install. 
If you have either one of them available on your machine, all you have to do is

    pip install Jinja2

or

    easy_install Jinja2


----


If you have any issue or question  please contact me at fedepaol@gmail.com


