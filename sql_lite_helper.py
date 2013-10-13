'''
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.  '''



import argparse

content_type_id = 1

type_dictionary = { 'String':'text',
                    'Float':'float',
                    'Double':'real',
                    'Long':'integer',
                    'Integer':'integer',
                    'Date':'integer',
                    'float':'float',
                    'double':'real',
                    'long':'integer',
                    'int':'integer',
                    }

constraint_dictionary = { 'NotNull':'not null',
                          'Unique':'unique'}

class ClassField():
    '''keeps the informations related to a single field of a class'''
    def __init__(self, name, class_name):
        self.name = name
        capitalized_name = name.upper()
        self.key_name = class_name.upper() + '_' + capitalized_name + '_COLUMN'
        self.column_name = class_name.upper() + '_' + capitalized_name + '_COLUMN_POSITION'
    def __repr__(self):
        return self.name

SQL_IMPORTMODULES = '''import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.util.Log;

import java.util.Date;'''

ROW_ID = '''    public static final String ROW_ID = "_id";'''


SQL_BANNER = '''/**********************************************************************************************************************************************************************
****** AUTO GENERATED FILE BY ANDROID SQLITE HELPER SCRIPT BY FEDERICO PAOLINELLI. ANY CHANGE WILL BE WIPED OUT IF THE SCRIPT IS PROCESSED AGAIN. *******
**********************************************************************************************************************************************************************/
'''

SQL_CLASS_CREATION = '''public class %s{
    private static final String TAG = "%s";

    private static final String DATABASE_NAME = "%sDb.db";
    private static final int DATABASE_VERSION = %s;'''

SQL_GENERIC_METHODS = '''
    // Variable to hold the database instance
    protected SQLiteDatabase mDb;
    // Context of the application using the database.
    private final Context mContext;
    // Database open/upgrade helper
    private MyDbHelper mDbHelper;
    
    public %s(Context context) {
        mContext = context;
        mDbHelper = new MyDbHelper(mContext, DATABASE_NAME, null, DATABASE_VERSION);
    }
    
    public %s open() throws SQLException { 
        mDb = mDbHelper.getWritableDatabase();
        return this;
    }
                                                     
    public void close() {
        mDb.close();
    }'''


SQL_FOOTER ='''
    private static class MyDbHelper extends SQLiteOpenHelper {
    
        public MyDbHelper(Context context, String name, CursorFactory factory, int version) {
            super(context, name, factory, version);
        }

        // Called when no database exists in disk and the helper class needs
        // to create a new one. 
        @Override
        public void onCreate(SQLiteDatabase db) {      
            %s
        }

        // Called when there is a database version mismatch meaning that the version
        // of the database on disk needs to be upgraded to the current version.
        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            // Log the version upgrade.
            Log.w(TAG, "Upgrading from version " + 
                        oldVersion + " to " +
                        newVersion + ", which will destroy all old data");
            
            // Upgrade the existing database to conform to the new version. Multiple 
            // previous versions can be handled by comparing _oldVersion and _newVersion
            // values.

            // The simplest case is to drop the old table and create a new one.
            %s
            // Create a new one.
            onCreate(db);
        }
    }
     
    /** Dummy object to allow class to compile */
}'''




CONTENT_IMPORTMODULES = '''
import android.content.ContentProvider;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.text.TextUtils;
import android.util.Log;'''


CONTENT_CLIENT_IMPORT = '''
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

import java.util.Date;'''



CONTENT_CLASS_CREATION = '''public class %s extends ContentProvider {
    private static final String DATABASE_NAME = "%sDb.db";
    private static final int DATABASE_VERSION = %s;
    private static final String TAG = "%s";
'''

CONTENT_SQL_CREATION = '''
    private MyDbHelper myOpenHelper;

    @Override
    public boolean onCreate() {
        myOpenHelper = new MyDbHelper(getContext(), DATABASE_NAME, null, DATABASE_VERSION);
        return true;
    }'''

