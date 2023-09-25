import sdRDM

from typing import Optional, Union, List
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from pydantic.types import FrozenSet

from .processingsteps import ProcessingSteps
from .abstractspecies import AbstractSpecies
from .protein import Protein
from .identity import Identity
from .parameters import Parameters
from .reactant import Reactant


@forge_signature
class FID(sdRDM.DataModel):
    """Container for a single NMR spectrum."""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("fidINDEX"),
        xml="@id",
    )

    raw_data: List[str] = Field(
        description=(
            "Complex spectral data from numpy array as string of format"
            " `{array.real}+{array.imag}j`."
        ),
        default_factory=ListPlus,
        multiple=True,
    )

    processed_data: List[Union[str, float]] = Field(
        description="Processed data array.",
        default_factory=ListPlus,
        multiple=True,
    )

    nmr_parameters: Optional[Parameters] = Field(
        default=Parameters(),
        description="Contains commonly-used NMR parameters.",
    )

    processing_steps: Optional[ProcessingSteps] = Field(
        default=ProcessingSteps(),
        description=(
            "Contains the processing steps performed, as well as the parameters used"
            " for them."
        ),
    )

    peak_identities: List[Identity] = Field(
        description=(
            "Container holding and mapping integrals resulting from peaks and their"
            " ranges to EnzymeML species."
        ),
        default_factory=ListPlus,
        multiple=True,
    )

    def add_to_peak_identities(
        self,
        name: str,
        enzymeml_species: Union[AbstractSpecies, Protein, Reactant, None] = None,
        associated_peaks: List[float] = ListPlus(),
        associated_ranges: List[FrozenSet] = ListPlus(),
        associated_integrals: List[float] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Identity' to attribute peak_identities

        Args:
            id (str): Unique identifier of the 'Identity' object. Defaults to 'None'.
            name (): Descriptive name for the species.
            enzymeml_species (): A species object from an EnzymeML document.. Defaults to None
            associated_peaks (): Peaks belonging to the given species. Defaults to ListPlus()
            associated_ranges (): Sets of ranges belonging to the given peaks. Defaults to ListPlus()
            associated_integrals (): Integrals resulting from the given peaks and ranges of a species. Defaults to ListPlus()
        """

        params = {
            "name": name,
            "enzymeml_species": enzymeml_species,
            "associated_peaks": associated_peaks,
            "associated_ranges": associated_ranges,
            "associated_integrals": associated_integrals,
        }

        if id is not None:
            params["id"] = id

        self.peak_identities.append(Identity(**params))

        return self.peak_identities[-1]
