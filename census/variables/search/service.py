from census.log.factory import ILoggerFactory
from census.utils.timer import timer
from census.variables.repository.interface import IVariableRepository
from census.variables.search.interface import IVariableSearchService
from census.variables.models import GroupCode
import pandas as pd

from logging import Logger


class VariableSearchService(IVariableSearchService[pd.DataFrame]):
    _variableRepository: IVariableRepository[pd.DataFrame]
    _logger: Logger

    def __init__(
        self,
        variableRepository: IVariableRepository[pd.DataFrame],
        loggerFactory: ILoggerFactory,
    ) -> None:
        self._variableRepository = variableRepository
        self._logger = loggerFactory.getLogger(__name__)

    @timer
    def searchGroups(self, regex: str) -> pd.DataFrame:
        self._logger.debug(f"searching groups for regex: `{regex}`")

        groups = self._variableRepository.getGroups()

        series: pd.Series[bool] = groups["description"].str.contains(  # type: ignore
            regex, case=False
        )

        return groups[series].reset_index(
            drop=True,
        )

    @timer
    def searchVariables(
        self,
        regex: str,
        *inGroups: GroupCode,
    ) -> pd.DataFrame:

        self._logger.debug(f"searching variables for pattern `{regex}`")

        variables: pd.DataFrame
        if not len(inGroups):
            variables = self._variableRepository.getAllVariables()
        else:
            variables = self._variableRepository.getVariablesByGroup(*inGroups)

        series = variables["name"].str.contains(regex, case=False)  # type: ignore

        return variables[series].reset_index(drop=True)  # type: ignore