CONTENT_QUERY = '''    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
        String[] selectionArgs, String sortOrder) {

        // Open thedatabase.
        SQLiteDatabase db;
        try {
            db = myOpenHelper.getWritableDatabase();
        } catch (SQLiteException ex) {
            db = myOpenHelper.getReadableDatabase();
        }

        // Replace these with valid SQL statements if necessary.
        String groupBy = null;
        String having = null;

        SQLiteQueryBuilder queryBuilder = new SQLiteQueryBuilder();

        // If this is a row query, limit the result set to the passed in row.
        switch (uriMatcher.match(uri)) {\n%s
                String rowID = uri.getPathSegments().get(1);
                queryBuilder.appendWhere(ROW_ID + "=" + rowID);
            default: break;
        }

        // Specify the table on which to perform the query. This can
        // be a specific table or a join as required.
        queryBuilder.setTables(getTableNameFromUri(uri));

        // Execute the query.
        Cursor cursor = queryBuilder.query(db, projection, selection,
                    selectionArgs, groupBy, having, sortOrder);
            cursor.setNotificationUri(getContext().getContentResolver(), uri);

        // Return the result Cursor.
        return cursor;
    }'''

CONTENT_DELETE = '''    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        SQLiteDatabase db = myOpenHelper.getWritableDatabase();

        switch (uriMatcher.match(uri)) {
%s
                String rowID = uri.getPathSegments().get(1);
                selection = ROW_ID + "=" + rowID + (!TextUtils.isEmpty(selection) ?  " AND (" + selection + ')' : "");
            default: break;
        }


        if (selection == null)
            selection = "1";

        int deleteCount = db.delete(getTableNameFromUri(uri),
                selection, selectionArgs);

        getContext().getContentResolver().notifyChange(uri, null);

        return deleteCount;
    }'''

CONTENT_INSERT = '''    @Override
    public Uri insert(Uri uri, ContentValues values) {
        SQLiteDatabase db = myOpenHelper.getWritableDatabase();
        String nullColumnHack = null;

        long id = db.insert(getTableNameFromUri(uri), nullColumnHack, values);
        if (id > -1) {
            Uri insertedId = ContentUris.withAppendedId(getContentUriFromUri(uri), id);
                                getContext().getContentResolver().notifyChange(insertedId, null);
            getContext().getContentResolver().notifyChange(insertedId, null);
            return insertedId;
        } else {
            return null;
        }
    }'''

CONTENT_UPDATE = '''    @Override
    public int update(Uri uri, ContentValues values, String selection,
                      String[] selectionArgs) {

        // Open a read / write database to support the transaction.
        SQLiteDatabase db = myOpenHelper.getWritableDatabase();

        // If this is a row URI, limit the deletion to the specified row.
        switch (uriMatcher.match(uri)) { %s
                String rowID = uri.getPathSegments().get(1);
                selection = ROW_ID + "=" + rowID + (!TextUtils.isEmpty(selection) ? " AND (" + selection + ')' : "");
            default: break;
        }

        // Perform the update.
        int updateCount = db.update(getTableNameFromUri(uri), values, selection, selectionArgs);

        // Notify any observers of the change in the data set.
        getContext().getContentResolver().notifyChange(uri, null);

        return updateCount;
    }'''


CONTENT_CLIENT_CLASS_CREATION = '''public class %sClient{'''



def add_indentation(function):
    indent = function.replace('\n', '\n    ')
    return '    ' + indent 

