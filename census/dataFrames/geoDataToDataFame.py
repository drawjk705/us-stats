import pandas as pd
from collections import OrderedDict
from api.models import GeographyItem


def geoDataToDataFrame(supportedGeos: OrderedDict[str, GeographyItem]) -> pd.DataFrame:
    valuesFlattened = []
    for geoItem in supportedGeos.values():
        for clause in geoItem.clauses:
            valuesFlattened.append({
                'name': geoItem.name,
                'hierarchy': geoItem.hierarchy,
                'for': clause.forClause,
                'in': ','.join(clause.inClauses)
            })

    return pd.DataFrame(valuesFlattened)