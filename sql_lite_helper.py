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



from optparse import OptionParser

type_dictionary = { 'String':'text',
                    'Float':'float',
                    'Long':'integer',
                    'Date':'integer'}

class ClassField():
    '''keeps the informations related to a single field of a class'''
    def __init__(self, name, class_name):
        self.name = name
        capitalized_name = name.upper()
        self.key_name = class_name.upper() + '_' + capitalized_name + '_KEY'
        self.column_name = class_name.upper() + '_' + capitalized_name + '_COLUMN'
    def __repr__(self):
        return self.name

importmodules = '''import java.util.Date;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.util.Log;'''


banner = '''/**********************************************************************************************************************************************************************
****** AUTO GENERATED FILE BY ANDROID SQLITE HELPER SCRIPT BY FEDERICO PAOLINELLI. ANY CHANGE WILL BE WIPED OUT IF THE SCRIPT IS PROCESSED AGAIN. *******
**********************************************************************************************************************************************************************/
'''

class_creation = '''public class %s{
    private static final String DATABASE_NAME = "%sDb.db";
    private static final int DATABASE_VERSION = 1;'''

generic_methods = '''
    // Variable to hold the database instance
    private SQLiteDatabase db;
    // Context of the application using the database.
    private final Context context;
    // Database open/upgrade helper
    private myDbHelper dbHelper;
    public %s(Context _context) {
        context = _context;
        dbHelper = new myDbHelper(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    
    public %s open() throws SQLException { 
        db = dbHelper.getWritableDatabase();
        return this;
    }
                                                     
    public void close() {
        db.close();
    }'''


end_stuff ='''
    private static class myDbHelper extends SQLiteOpenHelper {
        public myDbHelper(Context context, String name, CursorFactory factory, int version) {
            super(context, name, factory, version);
        }

        // Called when no database exists in disk and the helper class needs
        // to create a new one. 
        @Override
        public void onCreate(SQLiteDatabase _db) {      
            %s
        }

        // Called when there is a database version mismatch meaning that the version
        // of the database on disk needs to be upgraded to the current version.
        @Override
        public void onUpgrade(SQLiteDatabase _db, int _oldVersion, int _newVersion) {
          // Log the version upgrade.
          Log.w("TaskDBAdapter", "Upgrading from version " + 
                                 _oldVersion + " to " +
                                 _newVersion + ", which will destroy all old data");
            
          // Upgrade the existing database to conform to the new version. Multiple 
          // previous versions can be handled by comparing _oldVersion and _newVersion
          // values.

          // The simplest case is to drop the old table and create a new one.
          %s
          // Create a new one.
          onCreate(_db);
        }
      }
     
      /** Dummy object to allow class to compile */
}''' 

def add_indentation(function):
    indent = function.replace('\n', '\n\t')
    return '\t' + indent 

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

    def write_dbadapter(self, target_file, name, pckg):
        target_file.write(banner)
        target_file.write('package %s;\n'%(pckg))
        target_file.write(importmodules)
        self.write_separators(target_file)
        target_file.write(class_creation%(name, name))
        self.write_separators(target_file)

        target_file.write(generic_methods%(name, name))

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
        target_file.write('\t// -------- TABLES CREATION ----------')
        self.write_separators(target_file)

        for single_class in self._classes:
            target_file.write('\t// %s CREATION \n'%(single_class._name))
            target_file.write('\t' + single_class.get_table_create())
            self.write_separators(target_file)


    def write_static_constants(self, target_file):
        ''' writes static constant statements for each class'''
        for single_class in self._classes:
            target_file.write('\t// -------------- %s DEFINITIONS ------------\n\n'%(single_class._name.upper()))
            declarations = single_class.get_static_declaration_fields()
            decl = '\t' + '\n\t'.join(declarations)
            target_file.write(decl)
            self.write_separators(target_file)


    def write_class_helpers(self, single_class, target_file):
        '''writes helper methods for every class'''
        target_file.write('\t// -------------- %s HELPERS ------------------\n'%(single_class._name.upper()))

        func = add_indentation(single_class.build_add_function())
        target_file.write(func)
        self.write_separators(target_file)

        #TODO it would be nice to cycle all build_something functions using introspection

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


    def write_end_file(self, target_file):
        command = end_stuff%(self.get_db_create(), self.get_db_drop())
        target_file.write(command)
        

    def get_db_create(self):
        rows = map(lambda x:'_db.execSQL(%s);\n\t\t'%(x.database_create_name), self._classes)
        return ''.join(rows)

    def get_db_drop(self):
        rows = map(lambda x:'_db.execSQL("DROP TABLE IF EXISTS " + %s + ";");\n\t\t'%(x._table_name), self._classes)
        return ''.join(rows)