class SqlLiteHelper():
    '''Parses a Class file and produces a Java file with the sqlite helper class'''
    def __init__(self, file):
        self._classes = []
        for line in file:
            line.strip()
            values = line.split()
            if len(values) == 0:
                continue
            if values[0] == 'CLASS':
                self._classes.append(ClassImplementer(file, values[1]))

    def write_dbadapter(self, target_file, name, pckg, dbname, dbversion):
        print 'writing'
        target_file.write(SQL_BANNER)
        target_file.write('package %s;\n\n'%(pckg))
        target_file.write(SQL_IMPORTMODULES)
        self.write_separators(target_file)
        target_file.write(SQL_CLASS_CREATION%(name, name, dbname, dbversion))
        self.write_separators(target_file)
        target_file.write(SQL_GENERIC_METHODS%(name, name))
        self.write_separators(target_file)
        target_file.write(ROW_ID)
        self.write_separators(target_file)
        self.write_static_constants(target_file)
        self.write_separators(target_file)
        self.write_create_tables(target_file)
        self.write_separators(target_file)

        map(lambda x: self.write_class_helpers(x, target_file),  self._classes)

        self.write_separators(target_file)
        self.write_end_file(target_file)


    def write_separators(self, file):
        file.write('\n\n')
        
    def write_create_tables(self, target_file):
        ''' writes table creation statements'''
        target_file.write('    // -------- TABLES CREATION ----------')
        self.write_separators(target_file)

        for single_class in self._classes:
            target_file.write('    // %s CREATION \n'%(single_class._name))
            target_file.write('    ' + single_class.get_table_create())
            self.write_separators(target_file)


    def write_static_constants(self, target_file, is_content_provider = False):
        ''' writes static constant statements for each class'''
        for single_class in self._classes:
            target_file.write('    // -------------- %s DEFINITIONS ------------\n\n'%(single_class._name.upper()))
            declarations = single_class.get_static_declaration_fields()
            decl = '    ' + '\n    '.join(declarations) + '\n'
            target_file.write(decl)

            if is_content_provider:
                content_types = single_class.get_content_types()
                target_file.write('\n')
                target_file.write(content_types)

            self.write_separators(target_file)
            self.write_separators(target_file)



    def write_uris(self, target_file, authority):
        '''write static constant uris'''
        target_file.write('    // -------------- URIS ------------\n\n')
        for single_class in self._classes:
            uri = single_class.get_uri(authority)
            target_file.write(add_indentation(uri) + '\n')


    def write_uri_matcher(self, target_file, authority):
        start = '''    private static final UriMatcher uriMatcher;
    static {
        uriMatcher = new UriMatcher(UriMatcher.NO_MATCH);\n'''

        target_file.write(start)

        for single_class in self._classes:
            target_file.write('''        uriMatcher.addURI("%s", "%s", %s);\n'''%(\
                authority, single_class._name.lower(), single_class.get_allcontent_type()))
            target_file.write('''        uriMatcher.addURI("%s", "%s/#", %s);\n'''%(\
                authority, single_class._name.lower(), single_class.get_singlecontent_type()))

        target_file.write('    }')



    def write_get_table_name_from_uri(self, target_file):
        target_file.write('''    /**
    * Returns the right table name for the given uri
    * @param uri
    * @return
    */
    private String getTableNameFromUri(Uri uri){
        switch (uriMatcher.match(uri)) {\n''')

        for single_class in self._classes:
            target_file.write('            case %s:\n'%(single_class.get_allcontent_type()))
            target_file.write('            case %s:\n'%(single_class.get_singlecontent_type()))
            target_file.write('                return %s;\n'%(single_class.table_name))

        target_file.write('''            default: break;
        }

           return null;
    }''')

    def write_get_content_uri_from_uri(self, target_file):
        target_file.write('''\t/**
    * Returns the parent uri for the given uri
    * @param uri
    * @return
    */
    private Uri getContentUriFromUri(Uri uri){
        switch (uriMatcher.match(uri)) {\n''')

        for single_class in self._classes:
            target_file.write('            case %s:\n'%(single_class.get_allcontent_type()))
            target_file.write('            case %s:\n'%(single_class.get_singlecontent_type()))
            target_file.write('                return %s_URI;\n'%(single_class._name.upper()))

        target_file.write('''            default: break;
        }

        return null;
    }''')



    def get_single_cases(self):
        res = []
        for single_class in self._classes[:-1]:
            res.append('            case %s:\n'%(single_class.get_singlecontent_type()))

        res.append('            case %s:'%(self._classes[-1].get_singlecontent_type()))

        return ''.join(res)




    def write_class_helpers(self, single_class, target_file):
        '''writes helper methods for every class'''
        target_file.write('\t// -------------- %s HELPERS ------------------\n'%(single_class._name.upper()))

        func = add_indentation(single_class.build_add_function())
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_update_function())
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_remove_function())
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_remove_all_function())
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_get_all_function())
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_get_one_function())
        target_file.write(func)
        self.write_separators(target_file)



    def write_content_helpers(self, single_class, target_file, provider_name):
        '''writes helper methods for every class'''
        target_file.write('\t// -------------- %s HELPERS ------------------\n'%(single_class._name.upper()))

        func = add_indentation(single_class.build_content_add_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)


        func = add_indentation(single_class.build_content_remove_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_content_remove_all_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_get_all_content_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_get_one_content_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)

        func = add_indentation(single_class.build_update_content_function(provider_name))
        target_file.write(func)
        self.write_separators(target_file)


    def write_end_file(self, target_file):
        command =SQL_FOOTER%(self.get_db_create(), self.get_db_drop())
        target_file.write(command)
        

    def get_db_create(self):
        rows = map(lambda x:'db.execSQL(%s);\n\t\t\t'%(x.database_create_name), self._classes)
        return ''.join(rows)

    def get_db_drop(self):
        rows = map(lambda x:'db.execSQL("DROP TABLE IF EXISTS " + %s + ";");\n\t\t\t'%(x.table_name), self._classes)
        return ''.join(rows)

    def write_get_type(self, target_file, package):
        target_file.write('''    @Override
    public String getType(Uri uri) {
        // Return a string that identifies the MIME type
        // for a Content Provider URI
        switch (uriMatcher.match(uri)) {\n''')

        for single_class in self._classes:
            target_file.write('            case %s:\n'%(single_class.get_allcontent_type()))
            target_file.write('                return "vnd.android.cursor.dir/vnd.%s.%s";\n'%(package, single_class._name.lower()))
            target_file.write('            case %s:\n'%(single_class.get_singlecontent_type()))
            target_file.write('                return "vnd.android.cursor.dir/vnd.%s.%s";\n'%(package, single_class._name.lower()))

        target_file.write('''            default:
                throw new IllegalArgumentException("Unsupported URI: " + uri);
            }
    }''')


    def write_content_provider(self, target_file, auth, package, name, dbname, dbversion):
        print 'writing content provider : Authority %s Package %s Name %s DbName %s'%(auth, package, name, dbname)
        target_file.write(SQL_BANNER)
        target_file.write('package %s;\n\n'%(package))
        target_file.write(CONTENT_IMPORTMODULES)
        self.write_separators(target_file)
        target_file.write(CONTENT_CLASS_CREATION%(name, dbname, dbversion, name))
        self.write_separators(target_file)

        self.write_uris(target_file, auth)

        self.write_separators(target_file)
        target_file.write(ROW_ID)
        self.write_separators(target_file)
        self.write_static_constants(target_file, True)

        self.write_uri_matcher(target_file, auth)
        self.write_separators(target_file)
        self.write_create_tables(target_file)
        target_file.write(CONTENT_SQL_CREATION)
        self.write_separators(target_file)

        self.write_get_table_name_from_uri(target_file)
        self.write_separators(target_file)

        self.write_get_content_uri_from_uri(target_file)
        self.write_separators(target_file)

        target_file.write(CONTENT_QUERY%(self.get_single_cases()))
        self.write_separators(target_file)

        self.write_get_type(target_file, package)
        self.write_separators(target_file)

        target_file.write(CONTENT_DELETE%(self.get_single_cases()))
        self.write_separators(target_file)

        target_file.write(CONTENT_INSERT)
        self.write_separators(target_file)

        target_file.write(CONTENT_UPDATE%(self.get_single_cases()))
        self.write_separators(target_file)
        self.write_end_file(target_file)



    def write_content_provider_client(self, target_file, auth, package, name, dbname):
        print 'writing content provider client: Authority %s Package %s Name %s DbName %s'%(auth, package, name, dbname)
        target_file.write(SQL_BANNER)
        target_file.write('package %s;\n\n'%(package))
        target_file.write(CONTENT_CLIENT_IMPORT)
        self.write_separators(target_file)
        target_file.write(CONTENT_CLIENT_CLASS_CREATION%(name))

        self.write_separators(target_file)

        map(lambda x: self.write_content_helpers(x, target_file, name),  self._classes)
        target_file.write('}')







