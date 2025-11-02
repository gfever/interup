import json, sys, io
p = r'd:\PHPStormProjects\interup\kaggle_video_interpolation_notebook.ipynb'
print('Convert to nbformat 4:', p)
# read raw
with open(p, 'rb') as f:
    raw = f.read()
# try decode as utf-8 with errors replaced
text = None
for enc in ('utf-8','utf-8-sig','utf-16'):
    try:
        text = raw.decode(enc)
        break
    except Exception:
        continue
if text is None:
    text = raw.decode('utf-8','replace')
# strip leading non-json until first '{'
idx = text.find('{')
if idx > 0:
    print('Found prefix of length', idx, '- stripping')
    text2 = text[idx:]
else:
    text2 = text
# also remove trailing fenced triple backticks if present at end
if text2.strip().endswith('```'):
    # try to remove last backticks block
    last = text2.rfind('\n```')
    if last != -1:
        print('Stripping trailing ``` block')
        text2 = text2[:last]
# parse JSON
try:
    data = json.loads(text2)
except Exception as e:
    print('JSON parse error:', e)
    sys.exit(2)
# ensure nbformat 4
data['nbformat'] = 4
# choose minor 2
data['nbformat_minor'] = 2
# ensure metadata.kernelspec exists
md = data.get('metadata', {})
if 'kernelspec' not in md:
    md['kernelspec'] = {"name":"python3","display_name":"Python 3","language":"python"}
if 'language_info' not in md:
    md['language_info'] = {"name":"python","version":"3.8"}
data['metadata'] = md
# write back with compact formatting
with open(p, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('Wrote notebook as nbformat 4 (minor 2).')

