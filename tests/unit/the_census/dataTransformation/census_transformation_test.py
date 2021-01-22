from collections import OrderedDict
from typing import Any, Dict
from unittest.mock import MagicMock, Mock

import numpy as np
import pandas as pd
import pytest
from pytest_mock import MockFixture

from tests.serviceTestFixtures import ServiceTestFixture
from the_census._api.models import GeographyClauseSet, GeographyItem
from the_census._dataTransformation.service import CensusDataTransformer
from the_census._geographies.models import GeoDomain
from the_census._variables.models import Group, GroupCode, GroupVariable, VariableCode


@pytest.fixture
def pandasMock(mocker: MockFixture) -> Mock:
    return mocker.patch("pandas.DataFrame")


class TestCensusDataTransformer(ServiceTestFixture[CensusDataTransformer]):
    def test_supportedGeographies(self, pandasMock: MagicMock):
        supportedGeos = OrderedDict(
            {
                "abc": GeographyItem.makeItem(
                    name="abc",
                    hierarchy="123",
                    clauses=[
                        GeographyClauseSet.makeSet(
                            forClause="banana", inClauses=["apple"]
                        )
                    ],
                ),
                "def": GeographyItem.makeItem(
                    name="def",
                    hierarchy="567",
                    clauses=[
                        GeographyClauseSet.makeSet(
                            forClause="chair", inClauses=["stool", "table"]
                        ),
                        GeographyClauseSet.makeSet(
                            forClause="elf", inClauses=["santa", "workshop"]
                        ),
                    ],
                ),
            }
        )
        expectedCallValues = [
            {"name": "abc", "hierarchy": "123", "for": "banana", "in": "apple"},
            {"name": "def", "hierarchy": "567", "for": "chair", "in": "stool,table"},
            {"name": "def", "hierarchy": "567", "for": "elf", "in": "santa,workshop"},
        ]

        self._service.supportedGeographies(supportedGeos)

        pandasMock.assert_called_once_with(expectedCallValues)

    def test_geographyCodes(self, pandasMock: Mock):
        headers = ["header 1", "header 2"]
        rows = [["1", "2"], ["3", "4"], ["5", "6"]]
        geoCodes = [headers] + rows

        self._service.geographyCodes(geoCodes)

        pandasMock.assert_called_once_with(rows, columns=headers)

    def test_groupData(self, pandasMock: Mock):
        groupData = {
            "1": Group.fromJson(dict(name="1", description="desc1")),
            "2": Group.fromJson(dict(name="1", description="desc2")),
        }
        expectedCalledWith = [
            {"code": "1", "description": "desc1", "cleanedName": "Desc1"},
            {"code": "2", "description": "desc2", "cleanedName": "Desc2"},
        ]

        self._service.groups(groupData)

        pandasMock.assert_called_once_with(expectedCalledWith)

    def test_variables(self, pandasMock: Mock):
        variables = [
            GroupVariable(
                code=VariableCode("123"),
                groupCode=GroupCode("g123"),
                groupConcept="gCon1",
                name="name1",
                limit=1,
                predicateOnly=True,
                predicateType="string",
            ),
            GroupVariable(
                code=VariableCode("456"),
                groupCode=GroupCode("g456"),
                groupConcept="gCon2",
                name="name2",
                limit=2,
                predicateOnly=False,
                predicateType="int",
            ),
        ]
        expectedCall = [
            {
                "cleanedName": "",
                "code": "123",
                "groupCode": "g123",
                "groupConcept": "gCon1",
                "limit": 1,
                "name": "name1",
                "predicateOnly": True,
                "predicateType": "string",
            },
            {
                "cleanedName": "",
                "code": "456",
                "groupCode": "g456",
                "groupConcept": "gCon2",
                "limit": 2,
                "name": "name2",
                "predicateOnly": False,
                "predicateType": "int",
            },
        ]

        self._service.variables(variables)

        pandasMock.assert_called_once_with(expectedCall)

    def test_partition_stats_columns(self):
        renamedColHeaders = {VariableCode("abc"): "Abc", VariableCode("def"): "Def"}
        dfColumns = [
            "NAME",
            "five place",
            "abc",
            "def",
            "one place",
            "three place",
            "two place",
            "four place",
        ]
        expectedSortedGeoCols = [
            "one place",
            "two place",
            "three place",
            "four place",
            "five place",
        ]

        self.mocker.patch.object(
            self._service,
            "_sortGeoDomains",
            return_value=[GeoDomain(col) for col in expectedSortedGeoCols],
        )

        res = self._service._partitionStatColumns(renamedColHeaders, dfColumns)

        assert res == (["NAME"], expectedSortedGeoCols, ["abc", "def"])

    def test_sort_geo_domains(self):
        allSupportedGeos = pd.DataFrame(
            [
                dict(name="one place", hierarchy=1),
                dict(name="two place", hierarchy=2),
                dict(name="three place", hierarchy=3),
            ]
        )
        geoDomains = [
            GeoDomain(place) for place in ["two place", "one place", "three place"]
        ]

        self.mocker.patch.object(
            self._service._geoRepo,
            "getSupportedGeographies",
            return_value=allSupportedGeos,
        )

        res = self._service._sortGeoDomains(geoDomains)

        assert res == [
            GeoDomain(place) for place in ["one place", "two place", "three place"]
        ]

    @pytest.mark.parametrize("shouldReplaceColumnHeaders", [True, False])
    def test_stats(self, shouldReplaceColumnHeaders: bool):
        results = [
            [
                ["NAME", "var1", "var2", "geoCol1", "geoCol2"],
                ["1", "5", "1.2", "4", "5"],
                ["6", "6", "4.2", "9", "10"],
            ],
            [
                ["NAME", "var3", "var4", "geoCol1", "geoCol2"],
                ["1", "stringy", "tassel", "4", "5"],
                ["6", "yarn", "ropy", "9", "10"],
            ],
        ]

        typeConversions: Dict[str, Any] = dict(var1=int, var2=float)
        columnHeaders: Dict[VariableCode, str] = dict(
            var1="banana", var2="apple", var3="pear", var4="peach"
        )
        geoDomains = [GeoDomain("geoCol1"), GeoDomain("geoCol2")]

        self.mocker.patch.object(
            self._service,
            "_partitionStatColumns",
            return_value=(
                ["NAME"],
                ["geoCol1", "geoCol2"],
                ["var1", "var2", "var3", "var4"],
            ),
        )
        self.mocker.patch.object(
            self._service._config, "replaceColumnHeaders", shouldReplaceColumnHeaders
        )

        res = self._service.stats(results, typeConversions, geoDomains, columnHeaders)

        if shouldReplaceColumnHeaders:
            assert res.dtypes.to_dict() == {  # type: ignore
                "NAME": np.dtype("O"),
                "apple": np.dtype("float64"),
                "banana": np.dtype("int64"),
                "geoCol1": np.dtype("O"),
                "geoCol2": np.dtype("O"),
                "peach": np.dtype("O"),
                "pear": np.dtype("O"),
            }
            assert res.columns.tolist() == [
                "NAME",
                "geoCol1",
                "geoCol2",
                "banana",
                "apple",
                "pear",
                "peach",
            ]
        else:
            assert res.dtypes.to_dict() == {  # type: ignore
                "NAME": np.dtype("O"),
                "var2": np.dtype("float64"),
                "var1": np.dtype("int64"),
                "geoCol1": np.dtype("O"),
                "geoCol2": np.dtype("O"),
                "var4": np.dtype("O"),
                "var3": np.dtype("O"),
            }
            assert res.columns.tolist() == [
                "NAME",
                "geoCol1",
                "geoCol2",
                "var1",
                "var2",
                "var3",
                "var4",
            ]
