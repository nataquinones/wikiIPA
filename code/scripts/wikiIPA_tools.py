import requests
import pandas as pd
import os
from datetime import date as dt


def get_articles(category, cat_fmt='cmpageid', save_tsv=False):
    '''
    This function parses a Category page of Wiktionary, extracts the category 
    members and the pageid corresponding to each member's page. 
    It is aimed  to extract the list of a page of the form: 
    "{LANGUAGE} terms with IPA pronunciation".
    
    input: the name of the Category
    output: a dataframe with columns: [pageid, title]
    '''
    
    if cat_fmt == 'cmtitle':
        
        url = ('https://en.wiktionary.org/w/api.php?' +
               'action=query' +
               '&list=categorymembers' +
              f'&cmtitle=Category:{category}' +
               '&format=json&utf8=1')
    
    elif cat_fmt == 'cmpageid':
        
        url = ('https://en.wiktionary.org/w/api.php?' +
               'action=query' +
               '&list=categorymembers' +
              f'&cmpageid={category}' +
               '&format=json&utf8=1')
    else:
        raise Exception('cat_fmt can only be cmtitle or cmpageid')
    
    
    results = []
    params = []
    
    # first iteration
    r = requests.get(url, params)
    jsondata = r.json()
    results.append(jsondata['query']['categorymembers'])

    while 'continue' in jsondata:
        params = jsondata['continue']
        r = requests.get(url, params)
        jsondata = r.json()
        results.append(jsondata['query']['categorymembers'])

    # flatten data
    flat = [i for x in results for i in x]
    
    # save as pandas df
    df = pd.DataFrame(flat)
    
    # add language column
    df['lang'] = df['title'].str.split('Category:').str[1].str.split(' terms').str[0]
    
    df = df[['pageid','title','lang']]
    
     
    lang_lower_list = []
    
    for language in df['lang']:
        language_lowercase = ''.join(char for char in language if char.isalnum()).lower()
        lang_lower_list.append(language_lowercase)
    
    df['lang_min'] = lang_lower_list
    
    
    if save_tsv:
        df.to_csv(save_tsv,
                  sep='\t',
                  index=None)
    
    return df



def create_list(version, date=True, out_dir = '../data'):
    '''
    '''
    # directory
    version_dir = os.path.join(out_dir, str(version))
    # language list path
    langlist_file = f'{version_dir}/language_list.tsv'
    
    # metadata file
    metadata_file = f'{version_dir}/metadata.txt'
    
    # today's date
    tdate = str(dt.today())
    
    # computations
    langs_ipa = get_articles('Terms with IPA pronunciation by language',
                             cat_fmt='cmtitle',
                             save_tsv=langlist_file)
    
    with open(metadata_file, 'w') as f:
        f.write(f'date: {tdate}\n')
        f.close()
