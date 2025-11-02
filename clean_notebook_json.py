import json, sys
p = r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb'
print('Cleaning notebook:', p)
text = open(p, 'r', encoding='utf-8', errors='replace').read()
# find first '{' and last '}'
first = text.find('{')
last = text.rfind('}')
if first == -1 or last == -1 or last <= first:
    print('Cannot find JSON braces in file; abort')
    sys.exit(1)
json_text = text[first:last+1]
try:
    data = json.loads(json_text)
except Exception as e:
    print('JSON parse error:', e)
    # try to be tolerant: replace trailing ',\n}' issues
    try:
        import re
        jt = re.sub(r',\s*\}\s*$','}', json_text)
        data = json.loads(jt)
    except Exception as e2:
        print('Fallback parse failed:', e2)
        sys.exit(2)
# normalize
data['nbformat'] = 4
data['nbformat_minor'] = 2
md = data.get('metadata', {})
if 'kernelspec' not in md:
    md['kernelspec'] = {"name":"python3","display_name":"Python 3","language":"python"}
if 'language_info' not in md:
    md['language_info'] = {"name":"python","version":"3.8"}
data['metadata'] = md
# write back
with open(p, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('Notebook cleaned and written as nbformat 4 (minor 2).')

