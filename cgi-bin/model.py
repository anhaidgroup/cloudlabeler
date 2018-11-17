#!/usr/bin/python
import pandas as pd
import json
import os
import sqlite3
from pandas.io import sql
from StringIO import StringIO


# Database file and table
sql_path = os.path.join(os.path.dirname(__file__), '/var/www/cgi-bin/data/labels.db')
table_name = 'labels'

# Read and write the current table name
def save_table(tablen):
    f = open('/var/www/cgi-bin/data/tablename', 'w')
    w = f.write(tablen)

def getTable():
    f = open('/var/www/cgi-bin/data/tablename', 'r')
    global table_name
    table_name = f.read()

# Upload a csv file into the database
def upload_table(tablen,fileitem):
    getTable()
    io = StringIO(fileitem.file.read())
    # Load csv file into pandas
    table = pd.read_csv(io)
    # Save the pandas dataframe as a sql file
    cnx = sqlite3.connect(sql_path)
    table.to_sql(tablen, cnx, index=False, index_label='_id', if_exists='replace')

# read current table from the database
def read_table():
    getTable()
    cnx = sqlite3.connect(sql_path)
    return pd.read_sql('select * from \'' + table_name + '\'', con=cnx)

# read given table from the database
def read_table_given(tablen):
    cnx = sqlite3.connect(sql_path)
    return pd.read_sql('select * from \'' + tablen + '\'', con=cnx)

# read current table and process data for json
def read_data(filename = sql_path, filter_label_str=None, l_prefix='ltable_', r_prefix='rtable_',
              id_col='_id', label_col='Label'):

    data = read_table()
    if filter_label_str != None:
        filter_label_list = _parse_label_types(filter_label_str)
        data = data[data['Label'].isin(filter_label_list)]

    (ltable, rtable) = _process_data(data, l_prefix='ltable_', r_prefix='rtable_',
                  id_col='_id', label_col='Label')
    cols = list(ltable.columns)
    ltable = ltable.T.to_dict().values()
    rtable = rtable.T.to_dict().values()
    d = {}
    d['id'] = id_col
    d['columns'] = cols
    d['label'] = label_col
    d['ltable'] = ltable
    d['rtable'] = rtable
    return json.dumps(d)

def generate_tuplepage(file1, file2, file3):

    io1 = StringIO(file1.file.read())
    A = pd.read_csv(io1)
    io2 = StringIO(file2.file.read())
    B = pd.read_csv(io2)
    io3 = StringIO(file3.file.read())
    L = pd.read_csv(io3)

    # Get common columns
    common_attrs = [x for x in A.columns if x in B.columns]

    # Set the indices for easy retrieval of rows
    L = L.set_index(['ltable_id', 'rtable_id'], drop=False)
    idx_vals = list(L.index.values)
    A.set_index('ID', inplace=True, drop=False)
    B.set_index('ID', inplace=True, drop=False)

    # Read the html header and html tail files

    # Note that the html header needs to be modified to include correct input table names
    # (look for <th> Attribute </th> and the two strings below that should be modified)
    with open('/var/www/cgi-bin/html_header.txt') as f:
        html_head = f.read()


    with open('/var/www/cgi-bin/html_tail.txt') as f:
        html_tail = f.read()

    # Now construct the html pages and put them in "tuplepairpages" directory
    output_dir = '/var/www/html/tuplepairpages'

    attrs_only_in_A = [x for x in A.columns if x not in B.columns]
    attrs_only_in_B = [x for x in B.columns if x not in A.columns]

    html = ''

    for v in idx_vals:
        html = ''
        file_str = str(v[0])+'_'+str(v[1])
        tmp_header = html_head
        tmp_header = tmp_header.replace('$#$', file_str)
        html += tmp_header
        a = A.ix[v[0], common_attrs].values
        b = B.ix[v[1], common_attrs].values

        # First include all the common attributes
        for i in range(len(common_attrs)):
            html += '<tr>'

            html += '<td class="col-md-3">'
            html += str(common_attrs[i])
            html += '</td>'

            html += '<td class="col-md-3">'
            html += str(a[i])
            html += '</td>'

            html += '<td class="col-md-3">'
            html += str(b[i])
            html += '</td>'

            html += '</tr>'

        # Next include attributes that are only in A
        a = A.ix[v[0], attrs_only_in_A].values
        for i in range(len(attrs_only_in_A)):
            html += '<tr>'

            html += '<td class="col-md-3">'
            html += str(attrs_only_in_A[i])
            html += '</td>'

            html += '<td class="col-md-3">'
            html += str(a[i])
            html += '</td>'

            html += '<td class="col-md-3">'
            html += '<font size="3" color="orange">[ATTR NOT PRESENT]</font>'
            html += '</td>'

            html += '</tr>'


        # Next include attributes that are only in B
        b = B.ix[v[1], attrs_only_in_B].values
        for i in range(len(attrs_only_in_B)):
            html += '<tr>'

            html += '<td class="col-md-3">'
            html += str(attrs_only_in_B[i])
            html += '</td>'

            html += '<td class="col-md-3">'
            html += '<font size="3" color="orange">[ATTR NOT PRESENT]</font>'
            html += '</td>'

            html += '<td class="col-md-3">'
            html += str(b[i])
            html += '</td>'

            html += '</tr>'

        # Finally write the html file to tuplepairpages directory
        html += html_tail
        filename = file_str +'.html'



        with open(output_dir+'/'+filename, 'w') as text_file:
            text_file.write(html)
    return html

