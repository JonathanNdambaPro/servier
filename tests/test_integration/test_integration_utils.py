import shutil
from pathlib import Path

import pytest
from google.cloud import storage

from app.schema import schema
from app.utils import utils


def test_read_file_extention_error():
    path_file_with_bad_extention = Path(__file__).resolve().parent / "some_file.txt"
    with pytest.raises(Exception, match=r"Extention of file must be in csv or json"):
        utils.read_file(path_file_with_bad_extention, "pubmed")


@pytest.mark.parametrize(
    "expected",
    [
        schema.ClinicalTrials(
            id="NCT01967433",
            scientific_title="Use of Diphenhydramine as an Adjunctive Sedative for Colonoscopy in Patients Chronically on Opioids",
            date="1 January 2020",
            journal="Journal of emergency nursing",
        ),
        schema.ClinicalTrials(
            id="NCT04189588",
            scientific_title="Phase 2 Study IV QUZYTTIR™ (Cetirizine Hydrochloride Injection) vs V Diphenhydramine",
            date="1 January 2020",
            journal="Journal of emergency nursing",
        ),
        schema.ClinicalTrials(
            id="NCT04237090",
            scientific_title="  ",
            date="1 January 2020",
            journal="Journal of emergency nursing",
        ),
        schema.ClinicalTrials(
            id="NCT04237091",
            scientific_title="Feasibility of a Randomized Controlled Clinical Trial Comparing the Use of Cetirizine to Replace Diphenhydramine in the Prevention of Reactions Related to Paclitaxel",
            date="1 January 2020",
            journal="Journal of emergency nursing",
        ),
        schema.ClinicalTrials(
            id="NCT04153396",
            scientific_title="Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or  Laminectomy",
            date="1 January 2020",
            journal="Hôpitaux Universitaires de Genève",
        ),
        schema.ClinicalTrials(
            id="NCT03490942",
            scientific_title="Glucagon Infusion in T1D Patients With Recurrent Severe Hypoglycemia: Effects on Counter-Regulatory Responses",
            date="25/05/2020",
            journal="",
        ),
        schema.ClinicalTrials(
            id="NCT04188184",
            scientific_title="Tranexamic Acid Versus Epinephrine During Exploratory Tympanotomy",
            date="27 April 2020",
            journal="Journal of emergency nursing",
        ),
    ],
)
def test_read_file_extention_clinical_trial(path_file_clinical_trials, expected):
    output_clinical, _ = utils.read_file(path_file_clinical_trials, "clinical_trials")
    assert expected in output_clinical


@pytest.mark.parametrize(
    "expected",
    [
        schema.PubMed(
            id=1,
            title="A 44-year-old man with erythema of the face diphenhydramine, neck, and chest, weakness, and palpitations",
            date="01/01/2019",
            journal="Journal of emergency nursing",
        ),
        schema.PubMed(
            id=2,
            title="An evaluation of benadryl, pyribenzamine, and other so-called diphenhydramine antihistaminic drugs in the treatment of allergy.",
            date="01/01/2019",
            journal="Journal of emergency nursing",
        ),
        schema.PubMed(
            id=3,
            title="Diphenhydramine hydrochloride helps symptoms of ciguatera fish poisoning.",
            date="02/01/2019",
            journal="The Journal of pediatrics",
        ),
        schema.PubMed(
            id=4,
            title="Tetracycline Resistance Patterns of Lactobacillus buchneri Group Strains.",
            date="01/01/2020",
            journal="Journal of food protection",
        ),
        schema.PubMed(
            id=5,
            title="Appositional Tetracycline bone formation rates in the Beagle.",
            date="02/01/2020",
            journal="American journal of veterinary research",
        ),
        schema.PubMed(
            id=6,
            title="Rapid reacquisition of contextual fear following extinction in mice: effects of amount of extinction, tetracycline acute ethanol withdrawal, and ethanol intoxication.",
            date="2020-01-01",
            journal="Psychopharmacology",
        ),
        schema.PubMed(
            id=7,
            title="The High Cost of Epinephrine Autoinjectors and Possible Alternatives.",
            date="01/02/2020",
            journal="The journal of allergy and clinical immunology. In practice",
        ),
        schema.PubMed(
            id=8,
            title="Time to epinephrine treatment is associated with the risk of mortality in children who achieve sustained ROSC after traumatic out-of-hospital cardiac arrest.",
            date="01/03/2020",
            journal="The journal of allergy and clinical immunology. In practice",
        ),
    ],
)
def test_read_file_pubmed_csv(path_file_pubmed_csv, expected):
    output_pubmed_csv, _ = utils.read_file(path_file_pubmed_csv, "pubmed")
    assert expected in output_pubmed_csv


