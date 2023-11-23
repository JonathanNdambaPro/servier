import csv
import json
import typing as t
from collections import Counter
from pathlib import Path

import charset_normalizer
from google.cloud import storage
from loguru import logger
from pydantic import BaseModel, ValidationError

from app.config import config
from app.error import custom_error
from app.schema import schema

REFERENCE_EXTENTION_FILE = {".csv": csv.DictReader, ".json": json.load}
REFERENCE_SAVE_FILE = {".csv": csv.DictReader, ".json": json.load}


def check_encoding(file_path: Path):
    """
    Determines the encoding of a file by examining its contents.

    This function reads the first 10000 bytes of a file and uses the charset_normalizer library
    to detect the file's character encoding. It returns the detected encoding.

    Parameters
    ----------
    file_path : Path
        The path to the file whose encoding needs to be determined.

    Returns
    -------
    str
        The name of the detected encoding (e.g., 'utf-8', 'ascii', etc.), or `None` if
        the encoding could not be determined.

    Examples
    --------
    >>> from pathlib import Path
    >>> file_path = Path('example.txt')
    >>> encoding = check_encoding(file_path)
    >>> print(encoding)

    Notes
    -----
    The function reads only the first 10000 bytes of the file. This is usually sufficient
    to determine the encoding but may not work correctly for files with mixed encodings
    or unusual character sets.
    """
    with file_path.open("rb") as file:
        result = charset_normalizer.detect(file.read(10000))

    encoding = result["encoding"]
    return encoding


def json_handler_error_character(file_path: Path, error_position: int) -> json:
    """
    Handles and corrects a JSON decoding error by removing a problematic character in a JSON file.

    This function opens a JSON file, identifies a problematic character at a given position,
    removes that character, and then attempts to reload the JSON content. If the correction is successful,
    the modified JSON content is returned.

    Parameters
    ----------
    file_path : Path
        Path of the JSON file to be processed.
    error_position : int
        Position of the problematic character in the file.

    Returns
    -------
    json
        The JSON content after removing the problematic character and correcting the error.

    Raises
    ------
    json.JSONDecodeError
        If the modified content still cannot be decoded into JSON.

    Examples
    --------
    >>> from pathlib import Path
    >>> file_path = Path('example.json')
    >>> error_position = 50  # Assuming the error is at position 50
    >>> corrected_json = json_handler_error_character(file_path, error_position)
    >>> print(corrected_json)
    """
    with file_path.open("r", encoding="utf-8") as file:
        content_file = file.read()
        modify_content = (
            content_file[: error_position - 2] + content_file[error_position:]
        )

    jsonify_modify_content = json.loads(modify_content)
    return jsonify_modify_content


def read_file(
    file_path: Path, type_of_schema: str
) -> t.Tuple[t.List[str], t.List[str]]:
    """
    Reads a file and validates its content according to a specified schema.

    This function opens a file (CSV, JSON, etc.), reads its content, and validates each item
    against a predefined schema. Validated items are added to one list, while items that fail
    validation are added to another list for further processing.

    Parameters
    ----------
    file_path : Path
        Path of the file to read.
    type_of_schema : str
        Type of schema to use for validating the file's items.

    Returns
    -------
    tuple
        A tuple of two lists: the first containing the validated items, and the second
        containing the items that failed validation.

    Notes
    -----
    In case of a JSON decoding error, this function uses `json_handler_error_character`
    to correct the error before continuing with reading and validation.

    Examples
    --------
    >>> from pathlib import Path
    >>> file_path = Path('pubmed.json')
    >>> type_of_schema = 'pubmed'
    >>> valid_items, invalid_items = read_file(file_path, type_of_schema)
    >>> print(f"Valid items: {len(valid_items)}, Invalid items: {len(invalid_items)}")
    """
    if file_path.suffix not in REFERENCE_EXTENTION_FILE:
        message = "Extention of file must be in csv or json"
        logger.error(message)
        raise custom_error.ExtentionError(message=message)

    valid_items = []
    invalid_items = []

    encoding = check_encoding(file_path=file_path)
    with file_path.open(newline="", encoding=encoding) as file:
        try:
            reader_file = REFERENCE_EXTENTION_FILE[file_path.suffix](file)
        except json.JSONDecodeError as err:
            logger.error(f"Error message :{err}")
            reader_file = json_handler_error_character(file_path, err.pos)

        for row in reader_file:
            try:
                row_validated = config.REFERENCE_SCHEMA[type_of_schema](**row)
                valid_items.append(row_validated)
            except ValidationError as err:
                logger.error(f"Error for one element : {err}")
                invalid_items.append(row)
    return valid_items, invalid_items


