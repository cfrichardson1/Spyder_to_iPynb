import argparse
import re
from pathlib import Path
import nbformat
from nbformat import v4 as nbv4

#
# parse command line args
#

parser = argparse.ArgumentParser(description='Converts Python files to Jupyter Notebook')
parser.add_argument('infile', type=str, help='path to the python file to read')
parser.add_argument('outfile', type=str, help='path to the notebook file to write')
args = parser.parse_args()

if not args.infile.endswith('.py'):
	raise Exception('infile must be a python file!')

if not args.outfile.endswith('.ipynb'):
	raise Exception('outfile must be a notebook file!')

out_path = Path(args.outfile)
if out_path.exists():
	raise Exception('file {} already exists!'.format(args.outfile))

#
# read python file
#

with open(args.infile) as f:
    text = f.read()

#
# write notebook file
#

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

types_and_conents = re.split('# In\[\s(.*?)\s\]', text)[1:]

cells = []

for cell_type, contents in chunks(types_and_conents, 2):
	fn = {
		'code': nbv4.new_code_cell,
		'markdown': nbv4.new_markdown_cell,
		'raw': nbv4.new_raw_cell,
	}.get(cell_type)
	if not fn:
		raise Exception('unknown cell type {}!'.format(cell_type))
	cells.append(fn(contents.strip()))

nb = nbv4.new_notebook(cells=cells)
nbformat.write(nb, args.outfile)

print('Done!')
