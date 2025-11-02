import os, json, sys
paths=[r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb', r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook_fixed.ipynb']
for p in paths:
    print('Processing',p)
    with open(p,'rb') as f:
        raw=f.read()
    try:
        s=raw.decode('utf-8')
    except Exception:
        s=raw.decode('utf-8','replace')
    i=s.find('{')
    j=s.rfind('}')
    if i==-1 or j==-1 or j<=i:
        print('Failed to find JSON braces in',p)
        continue
    js=s[i:j+1]
    try:
        data=json.loads(js)
    except Exception as e:
        print('JSON parse error for',p,':',e)
        # try to fix common trailing commas
        import re
        js2=re.sub(r',\s*\}', '}', js)
        try:
            data=json.loads(js2)
            print('Parsed after trailing-comma fix')
        except Exception as e2:
            print('Still failed:',e2)
            continue
    # normalize nbformat
    data['nbformat']=4
    data['nbformat_minor']=2
    md=data.get('metadata',{})
    if 'kernelspec' not in md:
        md['kernelspec']={'name':'python3','display_name':'Python 3'}
    data['metadata']=md
    # write back
    with open(p,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
        f.write('\n')
    print('Wrote cleaned',p)
    # show preview
    with open(p,'r',encoding='utf-8') as f:
        text=f.read(300)
    print('Preview:', text[:300].replace('\n','\\n'))
print('Done')

