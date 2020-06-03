import argparse
import sys
from xor_exploration import xorfile


def make_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument(
        '--input_file', '-i', default='heavensVaultSave.json',
        help='file (encrypted) to read from',
        )
    parser.add_argument(
        '--output_file', '-o', default=None,
        nargs='?', const='',
        help='file to write an (unencrypted) copy to',
        )
    return parser


def main(args):
    output_file = xorfile(args.input_file, args.output_file or '')
    print(output_file)


if __name__ == "__main__":
    args = make_parser().parse_args()
    sys.exit(main(args))
