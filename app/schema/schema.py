import re
import typing as t

from pydantic import BaseModel, Field, field_validator


class ClinicalTrials(BaseModel):
    """
    A model representing a clinical trial record.

    Attributes
    ----------
    id : str
        A unique identifier for the clinical trial.
    scientific_title : str
        The scientific title of the trial, describing the study in technical terms.
    date : str
        The date on which the trial information was published or updated. Should be in a standard date format.
    journal : str
        The name of the journal where the trial findings or details are published.
    """

    id: str = Field(min_length=3, pattern=r"^NCT.*$")
    scientific_title: str
    date: str
    journal: str

    @field_validator("scientific_title", "journal")
    @classmethod
    def check_alphanumeric(cls, value: str) -> str:
        """
        Removes non-alphanumeric characters from the provided string.

        This method is designed to clean fields like scientific_title and journal in the ClinicalTrials class.
        It uses a regular expression to identify and remove characters represented by hexadecimal codes,
        which are typically non-alphanumeric. This ensures that the fields only contain readable text characters.

        Parameters
        ----------
        value : str
            The string to be cleaned of non-alphanumeric characters.

        Returns
        -------
        str
            The cleaned string with non-alphanumeric characters removed.
        """
        pattern = r"\\x[0-9a-fA-F]{2}"
        value = re.sub(pattern, "", value)
        return value


class Drugs(BaseModel):
    """
    A model representing information about a specific drug.

    Attributes
    ----------
    atccode : str
        The Anatomical Therapeutic Chemical (ATC) classification system code, which classifies the drug based on its therapeutic and chemical characteristics.
    drug : str
        The common name or designation of the drug.
    """

    atccode: str
    drug: str


class PubMed(BaseModel):
    """
    A model representing a publication record from PubMed.

    Attributes
    ----------
    id : int
        A unique identifier for the publication in the PubMed database.
    title : str
        The title of the publication, providing a concise summary of the content.
    date : str
        The date when the publication was released or last updated. Should be in a standard date format.
    journal : str
        The name of the journal in which the publication appeared.
    """

    id: int
    title: str
    date: str
    journal: str


class DrugsReconcilation(BaseModel):
    """
    A model representing information about a specific drug.

    Attributes
    ----------
    atccode : str
        The Anatomical Therapeutic Chemical (ATC) classification system code, which classifies the drug based on its therapeutic and chemical characteristics.
    drug : str
        The common name or designation of the drug.
    """

    drug: Drugs
    pubmed: t.List[int]
    clinical_trials: t.List[str]
    journals: t.List[str]
