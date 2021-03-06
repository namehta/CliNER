######################################################################
#  CliNER - cli.py                                                   #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Command Line Interface for working with CliNER.          #
######################################################################


__author__ = 'Willie Boag'
__date__   = 'Oct. 5, 2014'



import click
import os
import sys
import subprocess
import glob


# Ensure CLINER_DIR is set (TODO set properly?)
if 'CLINER_DIR' not in os.environ:
    print >>sys.stderr, '\n\tError: You must set the CLINER_DIR path to continue\n'
    exit()
sys.path.append( os.environ['CLINER_DIR'] + "/cliner/notes" )


from note import Note

@click.group()
def cliner():
    pass


supported_formats_help = "Data format ( " + ' | '.join(Note.supportedFormats()) + " )"


# Train
@cliner.command()
@click.option('--annotations'   ,help='Concept files for training.'             )
@click.option('--model'         ,help='Model output by train.'                  )
@click.option('--format'        ,help=supported_formats_help                    )
@click.option('--grid/--no-grid',help='Flag to enable grid search',default=False)
@click.option('--crf/--no-crf'  ,help='Flag to enable crfsuite'   ,default=True )
@click.option('--discontiguous_spans/--no-discontiguous_spans', help='Flag to enable detection and merging of discontiguous spans', default=False)
@click.option('--umls_disambiguation/--no-umls_disambiguation', help='Flag to enable mapping detecting entities to UMLS', default=False)
@click.argument('input')
def train(annotations, model, format, grid, crf, discontiguous_spans, umls_disambiguation, input):

    # Base directory
    BASE_DIR = os.environ.get('CLINER_DIR')
    if not BASE_DIR:
        raise Exception('Environment variable CLINER_DIR must be defined')

    # Executable
    runable = os.path.join(BASE_DIR, 'cliner/train.py')

    # Build command
    cmd = ['python', runable, '-t', input]

    # Arguments
    if annotations:
        cmd += ['-c', annotations]
    if model:
        cmd += ['-m',       model]
    if format:
        cmd += ['-f',      format]
    if grid:
        cmd += ['-g']
    if not crf:
        cmd += ['-no-crf']
    if discontiguous_spans:
        cmd += ['-discontiguous_spans']
    if umls_disambiguation:
        cmd += ['-umls_disambiguation']

    # Execute train.py
    subprocess.call(cmd)




# Predict
@cliner.command()
@click.option('--out'     , help='The directory to write the output'           )
@click.option('--model'   , help='Model used to predict on files'              )
@click.option('--format'  , help=supported_formats_help                        )
@click.option('--discontiguous_spans/--no-discontiguous_spans', help='Flag to enable detection and merging of discontiguous spans', default=False)
@click.option('--umls_disambiguation/--no-umls_disambiguation', help='Flag to enable mapping detecting entities to UMLS', default=False)
@click.argument('input')
def predict(out, model, format, discontiguous_spans, umls_disambiguation, input):

    # Base directory
    BASE_DIR = os.environ.get('CLINER_DIR')
    if not BASE_DIR:
        raise Exception('Environment variable CLINER_DIR must be defined')

    # Executable
    runable = os.path.join(BASE_DIR,'cliner/predict.py')

    # Build command
    cmd = ['python', runable, '-i', input]

    # Optional arguments
    if out:
        cmd += ['-o',    out]
    if model:
        cmd += ['-m',  model]
    if format:
        cmd += ['-f', format]
    if discontiguous_spans:
        cmd += ['-discontiguous_spans']
    if umls_disambiguation:
        cmd += ['-umls_disambiguation']

    # Execute predict.py
    subprocess.call(cmd)





# Evaluate
@cliner.command()
@click.option('--predictions', help='Directory where predictions  are stored.')
@click.option('--gold'       , help='Directory where gold standard is stored.')
@click.option('--out'        , help='Output file'                             )
@click.option('--format'     , help=supported_formats_help                    )
@click.argument('input')
def evaluate(predictions, gold, out, format, input):

    # Base directory
    BASE_DIR = os.environ.get('CLINER_DIR')
    if not BASE_DIR:
        raise Exception('Environment variable CLINER_DIR must be defined')

    # Executable
    runable = os.path.join(BASE_DIR,'cliner/evaluate.py')

    # Build command
    cmd = ['python', runable, '-t', input]

    # Optional arguments
    if predictions:
        cmd += ['-c', predictions]
    if gold:
        cmd += ['-r',        gold]
    if out:
        cmd += ['-o',         out]
    if format:
        cmd += ['-f',      format]

    # Execute evaluate.py
    subprocess.call(cmd)





# Format
@cliner.command()
@click.option('--annotations', help='Concept files for training.'                 )
@click.option('--format'     , help=supported_formats_help                        )
@click.option('--out'        , help='File to write the output.'                   )
@click.argument('input')
def format(annotations, format, out, input):

    # Base directory
    BASE_DIR = os.environ.get('CLINER_DIR')
    if not BASE_DIR:
        raise Exception('Environment variable CLINER_DIR must be defined')

    # Executable
    runable = os.path.join(BASE_DIR,'cliner/format.py')

    # Build command
    cmd = ['python', runable, "-t", input]

    # Optional arguments
    if annotations:
        cmd += ['-a', annotations]
    if out:
        cmd += ['-o',         out]
    if format:
        cmd += ['-f',      format]

    # Execute format.py
    subprocess.call(cmd)




if __name__ == '__main__':
    cliner()


