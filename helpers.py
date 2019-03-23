import sys

class term_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def str_bold(s):
    return ("{}{}{}".format(term_colors.BOLD, s, term_colors.ENDC))

def str_header(s):
    return ("{}{}{}".format(term_colors.HEADER, s, term_colors.ENDC))

def str_blue(s):
    return ("{}{}{}".format(term_colors.OKBLUE, s, term_colors.ENDC))

def str_green(s):
    return ("{}{}{}".format(term_colors.OKGREEN, s, term_colors.ENDC))

def str_fail(s):
    return ("{}{}{}".format(term_colors.FAIL, s, term_colors.ENDC))

def console_update(s):
    sys.stdout.write("\r{}".format(s))
    sys.stdout.flush()

