import logging
import time

from shared_resources.dictionaries import ResourcesDictionaries, get_raw_hpo_dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_gene_dictionaries():
    gd = ResourcesDictionaries(timeout=10)
    last_updated = gd.last_updated
    assert isinstance(gd.hpo_dict, dict)
    assert isinstance(gd.hpo_list, list)
    _ = gd.hpo_list
    assert last_updated == gd.last_updated
    time.sleep(11)
    _ = gd.hpo_list
    assert (gd.last_updated - last_updated).seconds > 10


def test_get_raw_hpo_dict():
    """Small test, mostly to make sure that no exceptions are raised when calling the function."""
    assert isinstance(get_raw_hpo_dict(), dict)
