"""
Utility to create resources dictionaries from csv or tsv files.
"""
import logging
from datetime import datetime as dt
from functools import reduce
from pathlib import Path

from shared_resources.dictionaries.utils import load_json

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent / 'data'
HPO_JSON = BASE_DIR / "hpo_dictionary.json"
ROSETTA_SYMBOLS_JSON = BASE_DIR / "rosetta_symbol_to_hgnc_id.json"
ROSETTA_IDS_JSON = BASE_DIR / "rosetta_hgnc_id_to_symbol.json"


def get_raw_hpo_dict():
    """Return the dictionary of HPO terms without applying any modification."""
    return load_json(HPO_JSON)


class ResourcesDictionaries:

    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout or 1200
        self._load()

    @staticmethod
    def get_fullname(hpo):
        fullname = hpo["name_id"]
        synonyms = [[
            w for w in s.split(" ")
            if w.lower() not in [x.lower() for x in fullname.split(" ")]
        ] for s in hpo["synonyms"] if s and not s.startswith("HP:")]
        return (f"{fullname} " +
                (" ".join(sorted(set(reduce(list.__add__, synonyms))))
                 if synonyms else "")).lower()

    def _load(self):
        hpo_dict = load_json(HPO_JSON)
        self.hpo_dict = {
            k: {
                "name": v["name_id"],
                "full_name": self.get_fullname(v),
                "children": v.get("children", [])
            }
            for k, v in hpo_dict.items()
        }
        self.symbol_to_hgnc = load_json(ROSETTA_SYMBOLS_JSON)
        self.hgnc_to_symbol = load_json(ROSETTA_IDS_JSON)
        self.last_updated = dt.now()

    def _reload(self):
        if (dt.now() - self.last_updated).seconds > self.timeout:
            self._load()

    @property
    def hpo_list(self):
        self._reload()
        hpo_dict_list = [{
            "id": k,
            "name": v["name"],
            "full_name": v["full_name"],
            "synonyms": v.get("synonyms", []),
            "children": v.get("children", []),
        } for k, v in self.hpo_dict.items()]
        return sorted(hpo_dict_list, key=lambda h: h.get("id"))

    def get_hpo_items(self, hpo_list):
        return [{
            "id": hpo_id,
            "name": self.hpo_dict.get(hpo_id, {}).get("name"),
            "full_name": self.hpo_dict.get(hpo_id, {}).get("full_name"),
            "synonyms": self.hpo_dict.get(hpo_id, {}).get("synonyms", []),
            "children": self.hpo_dict.get(hpo_id, {}).get("children", []),
        } for hpo_id in sorted(set(hpo_list))]


resources_dictionaries = ResourcesDictionaries()