def reconciliation_data(
    drug: schema.Drugs,
    elements_pubmed: t.List[schema.PubMed],
    elements_clinical_trials: t.List[schema.ClinicalTrials],
) -> json:
    """
    Performs data reconciliation between drug information and publications from PubMed and ClinicalTrials.

    This function filters PubMed and ClinicalTrials data based on the presence of the drug's name in their titles.
    It then aggregates unique IDs from these filtered entries and extracts journal names. The resulting data,
    including filtered PubMed IDs, ClinicalTrials IDs, and journal names, is encapsulated into a
    DrugsReconciliation object and returned.

    Parameters
    ----------
    drug : schema.Drugs
        The drug information object.
    elements_pubmed : List[schema.PubMed]
        A list of PubMed data entries.
    elements_clinical_trials : List[schema.ClinicalTrials]
        A list of ClinicalTrials data entries.

    Returns
    -------
    schema.DrugsReconcilation
        An object containing reconciled data: filtered PubMed and ClinicalTrials IDs, and journal names.

    Examples
    --------
    >>> drug = schema.Drugs(drug='Aspirin')
    >>> elements_pubmed = [schema.PubMed(id=1, title='Study on Aspirin', journal='Journal A')]
    >>> elements_clinical_trials = [schema.ClinicalTrials(id=2, scientific_title='Aspirin Clinical Trial', journal='Journal B')]
    >>> reconciliation_result = reconciliation_data(drug, elements_pubmed, elements_clinical_trials)
    >>> print(reconciliation_result)

    Notes
    -----
    The function expects that the `title` attribute in PubMed entries and `scientific_title` in ClinicalTrials
    entries are present. It performs a case-insensitive search for the drug's name in these titles.
    """
    elements_pubmed_filtred_id = {
        element_pubmed.id
        for element_pubmed in elements_pubmed
        if drug.drug.lower() in element_pubmed.title.lower()
    }

    elements_clinical_trials_filtred_id = {
        element_clinical_trials.id
        for element_clinical_trials in elements_clinical_trials
        if drug.drug.lower() in element_clinical_trials.scientific_title.lower()
    }

    elements_journals_from_pubmed = {
        element_journal.journal
        for element_journal in elements_pubmed
        if drug.drug.lower() in element_journal.title.lower()
    }

    elements_journals_from_clinical_trial = {
        element_journal.journal
        for element_journal in elements_clinical_trials
        if drug.drug.lower() in element_journal.scientific_title.lower()
    }

    elements_journals = (
        elements_journals_from_pubmed | elements_journals_from_clinical_trial
    )

    drug_reconciliation = schema.DrugsReconcilation(
        drug=drug,
        pubmed=elements_pubmed_filtred_id,
        clinical_trials=elements_clinical_trials_filtred_id,
        journals=elements_journals,
    )

    return drug_reconciliation.model_dump()


def save_json(data, file_path: Path):
    """
    Save data to a JSON file using the pathlib module.

    Parameters
    ----------
    data : dict
        The data to be saved in JSON format.
    file_path : Path
        The file path where the JSON file will be saved. Can be a string or a Path object.

    Returns
    -------
    None

    Examples
    --------
    >>> file_path = Path(__file__).resolve().parent / "file.json"
    >>> data = {"name": "John", "age": 30, "city": "New York"}
    >>> save_json(data, file_path)

    Notes
    -----
    The function will overwrite any existing file at the specified path without warning.
    Ensure the provided path is correct and the necessary permissions are available.
    """
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_file(data, file_path: Path, returned_format: str = "json") -> None:
    """
    Save given data to a specified file in a specified format.

    This function takes a list of data, standardizes it, and then saves it to a file.
    If elements in the data list are instances of BaseModel, they are first converted
    to a standardized format before saving.

    Parameters
    ----------
    data : list
        A list of data to be saved. Can contain objects of any type, including
        instances of BaseModel.
    file_path : Path
        The file path where the data should be saved. Should be a Path object from pathlib.
    returned_format : str, optional
        The file format for saving the data. Currently supported options are limited to 'json'.
        Default is 'json'.

    Returns
    -------
    None
        The function does not return anything but saves the data to the specified file.

    Examples
    --------
    >>> save_file(my_data, Path('/path/to/file.json'))

    Notes
    -----
    The function relies on the `model_dump()` method for instances of BaseModel for
    standardization before saving. Ensure that this method is properly defined in
    the BaseModel definition.
    """
    data_standardized = []
    for element in data:
        if isinstance(element, BaseModel):
            element = element.model_dump()
        data_standardized.append(element)

    if returned_format == "json":
        save_json(data_standardized, file_path)


