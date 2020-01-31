#!/usr/bin/env python

import os
import sys


here = sys.path[0]
if here not in ('/usr/bin', '/bin', '/usr/local/bin'):
    # git checkout
    toplevel = os.path.dirname(here)
    sys.path[0] = toplevel

from distutils.sysconfig import get_python_lib

sys.path.insert(1, os.path.join(get_python_lib(), "rcm_release"))

from rcm_release import *

DEFAULT_PDC_INSTANCE = 'https://pdc.engineering.redhat.com/rest_api/v1/'


def main():
    usage="%prog --pdc pdc_url"
    parser = OptionParser(usage=usage)
    parser.add_option(
        "--pdc",
        metavar="PDC_SERVER_URL",
        default=DEFAULT_PDC_INSTANCE,
        help="PDC instance shortcut or url [%default]",
    )

    opts, args = parser.parse_args()

    get_data = Pdc(opts.pdc)
    all_data = get_data.release_variants()
    print(all_data)


if __name__ == "__main__":
    main()