class ClassImplementer():
    ''' consumes the lines and returns an object useful for building sqlite facilities '''
    def __init__(self, file, name):
        self._class_fields = []
        self._name = name
        self.parse_file(file)
        self._table_name = self._name.upper() + '_TABLE'
        self._row_id = self._name.upper() + '_ROW_ID'
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

            #TODO Check che type sia un tipo accettabile
            field_name = fields[1]
            try:
                if fields[2] == '*':
                    key = True
                else:
                    key = False
            except:
                key = False

            field = ClassField(field_name, self._name)
            field.type = type
            field.key = key
            field.sql_lite_type = type_dictionary[type]
            self._class_fields.append(field)

    def get_table_create(self):
        '''returns table creation command'''
        command = 'private static final String %s = "create table " + %s + " (" + %s + " integer primary key autoincrement"'%(self.database_create_name, self._table_name, self._row_id) + ''.join(map(lambda x: '+ ", " + \n\t\t\t\t %s + " %s "'%(x.key_name,  x.sql_lite_type), self._class_fields)) + ' + ");";\n'

        return command;
        
    def get_static_declaration_fields(self):
        '''returns a list of declarations of every field needed for sqllite usage'''
        static_fields = []
        template_static_string = r'private static final String %s = "%s";'
        template_static_int = r'private static final int %s = %d;'
        static_fields.append(template_static_string%(self._table_name, self._name))

        for column_num, field in enumerate(self._class_fields):
            static_fields.append(template_static_string%(field.key_name, field.name))
            static_fields.append(template_static_int%(field.column_name, column_num + 1))

        static_fields.append(template_static_string%(self._row_id, '_id'))

        return static_fields

    def get_function(self, signature, body):
        return '%s\n{\n%s\n}'%(signature, body)

    def get_content_values(self):
        ''' returns the list of command needed to declare a content values variable named contentValues on the stack, filled with all the fields of the class'''
        content_values_fill = '\tContentValues contentValues = new ContentValues();\n'
        for field in self._class_fields:
            if field.type != 'Date':
                content_values_fill = content_values_fill + '\tcontentValues.put(%s, %s);\n'%(field.key_name, field.name)
            else:
                content_values_fill = content_values_fill + '\tcontentValues.put(%s, %s.getTime());\n'%(field.key_name, field.name)
        return content_values_fill

    def get_arg_fields_list(self):
        ''' returns the fields of the class with the given time, separated by , useful in case of function argument list'''
        return ','.join('%s %s'%(field.type, field.name) for field in self._class_fields)


    def build_update_function(self):
        ''' returns the update function''' 
        function_sign = 'public long update%s('%(self._name)
        args = 'long _rowIndex, ' + self.get_arg_fields_list()
        function_sign = function_sign + args + ')'

        function_body = '\tString where = %s+ " = " + _rowIndex;\n'%(self._row_id) + \
        self.get_content_values() + '\treturn db.update(%s, contentValues, where, null);\n'%(self._table_name)
        return self.get_function(function_sign, function_body)

    def build_add_function(self):
        function_sign = 'public long add%s('%(self._name)
        function_args = self.get_arg_fields_list()
        function_sign = function_sign + function_args + ')'
        function_body = self.get_content_values() + '\treturn db.insert(%s, null, contentValues);\n'%(self._table_name)
        return self.get_function(function_sign, function_body)

    def build_remove_function(self):
        function_sign = 'public boolean remove%s(Long _rowIndex)'%self._name
        function_body = '\treturn db.delete(%s, %s+ "=" + _rowIndex, null) > 0;'%(self._table_name, self._row_id)
        return self.get_function(function_sign, function_body)

    def build_remove_all_function(self):
        function_sign = 'public boolean removeAll%s(Long _rowIndex)'%(self._name)
        function_body = '\treturn db.delete(%s, null, null) > 0;'%(self._table_name)
        return self.get_function(function_sign, function_body)

    def get_keys_array(self):
        ''' returs all the _KEY fields (the names of the columns) separated by , useful when I need to get the results of a cursor'''
        return self._row_id + ',\n\t\t\t\t' + ',\n\t\t\t\t'.join(field.key_name for field in self._class_fields)

    def build_get_all_function(self):
        function_sign = 'public Cursor getAll%s()'%(self._name)
        keys = self.get_keys_array()
        function_body = '\treturn db.query(%s, new String[] {%s}, null, null, null, null, null);'%(self._table_name, keys) 
        return self.get_function(function_sign, function_body)

    def build_get_one_function(self):
        function_sign = 'public Cursor get%s(long _rowIndex)'%(self._name)
        keys = self.get_keys_array()
        where = '%s + " = " + _rowIndex'%(self._row_id)
        function_body = '\tCursor res = db.query(%s, new String[] {%s}, %s, null, null, null, null);\n'%(self._table_name, keys, where) + '\tif(res != null){\n\t\tres.moveToFirst();\n\t}\n\treturn res;'
        return self.get_function(function_sign, function_body)



def parse_options():
    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="infile", help="file that contains classes definition", default="in.txt")
    parser.add_option("-n", "--name", dest="name", help="name of the dbhelper class ", default="dbhelper")
    parser.add_option("-p", "--package", dest="package", help="name of the package", default="")
    (options, args) = parser.parse_args()
    return options



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
        target_file = open('%s.java'%(opt.name), 'w')
        helper.write_dbadapter(target_file, opt.name, opt.package)
        target_file.close()

