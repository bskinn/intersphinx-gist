r"""*Module to provide commit-or-not indicator.*

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    23 Feb 2022

**Copyright**
    \(c) Brian Skinn 2021-2022

**Source Repository**
    http://www.github.com/bskinn/intersphinx-gist

**Documentation**
    N/A

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import datetime
import sys


def main() -> int:
    """Return 1 for 'commit' or 0 for 'no commit'.

    Only commit between midnight and 2am on a Sunday.

    """
    now = datetime.datetime.utcnow()

    return 1 if (now.weekday == 6 and 0 <= now.hour <= 2) else 0


if __name__ == "__main__":
    sys.exit(main())
