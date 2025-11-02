import json
p = r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook_fixed.ipynb'
print('Cleaning', p)
with open(p, 'rb') as f:
    raw = f.read()
try:
    s = raw.decode('utf-8')
except Exception:
    s = raw.decode('utf-8','replace')
start = s.find('{')
end = s.rfind('}')
if start==-1 or end==-1 or end<=start:
    print('Cannot find JSON region')
    raise SystemExit(1)
js = s[start:end+1]
obj = json.loads(js)
obj['nbformat']=4
obj['nbformat_minor']=2
if 'metadata' not in obj:
    obj['metadata']={'kernelspec':{'name':'python3','display_name':'Python 3'}, 'language_info':{'name':'python','version':'3.8'}}
with open(p,'w',encoding='utf-8') as f:
    json.dump(obj,f,ensure_ascii=False,indent=2)
    f.write('\n')
print('WROTE clean file; preview:')
with open(p,'r',encoding='utf-8') as f:
    print(f.read(200))
print('Done')

