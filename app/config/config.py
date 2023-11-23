from app.schema import schema

REFERENCE_SCHEMA = {
    "clinical_trials": schema.ClinicalTrials,
    "drugs": schema.Drugs,
    "pubmed": schema.PubMed,
    "drugs_reconcilation": schema.DrugsReconcilation,
}

EXTENTIONS = {".json", ".csv"}
