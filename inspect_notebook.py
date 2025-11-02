import json
p = r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb'
with open(p,'r',encoding='utf-8') as f:
    data = json.load(f)
cells = data.get('cells', [])
print('nbformat', data.get('nbformat'), 'nbformat_minor', data.get('nbformat_minor'))
print('cells_count=', len(cells))
for i, c in enumerate(cells[:10]):
    print(i, 'type=', c.get('cell_type'), 'source_lines=', len(c.get('source', [])))

# print first 5 characters of first source lines to inspect
if cells:
    s = cells[0].get('source','')
    if isinstance(s, list):
        print('\nFirst 5 source lines of cell 0:')
        for ln in s[:5]:
            print(ln[:200])
    else:
        print('\nCell0 source (first 200 chars):', str(s)[:200])