def upload_blob(bucket_name: str, local_file_name: str, gcs_file_name: str) -> None:
    """
    Upload a file to the specified Google Cloud Storage bucket.

    Parameters
    ----------
    bucket_name : str
        The name of the Google Cloud Storage bucket.
    local_file_name : str
        The file path of the file to upload.
    gcs_file_name : str
        The destination object name in the bucket.

    Returns
    -------
    None

    Examples
    --------
    >>> upload_blob("my-bucket", "local/path/to/file.txt", "destination/path/in/bucket.txt")

    Notes
    -----
    Ensure that the Google Cloud credentials are properly set up and that the bucket
    name provided exists and is accessible with the given credentials.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_name)
    blob.upload_from_filename(local_file_name)


def download_blob(bucket_name: str, local_file_name: str, gcs_file_name: str) -> None:
    """
    Download a blob from the specified Google Cloud Storage bucket to a local file.

    Parameters
    ----------
    bucket_name : str
        The name of the Google Cloud Storage bucket.
    local_file_name : str
        The destination file path on the local machine.
    gcs_file_name : str
        The source blob name in the bucket (path of the file in the bucket).


    Returns
    -------
    None

    Examples
    --------
    >>> download_blob("my-bucket", "local/path/to/save/file.txt", "path/in/bucket/file.txt")

    Notes
    -----
    Ensure that the Google Cloud credentials are properly set up and that the bucket
    name provided exists and is accessible with the given credentials. The user must
    have read permissions on the specified blob.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_name)
    blob.download_to_filename(local_file_name)


REFERENCE_GCS = {"push": upload_blob, "pull": download_blob}


def gcs_handler_blob(type_of_operation: str, *args, **kwargs) -> None:
    """
    Handle blob operations (upload or download) for Google Cloud Storage.

    This function serves as a centralized handler to perform either upload or download operations
    on Google Cloud Storage, based on the specified operation type. It utilizes a mapping dictionary
    'REFERENCE_GCS' to call the appropriate function ('upload_blob' or 'download_blob').

    Parameters
    ----------
    type_of_operation : str
        The type of operation to perform. Acceptable values are 'push' for upload and 'pull' for download.
    *args
        Positional arguments to pass to the chosen upload or download function.
    **kwargs
        Keyword arguments to pass to the chosen upload or download function.

    Returns
    -------
    None

    Examples
    --------
    >>> gcs_handler_blob("push", "my-bucket", "local/path/to/file.txt", "destination/path/in/bucket.txt")
    >>> gcs_handler_blob("pull", "my-bucket", "local/path/to/save/file.txt", "path/in/bucket/file.txt")

    Notes
    -----
    - For a 'push' operation, the expected arguments are the bucket name, the local file path to upload,
      and the GCS file name (the destination blob name in the bucket).
    - For a 'pull' operation, the expected arguments are the bucket name, the GCS file name (the source blob name in the bucket),
      and the local file path for the downloaded file.
    - Ensure that Google Cloud credentials are properly set up and the specified bucket exists and is accessible.
    - For downloading, the user must have read permissions on the specified blob.
    """
    REFERENCE_GCS[type_of_operation](*args, **kwargs)


def journal_most_cited(file_path: Path) -> t.List[str]:
    """
    Reads a JSON file containing drug reconciliation data and identifies the most cited journals.

    This function parses a specified JSON file to extract drug reconciliation data,
    then analyzes the frequency of journal citations within the data. It returns a list
    of the most cited journals.

    Parameters
    ----------
    file_path : Path
        A Path object representing the file path of the JSON file to be read.

    Returns
    -------
    List[str]
        A list of strings, where each string is the name of a journal that has the highest
        number of citations in the dataset.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    json.JSONDecodeError
        If the file is not a valid JSON.

    Notes
    -----
    This function depends on the `read_file` function for reading and parsing the JSON file.
    The structure of the JSON file and the schema 'drugs_reconcilation' should be
    predefined and compatible with the `read_file` function.
    """

    all_journal = []
    top_journal = []

    drugs_reconcilation, _ = read_file(
        file_path=file_path, type_of_schema="drugs_reconcilation"
    )

    for element in drugs_reconcilation:
        all_journal.extend(element.journals)

    counter_occurrences = dict(Counter(all_journal))
    max_occurences = max(counter_occurrences.values())

    for element in counter_occurrences:
        if counter_occurrences[element] == max_occurences:
            top_journal.append(element)

    return top_journal
