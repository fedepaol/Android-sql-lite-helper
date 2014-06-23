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


import jinja2
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

class ClassImplementer():
    ''' consumes the lines and returns an object useful for building sqlite facilities '''
    def __init__(self, file, name):
        self.fields = []
        self.name = name
        self.upper_name = name.upper()
        self.parse_file(file)
        self.table_name = self.name.upper() + '_TABLE'
        self._row_id = 'ROW_ID'
        self.database_create_name = 'DATABASE_%s_CREATE'%(self.name.upper())

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

            field = ClassField(field_name, self.name)
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
            self.fields.append(field)

def parse_options():
    parser = argparse.ArgumentParser(description='Generates sqlite helper or content provider.\nThe name of content provider triggers the generation of the content provider as well')

    parser.add_argument('-name', '--name', dest='name', help='Name of the dbhelper class', default='DbHelper')
    parser.add_argument('-f', '--file', dest='infile', help='file that contains classes definition')
    parser.add_argument('-p', '--package', dest='package', help='name of the package')
    parser.add_argument('-a', '--authority', dest='authority', help='name of the authority of the content provider', default='')
    parser.add_argument('-v', '--version', dest='dbversion', help='version of the database - to be used to upgrade the database', default='1')
    args = parser.parse_args()

    if not args.infile:
        raise ValueError("file name must be provided. Run with --help option to show script parameters")
    if not args.package:
        raise ValueError("package name must be provided. Run with --help option to show script parameters")
    if not args.authority:
        raise ValueError("authority name must be provided. Run with --help option to show script parameters")
    return args




templateLoader = jinja2.FileSystemLoader( searchpath="./" )
templateEnv = jinja2.Environment( loader=templateLoader )

SQL_TEMPLATE_FILE = "./sqllite.jinja"
PROVIDER_CLIENT_TEMPLATE_FILE = "./provider_client.jinja"
PROVIDER_TEMPLATE_FILE = "./provider.jinja"

def write_from_template(target_file, template_name, helper, options):
    template = templateEnv.get_template(template_name)
    templateVars = { "package" : options.package,
                     "name" : options.name,
                     "provider" : options.name + 'Provider',
                     "authority" : options.authority,
                     "dbversion" : options.dbversion,
                     "tables" : helper._classes,
                   }   
    target_file.write(template.render( templateVars ).encode('utf-8'))


if __name__ == '__main__':
    opt = parse_options()
    infile = open(opt.infile)
    helper = SqlLiteHelper(infile)
    target_file = open('%s.java'%(opt.name + 'DbHelper'), 'w')
    write_from_template(target_file, SQL_TEMPLATE_FILE, helper, opt)

    provider_name = opt.name + 'Provider'
    target_file = open('%s.java'%(provider_name), 'w')
    write_from_template(target_file, PROVIDER_TEMPLATE_FILE, helper, opt)
    target_file.close()

    client_file = open('%sClient.java'%(provider_name), 'w')
    write_from_template(client_file, PROVIDER_CLIENT_TEMPLATE_FILE, helper, opt)
    target_file.close()

    # opt.authority, opt.package, opt.cprovider, opt.dbname, opt.dbversion)helper.write_content_provider_client(target_file, opt.package, opt.package, opt.cprovider, opt.dbname)   #FIXME
    target_file.close()
    print 'Just remember to add :'
    print '<provider android:name=".%s"\n\
            android:authorities="%s"\n />'%(provider_name, opt.authority)
    print 'To your manifest file'

