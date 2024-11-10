from ..types import VersionName, version_name_to_number, highest_version_number, get_version_name_exponent
from typing import Self
from .getters import get_latest_version_number


class DataVersion:
    """
    Class to handle the data version, if only `dataset_name` is given, the latest version will be taken.
    """
    def __init__(
        self,
        dataset_name: str,
        version_number: int | None = None,
        version_name: VersionName | None = None,
        version_name_number: int | None = None,
        label: bool = False,
    ) -> None:
        self.dataset_name = dataset_name

        if version_number is not None:
            self.current_version = version_number
        elif version_name is None:
            # Just taking the latest version, no arguments given
            self.current_version: int = self.latest_version
        else:
            # Another version then the default
            self.set_version(version_name, version_number, label)


    def set_version(
        self, version_name: VersionName, version_name_number: int | None = None, label: bool = False
    ) -> None:
        """
        To get the latest version of a collection, it is more efficient to be able to sort by a number.
        This will set value of `self.set_version`

        0 000000 0 (Format of versions)
        0 - this is version as in the version_name
          000000 - this is the version number (The iteration of the model or cluster..., max iterations is 999999)
                 0 - this is a indicator if it is labeled or not

        Ex)
        0 - <filename> (datafile)
        10000000 - <filename>_cluster_0
        20000041 - <filename>_model_4_labeled
        10000011 - <filename>_cluster_1_labeled
        10001031 - <filename>_cluster_103_labeled
        """
        version_number = 0
        if version_name is VersionName.DATA_FILE:
            self.current_version = 0
            return None

        if self.current_version == 0:
            raise Exception("Error: Cannot set any versions of datafile")

        self.current_version += version_name_to_number(version_name)

        if version_name_number is None:
            print(version_name)
            raise Exception("Error: version_name_number is required when version_name is not DATA_FILE")

        version_number += int(version_name_number) * 10

        if label:
            version_number += 1

        self.current_version = version_number


    def upgrade(
        self, automatic: bool = False, major: bool = False, minor: bool = False, label: bool = False, copy: bool = False
    ) -> Self | "DataVersion":
        """
        The new version will be set as the current version.

        Major upgrade => This is when going from 1.0.0 to 2.0.0 (Cluster to Model) or (Datafile to Cluster)
        Minor upgrade => This is when going from 1.0.0 to 1.1.0 (Cluster to Cluster) or (Model to Model)
        Label upgrade => This is when going from 1.0.0 to 1.0.1 (Cluster to Cluster) or (Model to Model)
        Automatic upgrade => Steps: From Datafile to Cluster to Model to new minor version of Model.
            Automatic versioning will not have minor versions of Datafile or Cluster.

        If trying to upgrade to higher version than allowed, it will raise an exception.

        Default:
            Returns the same object, but with the version upgraded.
            Ex)
              x = DataVersion(filename)
              x.version => 2.2.0
              x.upgrade(label=True)
              x.version => 2.2.1

        copy = True:
            Returns a new object with the version upgraded.
            Ex)
            x = DataVersion(filename)
            x.version => 2.2.0
            y = x.downgrade(label=True, copy=True)
            x.version => 2.2.0
            y.version => 2.2.1
        """
        if (self.current_version == 0) and (not major) and (not automatic):
            raise Exception("Error: Cannot label or minor upgrade datafile.")

        instance = self
        if copy:
            print("In copy")
            instance = self.copy()

        version_exponent = get_version_name_exponent()

        if automatic:
            if instance.current_version < version_name_to_number(VersionName.FIRST_RUN):
                instance.current_version = version_name_to_number(VersionName.FIRST_RUN)
            elif instance.current_version < version_name_to_number(VersionName.LATTER_RUN):
                instance.current_version = version_name_to_number(VersionName.LATTER_RUN)
            else:
                instance.current_version += 10
            return instance

        if (label is True) and (self.current_version % 2 == 0):
            instance.current_version += 1

        if major and (self.current_version > highest_version_number()):
            raise Exception("Error: Trying to upgrade to higher version than allowed.")

        if major:
            prev_major = instance.current_version // (10 ** version_exponent)
            instance.current_version = (prev_major + 1) * (10 ** version_exponent)

        if minor:
            instance.current_version += 10

        return instance


    def downgrade(self, copy: bool = False) -> Self | "DataVersion":
        """
        The previous version will be set as the current version.

        Default:
            Returns the same object, but with the version downgraded.
            Ex)
              x = DataVersion(filename)
              x.version => 2.2.1
              x.downgrade()
              x.version => 2.2.0

        copy = True:
            Returns a new object with the version downgraded.
            Ex)
            x = DataVersion(filename)
            x.version => 2.2.1
            y = x.downgrade(copy=True)
            x.version => 2.2.1
            y.version => 2.2.0
        """
        print("[WARNING] VersionedData.downgrade is not implemented yet.")

        return self


    def copy(self) -> "DataVersion":
        """
        Retruns a new object with the same version.
        """

        x = DataVersion(dataset_name=(self.dataset_name), version_number=int(self.current_version))
        return x


    @property
    def version_name(self) -> str:
        """
        Returns the name of the collection.
        """
        return f"{self.dataset_name}_{self.current_version}"


    @property
    def latest_version(self) -> int:
        return get_latest_version_number(self.dataset_name)


    @property
    def version(self) -> int:
        """
        Alias for current_version.
        """
        return self.current_version


    @property
    def about_dict(self) -> dict:
        """
        Returns a dictionary with the information of the version.
        """
        return {
            "filename": self.dataset_name,
            "version": self.current_version,
        }
