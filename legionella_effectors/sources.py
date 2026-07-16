import csv
import io
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .config import PATHOGENS3D_URL, UNIPROT_URL


def _request(url, params=None, retries=3):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "legionella-effectors/0.1"})
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(request, timeout=90)
        except (urllib.error.URLError, TimeoutError):
            if attempt + 1 == retries:
                raise
            time.sleep(2**attempt)


def fetch_uniprot(query):
    """Return all UniProtKB JSON records for a query, following Link pagination."""
    params = {"query": query, "format": "json", "size": 500}
    response = _request(UNIPROT_URL, params)
    records = []
    while response:
        payload = json.load(response)
        records.extend(payload.get("results", []))
        link = response.headers.get("Link", "")
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        response.close()
        response = _request(match.group(1)) if match else None
    return records


def fetch_uniprot_accessions(accessions):
    accessions = sorted({x for x in accessions if x})
    records = []
    for start in range(0, len(accessions), 80):
        query = " OR ".join(f"accession:{x}" for x in accessions[start:start + 80])
        records.extend(fetch_uniprot(f"({query})"))
    return records


def fetch_pathogens3d():
    response = _request(PATHOGENS3D_URL)
    text = response.read().decode("utf-8-sig")
    response.close()
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))

