"""docopt sample

usage:
    cli_docopt.py -h | --help | --version
    cli_docopt.py say WORD [-abc] [--output=FILE]
    cli_docopt.py say2 <word> [--output=FILE]
    cli_docopt.py sum (NUM)...

options:
    -h --help       show this help message and exit
    -a --abuse      test a
    -b --bose       test bose
    -c --count      test count
    --version       show version and exit
    --output=FILE   output
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version="0.0.1")
    print(args)

    if args.get('say'):
        print(args.get('WORD'))
    elif args.get('say2'):
        print(args.get('<word>'))
        print(args.get('<file>'))
    elif args.get('sum'):
        str_list = args.get('NUM')
        int_list = [int(x) for x in str_list]
        print(sum(int_list))
