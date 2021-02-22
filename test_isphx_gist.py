r"""*Module to test link validity in intersphinx mappings gist.*

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    18 Feb 2021

**Copyright**
    \(c) Brian Skinn 2021

**Source Repository**
    http://www.github.com/bskinn/intersphinx-gist

**Documentation**
    N/A

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import re
from pathlib import Path

import arrow
import pytest
import requests as rq
import sphobjinv as soi


pat_domain = re.compile(r"https?://([^/]+)/")
pat_line = re.compile(r"<td[\s\S]+?js-file-line[\s\S]+?>[^<]+?http[^<]+</td>")
pat_tuple = re.compile(r"[(][^)]+[)]")

LOG_FILE = "gist-check.log"
TIMESTAMP = arrow.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def log_append(text):
    """Append text to log file."""
    with Path(LOG_FILE).open(mode="a") as f:
        f.write(text)


def get_mapping_tuples():
    """Retrieve intersphinx gist and extract mapping tuples."""
    resp = rq.get("https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209")
    log_append(f"Linkcheck run: {TIMESTAMP} UTC\n\n")
    log_append("Got gist page\n\n")

    data = resp.content.decode()
    mchs = list(pat_line.finditer(data))

    submchs = [
        sm.group(0).replace("&#39;", "'")
        for sm in [pat_tuple.search(m.group(0)) for m in mchs]
    ]

    tups = [eval(sm) for sm in submchs]

    [log_append(t[0] + "\n") for t in tups]
    log_append("\n")

    return tups


mapping_tuples_list = get_mapping_tuples()
mapping_tuple_ids = [pat_domain.search(t[0]).group(1) for t in mapping_tuples_list]


@pytest.fixture(scope="session", params=mapping_tuples_list, ids=mapping_tuple_ids)
def mapping_tuple(request):
    """Supply the mapping tuples singly to a test function."""
    return request.param


def test_mapping_root(mapping_tuple):
    """Check docs root link validity."""
    resp = rq.get(mapping_tuple[0])
    log_append(f"{mapping_tuple[0]}: {resp.status_code}\n")
    assert resp.ok


def test_mapping_objects_inv(mapping_tuple):
    """Check docs objects.inv link validity."""
    inv_link = mapping_tuple[1] or (mapping_tuple[0].removesuffix("/") + "/objects.inv")
    inv = soi.Inventory(url=inv_link)
    log_append(f"{repr(inv)}\n\n")
    assert inv

