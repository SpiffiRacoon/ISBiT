# own
from ..types import VersionName

def get_collection_name(dataset_name: str, version_name: VersionName, version_number: str, label: bool = False) -> str:
    collection = f"{dataset_name}_{version_name.value}_{version_number}{'_labeled' if label else ''}"
    return collection
