import requests
import pandas as pd
import json
import wikitextparser as wtp
import sys
import re



def get_articles(category, cat_fmt='cmpageid'):
    '''
    This function parses a Category page of Wiktionary,
    extracts the category members and the pageid corresponding to each member's page.
    It is aimed to extract the list of a page of the form: "{LANGUAGE} terms with IPA pronunciation".
    
    Takes the name of the Category and
    Returns a dataframe with columns: pageid, title
    '''
    
    if cat_fmt == 'cmtitle':
        url = f'https://en.wiktionary.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&format=json&utf8=1'
    elif cat_fmt == 'cmpageid':
        url = f'https://en.wiktionary.org/w/api.php?action=query&list=categorymembers&cmpageid={category}&format=json&utf8=1'
    else:
        raise Exception('cat_fmt can only be cmtitle or cmpageid')
    
    results = []
    params = []
    
    # first iter
    r = requests.get(url, params)
    jsondata = r.json()
    results.append(jsondata['query']['categorymembers'])

    while 'continue' in jsondata:
        params = jsondata['continue']
        r = requests.get(url, params)
        jsondata = r.json()
        results.append(jsondata['query']['categorymembers'])

    flat = [i for x in results for i in x]

    df = pd.DataFrame(flat)

    
    return df[['pageid','title']]


def get_IPA(pageid, lang_sect):
    '''
    This function parses through a Wiktionary page to extract the IPA text.
    It takes a pageid (and optionally, the language name)
    It will try to guess the language name from the page ti
    
    '''
    url = f'https://en.wiktionary.org/w/api.php?action=parse&pageid={pageid}&prop=wikitext&formatversion=2&format=json&utf8=1'
    r = requests.get(url)
    jsondata = json.loads(r.text)
    wikitext = jsondata['parse']['wikitext']
    
    parsed = wtp.parse(wikitext)
    
    ipas = []
    for section in parsed.sections:
        title = section.title
        if title:
            section_min = ''.join(char for char in title if char.isalnum()).lower()
            if section_min == lang_sect:
                for subsection in section.sections:
                    if subsection.title == 'Pronunciation':
                        pronunc = wtp.parse(subsection.contents)
                        for template in pronunc.templates:
                            if template.name == 'IPA':
                                try:
                                    for argument in template.arguments:
                                        ipa_obj = argument.value
                                        ipa_obj = re.sub("(<!--.*?-->)", "", ipa_obj, flags=re.DOTALL)
                                        ipas.append(ipa_obj)
                                except:
                                    raise Exception('Could not find IPA')
                            
    ipas_str = ', '.join(ipas[1:])
    
    return jsondata['parse']['title'], ipas_str, pageid

def get_glossary(lang_page_id, lang_name):
    '''
    '''
    df = get_articles(lang_page_id) 
    
    gloss = []
    
    for page in df['pageid']:
        gloss.append(get_IPA(page, lang_name))
    
    df_gloss = pd.DataFrame(gloss)
    df_gloss.columns = ['word', 'ipa', 'pageid']

    return df_gloss

def main(lang_page_id, lang_name, out_tsv):
    '''
    '''
    df = get_glossary(lang_page_id, lang_name)
    
    df.to_csv(out_tsv, sep='\t', index=None)
    


# .........................................................................

if __name__ == '__main__':
    lang_page_id = sys.argv[1]
    lang_name = sys.argv[2]  
    out_tsv = sys.argv[3]
    
    main(lang_page_id, lang_name, out_tsv)
