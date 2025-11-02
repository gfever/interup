import nbformat
import sys
p = r'd:\PHPStormProjects\interup\kaggle_video_interpolation_notebook.ipynb'
print('Checking notebook:', p)
try:
    nb = nbformat.read(p, as_version=4)
except Exception as e:
    print('ERROR reading notebook:', e)
    sys.exit(1)
try:
    nbformat.write(nb, p)
    print('Notebook rewritten successfully (nbformat v', nbformat.__version__, ')')
except Exception as e:
    print('ERROR writing notebook:', e)
    sys.exit(1)

