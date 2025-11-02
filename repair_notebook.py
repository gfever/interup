import json,sys,os
p=r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb'
print('Repairing',p)
with open(p,'r',encoding='utf-8') as f:
    data=json.load(f)
# If notebook contains a single raw cell whose source is full JSON, extract and replace
cells=data.get('cells',[])
if len(cells)==1 and cells[0].get('cell_type')=='raw':
    src=cells[0].get('source','')
    if isinstance(src,list):
        inner=''.join(src)
    else:
        inner=str(src)
    inner=inner.strip()
    # try to find first '{'
    i=inner.find('{')
    if i!=-1:
        inner_json=inner[i:]
    else:
        inner_json=inner
    try:
        inner_data=json.loads(inner_json)
    except Exception as e:
        print('Failed to parse inner JSON:',e)
        sys.exit(2)
    # ensure nbformat 4
    inner_data['nbformat']=4
    inner_data['nbformat_minor']=2
    md=inner_data.get('metadata',{})
    if 'kernelspec' not in md:
        md['kernelspec']={"name":"python3","display_name":"Python 3","language":"python"}
    if 'language_info' not in md:
        md['language_info']={"name":"python","version":"3.8"}
    inner_data['metadata']=md
    with open(p,'w',encoding='utf-8') as f:
        json.dump(inner_data,f,ensure_ascii=False,indent=2)
        f.write('\n')
    print('Rewrote notebook with inner JSON; cells=',len(inner_data.get('cells',[])))
else:
    print('Notebook does not have single raw cell containing JSON. No action. cells=',len(cells))
    sys.exit(0)

