import json, sys
p = r'd:\PHPStormProjects\interup\kaggle_video_interpolation_notebook.ipynb'
print('Validating', p)
try:
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print('JSON load error:', e)
    sys.exit(1)
# basic checks
ok = True
if 'nbformat' not in data:
    print('Missing nbformat')
    ok = False
if 'cells' not in data or not isinstance(data['cells'], list):
    print('Missing or invalid cells')
    ok = False
if 'metadata' not in data:
    print('Missing metadata')
    ok = False
else:
    if 'kernelspec' not in data['metadata']:
        print('Missing metadata.kernelspec')
        # not fatal
print('nbformat:', data.get('nbformat'))
print('nbformat_minor:', data.get('nbformat_minor'))
print('cells count:', len(data.get('cells', [])))
print('Validation result:', 'OK' if ok else 'FAILED')

