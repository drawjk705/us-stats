class CensusDoesNotExistException(Exception):
    """
    Thrown during the healthcheck if the requested
    dataset/survey does not exist.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidQueryException(Exception):
    """
    Thrown if an invalid query was made to the Census API.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)