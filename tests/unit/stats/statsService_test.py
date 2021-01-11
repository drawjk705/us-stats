import pandas as pd
from tests.utils import shuffledCases
import pytest
from census.geographies.models import GeoDomain
from typing import Any, Dict
from census.variables.models import GroupCode, GroupVariable, VariableCode
from tests.serviceTestFixtures import ServiceTestFixture
from census.stats.service import CensusStatisticsService

# pyright: reportPrivateUsage=false

var1 = GroupVariable(
    code=VariableCode("var1"),
    groupCode=GroupCode("g1"),
    groupConcept="concept1",
    name="name 1",
    limit=1,
    predicateOnly=False,
    predicateType="int",
    cleanedName="cleanedName1",
)
var2 = GroupVariable(
    code=VariableCode("var2"),
    groupCode=GroupCode("g1"),
    groupConcept="concept1",
    name="name 2",
    limit=1,
    predicateOnly=False,
    predicateType="float",
    cleanedName="cleanedName2",
)
var3 = GroupVariable(
    code=VariableCode("var3"),
    groupCode=GroupCode("g1"),
    groupConcept="concept1",
    name="name 3",
    limit=1,
    predicateOnly=False,
    predicateType="string",
    cleanedName="cleanedName3",
)
var4 = GroupVariable(
    code=VariableCode("var4"),
    groupCode=GroupCode("g1"),
    groupConcept="concept1",
    name="name 4",
    limit=1,
    predicateOnly=False,
    predicateType="string",
    cleanedName="cleanedName4",
)

variablesInRepo: Dict[str, GroupVariable] = dict(
    var1=var1, var2=var2, var3=var3, var4=var4
)


class TestStatsAsDataFrame(ServiceTestFixture[CensusStatisticsService]):
    @pytest.mark.parametrize(*shuffledCases(shouldReplaceColumnHeaders=[True, False]))
    def test_getStats_passesCorrectValuesToTransformer(
        self, shouldReplaceColumnHeaders: bool
    ):
        apiGet = self.mocker.patch.object(
            self._service._api, "stats", return_value=iter([[1, 2], [3]])
        )
        self.mocker.patch.object(
            self._service._config, "replaceColumnHeaders", shouldReplaceColumnHeaders
        )
        variablesToQuery = [
            var1.code,
            var2.code,
            var3.code,
        ]
        forDomain = GeoDomain("state")
        inDomains = [GeoDomain("us")]
        expectedColumnMapping: Dict[str, int] = dict(map=1)
        expectedTypeMapping: Dict[str, Any] = dict(map=int)

        self.mocker.patch.object(
            self._service,
            "_getVariableNamesAndTypeConversions",
            return_value=(expectedColumnMapping, expectedTypeMapping),
        )
        self.mocker.patch.object(
            self._service,
            "_sortGeoDomains",
            return_value=[forDomain] + inDomains,
        )

        self._service.getStats(variablesToQuery, forDomain, *inDomains)

        apiGet.assert_called_once_with(variablesToQuery, forDomain, inDomains)
        self.castMock(self._service._transformer.stats).assert_called_once_with(
            [[1, 2], [3]],
            expectedTypeMapping,
            [forDomain] + inDomains,
            columnHeaders=expectedColumnMapping if shouldReplaceColumnHeaders else None,
        )

    def test_getVariableNamesAndTypeConversions_givenUniqueNames(self):
        variablesToQuery = {
            var1.code,
            var2.code,
            var3.code,
        }

        df = pd.DataFrame([val.__dict__ for val in variablesInRepo.values()])
        self.mocker.patch.object(
            self._service._variableRepo, "getVariablesByGroup", return_value=df
        )

        columnMapping, typeMapping = self._service._getVariableNamesAndTypeConversions(
            variablesToQuery
        )

        assert columnMapping == {
            "var1": "cleanedName1",
            "var2": "cleanedName2",
            "var3": "cleanedName3",
        }
        assert typeMapping == {"var1": float, "var2": float}

    def test_getVariableNamesAndTypeConversions_givenDuplicateNamesBetweenGroups(self):
        variableWithDuplicateName = GroupVariable(
            code=VariableCode("var5"),
            groupCode=GroupCode("g2"),
            groupConcept="concept 3",
            limit=0,
            predicateType="string",
            predicateOnly=False,
            name=var1.name,
            cleanedName=var1.cleanedName,
        )
        df = pd.DataFrame([val.__dict__ for val in variablesInRepo.values()])
        self.mocker.patch.object(
            self._service._variableRepo,
            "getVariablesByGroup",
            return_value=df.append(
                variableWithDuplicateName.__dict__, ignore_index=True
            ),
        )
        variablesToQuery = {
            var1.code,
            var2.code,
            var3.code,
            variableWithDuplicateName.code,
        }

        columnMapping, typeMapping = self._service._getVariableNamesAndTypeConversions(
            variablesToQuery
        )

        assert columnMapping == {
            "var1": "cleanedName1_g1",
            "var2": "cleanedName2_g1",
            "var3": "cleanedName3_g1",
            "var5": "cleanedName1_g2",
        }
        assert typeMapping == {"var1": float, "var2": float}

    def test_sortGeoDomains(self):
        geoDomains = [GeoDomain("apple"), GeoDomain("banana"), GeoDomain("cantelope")]
        supportedGeoRetval = pd.DataFrame(
            [
                {
                    "name": "banana",
                    "hierarchy": "001",
                },
                {
                    "name": "apple",
                    "hierarchy": "010",
                },
                {
                    "name": "cantelope",
                    "hierarchy": "020",
                },
                {
                    "name": "dingo",
                    "hierarchy": "110",
                },
            ]
        )

        self.mocker.patch.object(
            self._service._geoRepo,
            "getSupportedGeographies",
            return_value=supportedGeoRetval,
        )

        res = self._service._sortGeoDomains(geoDomains)

        assert res == [GeoDomain("banana"), GeoDomain("apple"), GeoDomain("cantelope")]