def save_data(label_str, filename=sql_path, lid_col='ltable_RecordId',
              rid_col='rtable_RecordId', label_col='Label'):
    getTable()
    cnx = sqlite3.connect(sql_path)
    data = pd.read_sql('select * from \'' + table_name + '\'', con=cnx)
    ids_chopped = _parse_label_str(label_str)
    data = _update_tbl_labels(data, ids_chopped)
    sql.to_sql(data, name=table_name, con=cnx, index=False, index_label='_id', if_exists='replace')

def _update_tbl_labels(data, ids_chopped):
    data.set_index('_id', drop=False, inplace=True)
    for ids in ids_chopped:
        idx, lid, rid, label = ids
        data.ix[idx, 'Label'] = label
    data.reset_index(drop=True, inplace=True)
    return data


def _parse_label_str(x):
    x = x.encode('ascii','ignore')
    x_splitted = map(str.strip, x.split(','))
    ids_chopped = [] # chop and convert to int
    for t in x_splitted:
	idx, lid, rid, label = map(str.strip, t.split('_'))
	ids_chopped.append([int(idx),lid,rid,int(label)])
    #print(ids_chopped)
    return ids_chopped


def _parse_label_types(x):
    x = x.encode('ascii', 'ignore')
    x_splitted = map(int, map(str.strip, x.split(',')))
    return x_splitted


def _process_data(data, l_prefix='ltable_', r_prefix='rtable_',
                  id_col='_id', label_col='Label'):
    d1 = get_one_table_data(data, l_prefix, id_col, label_col)
    d2 = get_one_table_data(data, r_prefix, id_col, label_col)
    return (d1, d2)


def get_one_table_data(data, prefix='ltable_', id_col='_id', label_col='Label'):
    l = list(data.columns)
    cols = [x.startswith(tuple([prefix, id_col, label_col])) for x in l]
    req_cols = data.columns[cols]
    d = data[req_cols]
    if prefix+'NDC_CODE' in d.columns:
        d.drop(prefix+'NDC_CODE', inplace=True, axis=1)
    col_vals = remove_prefixes(d.columns, prefix)
    col_vals = replace_char(col_vals, '_', ' ', ['_id'])
    d.columns = col_vals
    return d


def remove_prefixes(cols, prefix):
    y = []
    for col in cols:
        if col.startswith(prefix):
            y.append(col[len(prefix):])
        else:
            y.append(col)
    return y


def replace_char(cols, old, new, exp_list):
    for idx in range(0, len(cols)):
        if cols[idx] not in exp_list:
            cols[idx] = cols[idx].replace(old, new)
    return cols

# get_summary return status of label for html
# if api is true, return how many files unlabeled
def get_summary(tablen='', api=False):
    getTable()
    dlist = []
    cnx = sqlite3.connect(sql_path)
    if tablen:
        data = pd.read_sql('select * from \'' + tablen + '\'', con=cnx)
    else:
        data = pd.read_sql('select * from \'' + table_name + '\'', con=cnx)

    v = data.Label.values
    label_list = ['Unlabeled', 'User-Yes', 'User-No',
                  'User-Unsure', 'Expert-Yes', 'Expert-No', 'Expert-Unsure']
    if api is False:
        for i in range(0, len(label_list)):
            cnt = sum(v == i)
            d = {}
            d['label'] = label_list[i]
            d['value'] = cnt
            dlist.append(d)
        dd = {}
        dd['foo'] = dlist
        dd = json.dumps(dd)
        return dd
    else:
        d = {}
        d['unlabel'] = sum(v == 0)
        d['total'] = data.shape[0]
        return json.dumps(d)
