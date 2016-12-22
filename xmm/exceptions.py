from urllib.error import URLError


class HashMismatchError(ValueError):
    """
    Raise when a file hash mismatches
    """


class PackageLookupError(LookupError):
    """
    Raise when Package does not exist in Repository
    """


class PackageMetadataWarning(Warning):
    """
    Raise when Package installs from a URL and has no metadata associated with it.
    """


class PackageNotTrackedWarning(Warning):
    """
    Raise when Package is not tracked in the local db
    """


class RepositoryLookupError(LookupError):
    """
    Raise when Repository lookup fails
    """


class RepositoryUpdateError(URLError):
    """
    Raise when Repository update fails
    """


class ServerLookupError(LookupError):
    """
    Raise when Server lookup fails
    """
