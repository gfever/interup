import json
files=[r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook.ipynb', r'd:\\PHPStormProjects\\interup\\kaggle_video_interpolation_notebook_fixed.ipynb']
for p in files:
    print('---',p)
    try:
        with open(p,'r',encoding='utf-8') as f:
            data=json.load(f)
    except Exception as e:
        print('LOAD ERROR:',e)
        continue
    print('nbformat=',data.get('nbformat'), 'nbformat_minor=',data.get('nbformat_minor'))
    cells=data.get('cells',[])
    print('cells_count=', len(cells))
    print('first_cell_type=', cells[0].get('cell_type') if cells else '(no cells)')
print('done')

