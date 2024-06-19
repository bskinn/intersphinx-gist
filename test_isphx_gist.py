r"""*Module to test link validity in intersphinx mappings gist.*

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    18 Feb 2021

**Copyright**
    \(c) Brian Skinn 2021-2024

**Source Repository**
    http://www.github.com/bskinn/intersphinx-gist

**Documentation**
    N/A

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import re
from itertools import dropwhile
from pathlib import Path

import arrow
import pytest
import requests as rq
import sphobjinv as soi
from bs4 import BeautifulSoup as BSoup


pat_domain = re.compile(r"https?://([^/]+)/")
pat_line = re.compile(r"<td[\s\S]+?js-file-line[\s\S]+?>[^<]+?http[^<]+</td>")
pat_tuple = re.compile(r"[(][^)]+[)]")

LOG_FILE = "gist-check.log"
TIMESTAMP = arrow.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def log_append(text):
    """Append text to log file."""
    with Path(LOG_FILE).open(mode="a") as f:
        f.write(text)


def get_gist_data():
    """Retrieve intersphinx gist contents."""
    log_append(f"Linkcheck run: {TIMESTAMP} UTC\n\n")
    resp = rq.get("https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209")
    log_append("Got gist page\n\n")
    data = resp.content.decode()
    return data


def gen_tuples_from_data(data):
    """Yield each tuple of mapping data from the data text."""
    mchs = list(pat_line.finditer(data))

    for sm in [pat_tuple.search(m.group(0)) for m in mchs]:
        sm = sm.group(0).replace("&#39;", "'")
        tup = eval(sm)
        log_append(tup[0] + "\n")
        yield tup

    log_append("\n")


def gen_mapping_tuples():
    """Retrieve intersphinx gist and yield mapping tuples."""
    data = get_gist_data()
    yield from gen_tuples_from_data(data)


def make_tuple_id(tup):
    """Generate pytest ID for mapping tuple."""
    return pat_domain.search(tup[0]).group(1)


@pytest.fixture(scope="session", params=gen_mapping_tuples(), ids=make_tuple_id)
def mapping_tuple(request):
    """Supply the mapping tuples singly to a test function."""
    return request.param


def test_mapping_root(mapping_tuple):
    """Check docs root link validity."""
    resp = rq.get(mapping_tuple[0])
    log_append(f"{mapping_tuple[0]}: {resp.status_code} {resp.reason}\n")
    assert resp.ok


def test_mapping_objects_inv(mapping_tuple):
    """Check docs objects.inv link validity."""
    inv_link = mapping_tuple[1] or (mapping_tuple[0].removesuffix("/") + "/objects.inv")
    inv = soi.Inventory(url=inv_link)
    log_append(f"{repr(inv)}\n")

    # Interestingly, (some?) module objects don't craft accurate URIs?
    data_obj = next(obj for obj in dropwhile(lambda o: o.role == "module", inv.objects))

    obj_link = mapping_tuple[0] + data_obj.uri_expanded
    obj_resp = rq.get(obj_link)
    log_append(f"{obj_link}: {obj_resp.status_code} {obj_resp.reason}\n")
    assert obj_resp.ok

    soup = BSoup(obj_resp.text, "html.parser")

    if anchor := obj_link.partition("#")[2]:
        anchor_check = soup.find_all("dt", id=anchor)
        log_append(f"Anchor '{anchor}' found? {bool(anchor_check)}\n\n")
        assert anchor_check
    else:
        log_append("No anchor in uri")
