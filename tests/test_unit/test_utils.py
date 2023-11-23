from pathlib import Path

import pytest

import app
from app.utils import utils


def test_check_encoding(
    path_file_clinical_trials,
    path_file_drugs,
    path_file_pubmed_csv,
    path_file_pubmed_json,
):
    encoding_clinical_trials = utils.check_encoding(path_file_clinical_trials)
    encoding_file_drugs = utils.check_encoding(path_file_drugs)
    encoding_file_pubmed_csv = utils.check_encoding(path_file_pubmed_csv)
    encoding_file_pubmed_json = utils.check_encoding(path_file_pubmed_json)

    assert encoding_clinical_trials == "utf-8"
    assert encoding_file_drugs == "ascii"
    assert encoding_file_pubmed_csv == "ascii"
    assert encoding_file_pubmed_json == "ascii"


def test_journal_most_cited(mocker, read_file_drugs_reconciliated):
    file_path_not_exist = Path(__file__).resolve().parent / "file_not_exist.json"
    mocker.patch(
        "app.utils.utils.read_file", return_value=(read_file_drugs_reconciliated, None)
    )
    top_journal = utils.journal_most_cited(file_path_not_exist)

    assert top_journal == ["Journal of emergency nursing", "Psychopharmacology"]