class ClassImplementer():
    ''' consumes the lines and returns an object useful for building sqlite facilities '''
    def __init__(self, file, name):
        self._class_fields = []
        self._name = name
        self.parse_file(file)
        self.table_name = self._name.upper() + '_TABLE'
        self._row_id = 'ROW_ID'
        self.database_create_name = 'DATABASE_%s_CREATE'%(self._name.upper())

    def parse_file(self, file):
        for line in file:
            line = line[:-1]
            fields = line.split()

            type = fields[0]

            if type == 'CLASS':
                continue
            if type == 'ENDCLASS':
                return

            field_name = fields[1]

            try:
                constr1 = fields[2]
            except:
                constr1 = ''
                
            try:
                constr2 = fields[3]
            except:
                constr2 = ''

            field = ClassField(field_name, self._name)
            field.type = type

            field.sql_lite_type = type_dictionary[type]
            if constr1 != '':
                field.sql_lite_constr1 = constraint_dictionary[constr1]
            else:
                field.sql_lite_constr1 = ''
            if constr2 != '':
                field.sql_lite_constr2 = constraint_dictionary[constr2]
            else:
                field.sql_lite_constr2 = ''
            self._class_fields.append(field)

    def get_table_create(self):
        '''returns table creation command'''
        command = 'private static final String %s = "create table " + %s + " (" + \n\t\t\t\t %s + " integer primary key autoincrement"'%(self.database_create_name, self.table_name, self._row_id) + ''.join(map(lambda x: ' + ", " + \n\t\t\t\t %s + " %s %s %s"'%(x.key_name,  x.sql_lite_type, x.sql_lite_constr1, x.sql_lite_constr2), self._class_fields)) + ' + ");";\n'

        return command
        
    def get_static_declaration_fields(self):
        '''returns a list of declarations of every field needed for sqllite usage'''
        static_fields = []
        template_static_string = r'public static final String %s = "%s";'
        template_static_int = r'public static final int %s = %d;'
        static_fields.append(template_static_string%(self.table_name, self._name))

        for column_num, field in enumerate(self._class_fields):
            static_fields.append(template_static_string%(field.key_name, field.name))
            static_fields.append(template_static_int%(field.column_name, column_num + 1))

        return static_fields

    def get_content_types(self):
        global content_type_id
        all_type = '    private static final int %s= %d;'%(self.get_allcontent_type(), content_type_id)
        content_type_id += 1
        single_type = '    private static final int %s= %d;'%(self.get_singlecontent_type(), content_type_id)
        content_type_id += 1
        return '\n'.join([all_type, single_type])


    def get_function(self, signature, body):
        return '%s{\n%s\n}'%(signature, body)

    def get_content_values_provider(self, provider_name):
        ''' returns the list of command needed to declare a content values variable named contentValues on the stack, filled with all the fields of the class'''
        content_values_fill = ' ContentValues contentValues = new ContentValues();\n'
        for field in self._class_fields:
            if field.type != 'Date':
                content_values_fill = content_values_fill + '   contentValues.put(%s.%s, %s);\n'%(provider_name, field.key_name, field.name)
            else:
                content_values_fill = content_values_fill + '   contentValues.put(%s.%s, %s.getTime());\n'%(provider_name, field.key_name, field.name)
        return content_values_fill

    def get_content_values(self):
        ''' returns the list of command needed to declare a content values variable named contentValues on the stack, filled with all the fields of the class'''
        content_values_fill = ' ContentValues contentValues = new ContentValues();\n'
        for field in self._class_fields:
            if field.type != 'Date':
                content_values_fill = content_values_fill + '   contentValues.put(%s, %s);\n'%(field.key_name, field.name)
            else:
                content_values_fill = content_values_fill + '   contentValues.put(%s, %s.getTime());\n'%(field.key_name, field.name)
        return content_values_fill

    def get_arg_fields_list(self):
        ''' returns the fields of the class with the given time, separated by , useful in case of function argument list'''
        return ', '.join('%s %s'%(field.type, field.name) for field in self._class_fields)

    def get_uri(self, authority):
        return 'public static final Uri %s_URI = Uri.parse("content://%s/%s");'%(self._name.upper(), authority, self._name.lower())


    def build_update_function(self):
        ''' returns the update function''' 
        function_sign = 'public long update%s('%(self._name)
        args = 'long rowIndex, ' + self.get_arg_fields_list()
        function_sign = function_sign + args + ')'

        function_body = '   String where = %s + " = " + rowIndex;\n'%(self._row_id) + \
        self.get_content_values() + '   return mDb.update(%s, contentValues, where, null);\n'%(self.table_name)
        return self.get_function(function_sign, function_body)

    def build_add_function(self):
        function_sign = 'public long add%s('%(self._name)
        function_args = self.get_arg_fields_list()
        function_sign = function_sign + function_args + ')'
        function_body = self.get_content_values() + '   return mDb.insert(%s, null, contentValues);\n'%(self.table_name)
        return self.get_function(function_sign, function_body)

    def build_remove_function(self):
        function_sign = 'public boolean remove%s(long rowIndex)'%self._name
        function_body = '   return mDb.delete(%s, %s + " = " + rowIndex, null) > 0;'%(self.table_name, self._row_id)
        return self.get_function(function_sign, function_body)

    def build_remove_all_function(self):
        function_sign = 'public boolean removeAll%s()'%(self._name)
        function_body = '   return mDb.delete(%s, null, null) > 0;'%(self.table_name)
        return self.get_function(function_sign, function_body)

    def get_keys_array(self):
        ''' returs all the _KEY fields (the names of the columns) separated by , useful when I need to get the results of a cursor'''
        return '\n              ' + self._row_id + \
                ',\n                ' + ',\n                '.join(field.key_name for field in self._class_fields)

    def get_columns_from_content_provider(self, provider_name):
        res = ['\t%s.%s'%(provider_name, self._row_id)]

        for field in self._class_fields:
            res.append('%s.%s'%(provider_name, field.key_name))

        return ',\n\t\t'.join(res)

    def build_get_all_function(self):
        function_sign = 'public Cursor getAll%s()'%(self._name)
        keys = self.get_keys_array()
        function_body = '\treturn mDb.query(%s, new String[] {%s}, null, null, null, null, null);'%(self.table_name, keys)
        return self.get_function(function_sign, function_body)

    def build_get_one_function(self):
        function_sign = 'public Cursor get%s(long rowIndex)'%(self._name)
        keys = self.get_keys_array()
        where = '%s + " = " + rowIndex'%(self._row_id)
        function_body = '\tCursor res = mDb.query(%s, new String[] {%s}, %s, null, null, null, null);\n'%(self.table_name, keys, where) + '\tif(res != null){\n\t\tres.moveToFirst();\n\t}\n\treturn res;'
        return self.get_function(function_sign, function_body)


    def build_update_content_function(self, provider_name):
        function_sign = 'public static int update%s(long rowId, '%(self._name) +  self.get_arg_fields_list() + ', Context c)'
        function_body = self.get_content_values_provider(provider_name) +\
                        '\n    Uri rowURI = ContentUris.withAppendedId(%s.%s_URI, rowId); \n\n\
    String where = null;\n\
    String whereArgs[] = null;\n\n\
    ContentResolver cr = c.getContentResolver();\n\
    int updatedRowCount = cr.update(rowURI, contentValues, where, whereArgs);\n\
    return updatedRowCount;'%(provider_name, self._name.upper())

        return self.get_function(function_sign, function_body)


    def build_get_one_content_function(self, provider_name):
        function_sign = 'public static Cursor get%s(long rowId, Context c)'%(self._name)

        function_body = '\tContentResolver cr = c.getContentResolver();\n\
    String[] result_columns = new String[] {\n\
    %s  };\n\n\
    Uri rowAddress = ContentUris.withAppendedId(%s.%s_URI, rowId);\n\n\
    String where = null;    \n\
    String whereArgs[] = null;\n\
    String order = null;\n\n\
    Cursor resultCursor = cr.query(rowAddress, result_columns, where, whereArgs, order);\n\
    return resultCursor;'%(self.get_columns_from_content_provider(provider_name), provider_name, self._name.upper())

        return self.get_function(function_sign, function_body)

    def build_get_all_content_function(self, provider_name):
        function_sign = 'public static Cursor getAll%s(Context c)'%(self._name)

        function_body = '\tContentResolver cr = c.getContentResolver();\n\
    String[] result_columns = new String[] {\n\
    %s  }; \n\n\
    String where = null;    \n\
    String whereArgs[] = null;\n\
    String order = null;\n\n\
    Cursor resultCursor = cr.query(%s.%s_URI, result_columns, where, whereArgs, order);\n\
    return resultCursor;'%(self.get_columns_from_content_provider(provider_name), provider_name, self._name.upper())

        return self.get_function(function_sign, function_body)


    def get_allcontent_type(self):
        return 'ALL%s'%(self._name.upper())

    def get_singlecontent_type(self):
        return 'SINGLE_%s'%(self._name.upper())

    def build_content_add_function(self, provider_name):
        function_sign = 'public static Uri add%s('%(self._name) +  self.get_arg_fields_list() + ', Context c)'
        function_body = self.get_content_values_provider(provider_name) +\
        '\tContentResolver cr = c.getContentResolver();\n\treturn cr.insert(%s.%s_URI, contentValues);'%(provider_name, self._name.upper())

        return self.get_function(function_sign, function_body)


    def build_content_remove_function(self, provider_name):
        function_sign = 'public static int remove%s(long rowIndex, Context c)'%self._name
        function_body = '   ContentResolver cr = c.getContentResolver();\n\
    Uri rowAddress = ContentUris.withAppendedId(%s.%s_URI, rowIndex);\n\
    return cr.delete(rowAddress, null, null);'%(provider_name, self._name.upper())
        return self.get_function(function_sign, function_body)

    def build_content_remove_all_function(self, provider_name):
        function_sign = 'public static int removeAll%s(Context c)'%(self._name)
        function_body = '   ContentResolver cr = c.getContentResolver();\n\
    return cr.delete(%s.%s_URI, null, null);'%(provider_name, self._name.upper())
        return self.get_function(function_sign, function_body)





