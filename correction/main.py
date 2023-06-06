import argparse
import sys
from .trailing_off import trail_off
from .utils import collect_xml_files, parse_xml_files
import logging
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

def main(argv):
    """
    Main entry point.
    """

    try:
        parser = argparse.ArgumentParser(
            prog='Correction tool',
            description='Applies corrections to all parse trees'
        )

        parser.add_argument(
            '-f', '--files',
            dest='in_dir',
            help='The input directory containing parse trees. All subdirectories are included.',
            required=True
        )

        parser.add_argument(
            '-dr', '--dry-run',
            dest='dry_run',
            help='Dry run: don\'t write files (default False)',
            action='store_true'
        )

        options = parser.parse_args(argv)

        in_dir, dry_run = options.in_dir, options.dry_run

        replacements = [trail_off]

        files = collect_xml_files(in_dir)
        trees = parse_xml_files(files)
        logging.info(f'{len(trees)} input files found')

        for rep in replacements:
            logging.info(f'Running replacement: {rep.label}\n')
            cnt = 0

            for (path, tree) in tqdm(trees):
                res = rep.replace(path, tree, dry_run)
                if res:
                    cnt += 1

            logging.info(f'Applied in {cnt} files')

    except Exception as exception:
        sys.stderr.write(repr(exception) + "\n")
        sys.stderr.write("for help use --help\n\n")
        raise exception

main(sys.argv[1:])
