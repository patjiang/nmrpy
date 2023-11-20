import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .fidobject import FIDObject
from .processingsteps import ProcessingSteps
from .identity import Identity
from .fidarray import FIDArray
from .parameters import Parameters


@forge_signature
class Experiment(sdRDM.DataModel):
    """Rohdaten -> Zwischenschritte nur nennen + interessante Parameter -> Endergebnis; Peaklist + Rangelist; rapidly pulsed (if then +calibration factor) vs fully relaxed
    Also preparation of EnzymeML doc https://github.com/EnzymeML/enzymeml-specifications/@AbstractSpecies, https://github.com/EnzymeML/enzymeml-specifications/@Protein, https://github.com/EnzymeML/enzymeml-specifications/@Reactant
    """

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    name: str = Field(
        ...,
        description="A descriptive name for the overarching experiment.",
    )

    fid: List[FIDObject] = Field(
        description="A single NMR spectrum.",
        default_factory=ListPlus,
        multiple=True,
    )

    fid_array: Optional[FIDArray] = Field(
        default=None,
        description="Multiple NMR spectra to be processed together.",
    )
    __repo__: Optional[str] = PrivateAttr(default="https://github.com/NMRPy/nmrpy")
    __commit__: Optional[str] = PrivateAttr(
        default="dec2cda6676f8d04070715fe079ed786515ea918"
    )

    def add_to_fid(
        self,
        raw_data: List[str] = ListPlus(),
        processed_data: List[Union[str, float]] = ListPlus(),
        nmr_parameters: Optional[Parameters] = None,
        processing_steps: Optional[ProcessingSteps] = None,
        peak_identities: List[Identity] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'FIDObject' to attribute fid

        Args:
            id (str): Unique identifier of the 'FIDObject' object. Defaults to 'None'.
            raw_data (): Complex spectral data from numpy array as string of format `{array.real}+{array.imag}j`.. Defaults to ListPlus()
            processed_data (): Processed data array.. Defaults to ListPlus()
            nmr_parameters (): Contains commonly-used NMR parameters.. Defaults to None
            processing_steps (): Contains the processing steps performed, as well as the parameters used for them.. Defaults to None
            peak_identities (): Container holding and mapping integrals resulting from peaks and their ranges to EnzymeML species.. Defaults to ListPlus()
        """
        params = {
            "raw_data": raw_data,
            "processed_data": processed_data,
            "nmr_parameters": nmr_parameters,
            "processing_steps": processing_steps,
            "peak_identities": peak_identities,
        }
        if id is not None:
            params["id"] = id
        self.fid.append(FIDObject(**params))
        return self.fid[-1]
