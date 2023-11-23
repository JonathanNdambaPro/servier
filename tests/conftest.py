from pathlib import Path

import pytest

from app.schema import schema


@pytest.fixture
def path_file_clinical_trials() -> Path:
    path_clinical_trials = (
        Path(__file__).resolve().parents[1] / "file" / "clinical_trials.csv"
    )
    return path_clinical_trials


@pytest.fixture
def path_file_drugs() -> Path:
    path_clinical_trials = Path(__file__).resolve().parents[1] / "file" / "drugs.csv"
    return path_clinical_trials


@pytest.fixture
def path_file_pubmed_csv() -> Path:
    path_clinical_trials = Path(__file__).resolve().parents[1] / "file" / "pubmed.csv"
    return path_clinical_trials


@pytest.fixture
def path_file_pubmed_json() -> Path:
    path_clinical_trials = Path(__file__).resolve().parents[1] / "file" / "pubmed.json"
    return path_clinical_trials


@pytest.fixture
def read_file_clinical_trials():
    output = [
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
    ]

    return output


@pytest.fixture
def read_file_pubmed_csv():
    output = [
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
    ]
    return output


@pytest.fixture
def read_file_pubmed_json():
    output = [
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
    ]

    return output


@pytest.fixture
def read_file_drugs():
    output = [
        schema.Drugs(atccode="A04AD", drug="DIPHENHYDRAMINE"),
        schema.Drugs(atccode="S03AA", drug="TETRACYCLINE"),
        schema.Drugs(atccode="V03AB", drug="ETHANOL"),
        schema.Drugs(atccode="A03BA", drug="ATROPINE"),
        schema.Drugs(atccode="A01AD", drug="EPINEPHRINE"),
        schema.Drugs(atccode="6302001", drug="ISOPRENALINE"),
        schema.Drugs(atccode="R01AD", drug="BETAMETHASONE"),
    ]

    return output


@pytest.fixture
def read_file_drugs_reconciliated():
    output = [
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="A04AD", drug="DIPHENHYDRAMINE"),
            pubmed=[1, 2, 3],
            clinical_trials=["NCT01967433", "NCT04189588", "NCT04237091"],
            journals=["The Journal of pediatrics", "Journal of emergency nursing"],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="S03AA", drug="TETRACYCLINE"),
            pubmed=[4, 5, 6],
            clinical_trials=[],
            journals=[
                "Psychopharmacology",
                "American journal of veterinary research",
                "Journal of food protection",
            ],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="V03AB", drug="ETHANOL"),
            pubmed=[6],
            clinical_trials=[],
            journals=["Psychopharmacology"],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="A03BA", drug="ATROPINE"),
            pubmed=[],
            clinical_trials=[],
            journals=[],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="A01AD", drug="EPINEPHRINE"),
            pubmed=[8, 7],
            clinical_trials=["NCT04188184"],
            journals=[
                "Journal of emergency nursing",
                "The journal of allergy and clinical immunology. In practice",
            ],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="6302001", drug="ISOPRENALINE"),
            pubmed=[9],
            clinical_trials=[],
            journals=["Journal of photochemistry and photobiology. B, Biology"],
        ),
        schema.DrugsReconcilation(
            drug=schema.Drugs(atccode="R01AD", drug="BETAMETHASONE"),
            pubmed=[10, 11],
            clinical_trials=["NCT04153396"],
            journals=[
                "Hôpitaux Universitaires de Genève",
                "Journal of back and musculoskeletal rehabilitation",
                "The journal of maternal-fetal & neonatal medicine",
            ],
        ),
    ]

    return output
