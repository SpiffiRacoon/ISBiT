from enum import Enum

class VersionName(Enum):
    DATA_FILE = "data_file"
    FIRST_RUN = "cluster"
    LATTER_RUN = "model"

exponent = 7

def _version_multiplier(num: int) -> int:
    return num * 10**exponent

version_to_number = {
    VersionName.DATA_FILE: 0,
    VersionName.FIRST_RUN: _version_multiplier(1),
    VersionName.LATTER_RUN: _version_multiplier(2)
}

def get_version_name_exponent() -> int:
    return exponent

def version_name_to_number(version_name: VersionName) -> int:
    return version_to_number[version_name]


def highest_version_number() -> int:
    return max(version_to_number.values())

def next_version_number(version_name: VersionName) -> int:
    done = False
    for key in version_to_number:
        if done:
            return version_to_number[key]
        if key == version_name:
            done = True

    if done:
        raise Exception("Error: version_name is the last version")

    raise Exception("Error: version_name is not in version_to_number")