def parse_options():
    parser = argparse.ArgumentParser(description='Generates sqlite helper or content provider.\nThe name of content provider triggers the generation of the content provider as well')

    parser.add_argument('-name', '--name', dest='name', help='Name of the dbhelper class', default='DbHelper')
    parser.add_argument('-i', '--infile', dest='infile', help='file that contains classes definition', default='in.txt')
    parser.add_argument('-db', '--dbhelper', dest='name', help='name of the dbhelper class ')
    parser.add_argument('-p', '--package', dest='package', help='name of the package', default='')
    parser.add_argument('-a', '--authority', dest='authority', help='name of the authority of the content provider', default='')
    parser.add_argument('-d', '--dbname', dest='dbname', help='name of the database file', default='dbFile')
    parser.add_argument('-c', '--cprovider', dest='cprovider', help='to enable generation of content provider')
    parser.add_argument('-v', '--version', dest='dbversion', help='version of the database - to be used to upgrade the database', default='1')
    args = parser.parse_args()
    return args

def test():
    infile = open(opt.infile)
    helper = SqlLiteHelper(infile)
    target_file = open(helper.targetfile, 'w')
    helper.write_dbadapter(target_file, opt.name)
    target_file.close()


if __name__ == '__main__':
    opt = parse_options()
    infile = open(opt.infile)
    helper = SqlLiteHelper(infile)
    if opt.name:
        target_file = open('%s.java'%(opt.name), 'w')
        helper.write_dbadapter(target_file, opt.name, opt.package, opt.dbname, opt.dbversion)
        target_file.close()

    if opt.cprovider:
        target_file = open('%s.java'%(opt.cprovider), 'w')
        print opt
        helper.write_content_provider(target_file, opt.authority, opt.package, opt.cprovider, opt.dbname, opt.dbversion)
        target_file.close()

        target_file = open('%sClient.java'%(opt.cprovider), 'w')

        helper.write_content_provider_client(target_file, opt.package, opt.package, opt.cprovider, opt.dbname)   #FIXME
        target_file.close()
        print 'Just remember to add :'
        print '<provider android:name=".%s"\n\
        android:authorities="%s"\n />'%(opt.cprovider, opt.authority)

        print 'To your manifest file'

