import json,sys,os,re
paths=[r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb', r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook_fixed.ipynb']
for p in paths:
    print('Processing',p)
    try:
        with open(p,'r',encoding='utf-8') as f:
            data=json.load(f)
    except Exception as e:
        print('Failed to load JSON file:',e)
        continue
    cells=data.get('cells',[])
    if len(cells)==1 and cells[0].get('cell_type')=='raw':
        src=cells[0].get('source','')
        if isinstance(src,list):
            inner=''.join(src)
        else:
            inner=str(src)
        # remove possible fence markers and comments before first '{'
        i=inner.find('{')
        j=inner.rfind('}')
        if i==-1 or j==-1 or j<=i:
            print('No JSON braces found inside raw cell; skipping')
            continue
        js=inner[i:j+1]
        try:
            obj=json.loads(js)
        except Exception as e:
            # try to fix common trailing-comma
            js2=re.sub(r',\s*\}','}', js)
            try:
                obj=json.loads(js2)
                print('Parsed after trailing-comma fix')
            except Exception as e2:
                print('Failed to parse inner JSON:',e2)
                continue
        # normalize
        obj['nbformat']=4
        obj['nbformat_minor']=2
        md=obj.get('metadata',{})
        if 'kernelspec' not in md:
            md['kernelspec']={'name':'python3','display_name':'Python 3'}
        obj['metadata']=md
        # write back
        with open(p,'w',encoding='utf-8') as f:
            json.dump(obj,f,ensure_ascii=False,indent=2)
            f.write('\n')
        print('Unwrapped and wrote',p,'cells=',len(obj.get('cells',[])))
    else:
        print('No single raw wrapper in',p,'(cells=',len(cells),')')
print('Done')

