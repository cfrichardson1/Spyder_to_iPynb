import argparse
import nbformat
from pathlib import Path
from nbconvert import ScriptExporter

#
# parse command line args
#

parser = argparse.ArgumentParser(description='Converts Jupyter Notebook files to Python')
parser.add_argument('infile', type=str, help='path to the notebook file to read')
parser.add_argument('outfile', type=str, help='path to the python file to write')
args = parser.parse_args()

if not args.infile.endswith('.ipynb'):
	raise Exception('infile must be a notebook file!')

if not args.outfile.endswith('.py'):
	raise Exception('outfile must be a python file!')

out_path = Path(args.outfile)
if out_path.exists():
	raise Exception('file {} already exists!'.format(args.outfile))

#
# read notebook file
#

nb = nbformat.read(args.infile, as_version=4)

#
# write python file
#

with open(args.outfile, 'w') as f:
	for cell in nb.cells:
		print('# In[', cell['cell_type'], ']', file=f)
		print(cell['source'], file=f)
		print(file=f)

print('Done!')