@pytest.mark.parametrize(
    "expected",
    [
        schema.PubMed(
            id=9,
            title="Gold nanoparticles synthesized from Euphorbia fischeriana root by green route method alleviates the isoprenaline hydrochloride induced myocardial infarction in rats.",
            date="01/01/2020",
            journal="Journal of photochemistry and photobiology. B, Biology",
        ),
        schema.PubMed(
            id=10,
            title="Clinical implications of umbilical artery Doppler changes after betamethasone administration",
            date="01/01/2020",
            journal="The journal of maternal-fetal & neonatal medicine",
        ),
        schema.PubMed(
            id=11,
            title="Effects of Topical Application of Betamethasone on Imiquimod-induced Psoriasis-like Skin Inflammation in Mice.",
            date="01/01/2020",
            journal="Journal of back and musculoskeletal rehabilitation",
        ),
        schema.PubMed(
            id=12,
            title="Comparison of pressure release, phonophoresis and dry needling in treatment of latent myofascial trigger point of upper trapezius muscle.",
            date="01/03/2020",
            journal="Journal of back and musculoskeletal rehabilitation",
        ),
    ],
)
def test_read_file_pubmed_json(path_file_pubmed_json, expected):
    output_pubmed_json, _ = utils.read_file(path_file_pubmed_json, "pubmed")
    assert expected in output_pubmed_json


@pytest.mark.parametrize(
    "expected",
    [
        schema.Drugs(atccode="A04AD", drug="DIPHENHYDRAMINE"),
        schema.Drugs(atccode="S03AA", drug="TETRACYCLINE"),
        schema.Drugs(atccode="V03AB", drug="ETHANOL"),
        schema.Drugs(atccode="A03BA", drug="ATROPINE"),
        schema.Drugs(atccode="A01AD", drug="EPINEPHRINE"),
        schema.Drugs(atccode="6302001", drug="ISOPRENALINE"),
        schema.Drugs(atccode="R01AD", drug="BETAMETHASONE"),
    ],
)
def test_read_file_drugs(path_file_drugs, expected):
    output_pubmed_json, _ = utils.read_file(path_file_drugs, "drugs")
    assert expected in output_pubmed_json


def test_reconciliation_data(
    read_file_pubmed_csv, read_file_pubmed_json, read_file_clinical_trials
):
    drug = schema.Drugs(atccode="A04AD", drug="DIPHENHYDRAMINE")
    elements_pubmed_validated = read_file_pubmed_json + read_file_pubmed_csv
    output_data_reconciliated = utils.reconciliation_data(
        drug=drug,
        elements_pubmed=elements_pubmed_validated,
        elements_clinical_trials=read_file_clinical_trials,
    )
    assert {"atccode": "A04AD", "drug": "DIPHENHYDRAMINE"} == output_data_reconciliated[
        "drug"
    ]
    assert [1, 2, 3] == output_data_reconciliated["pubmed"]


def test_save_json_folder_doesnt_exist():
    data = {"lol": "lol"}
    path_file = Path(__file__).resolve().parent / "folder_test" / "trash_data.json"

    utils.save_json(data, path_file)

    assert path_file.exists
    shutil.rmtree(path_file.parent)


def test_save_json_folder_exist():
    data = {"lol": "lol"}
    path_file = Path(__file__).resolve().parent / "folder_test" / "trash_data.json"
    path_file.parent.mkdir()
    utils.save_json(data, path_file)
    assert path_file.exists
    shutil.rmtree(path_file.parent)


def test_save_file(read_file_clinical_trials):
    path_file = Path(__file__).resolve().parent / "folder_test" / "trash_data.json"
    utils.save_file(read_file_clinical_trials, path_file)
    assert path_file.exists
    shutil.rmtree(path_file.parent)


def test_upload_blob(read_file_clinical_trials):
    path_file = Path(__file__).resolve().parent / "folder_test" / "trash_data.json"
    bucket_name = "servier-bronze"
    path_gcs_file = "test/trash_data.json"
    utils.save_file(read_file_clinical_trials, path_file)
    utils.upload_blob(bucket_name, path_file, path_gcs_file)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path_gcs_file)

    assert blob.exists()
    shutil.rmtree(path_file.parent)
    blob.delete()


def test_download_blob(read_file_clinical_trials):
    path_file = Path(__file__).resolve().parent / "folder_test" / "trash_data.json"
    bucket_name = "servier-bronze"
    path_gcs_file = "test/trash_data.json"

    utils.save_file(read_file_clinical_trials, path_file)
    utils.upload_blob(bucket_name, path_file, path_gcs_file)
    path_file.unlink()

    utils.download_blob(bucket_name, str(path_file), path_gcs_file)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path_gcs_file)

    assert path_file.exists()
    shutil.rmtree(path_file.parent)
    blob.delete()
