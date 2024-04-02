from dataclasses import dataclass

type geometry = list[str]
type geolocation = tuple[float, float]

@dataclass
class CellTower:
    """This class defines a unique structure for cell towers."""
    id: int                 # Unique number used to identify the GSM base transceiver station
    mcc: int                # Unique number for the country with the GSM net
    mnc: int                # Number used to uniquely identify the GSM network operator
    radio: str              # generation of broadband cellular network technology (Eg. LTE, GSM)
    lac: int                # Location Area Code
    lon: geolocation        # Longitude and Latitude: geographic coordinates.
    range: int              # Approximate area within which the cell could be
    traffic: float = 0.0    # Traffic load of the cell tower
    priority: int  = 0      # Priority of the cell tower


@dataclass
class Road:
    """This class defines a unique structure for a road"""
    id: int
    country: object
    geometry: geometry