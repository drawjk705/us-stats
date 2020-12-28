import logging
from pathlib import Path
import re
import requests
from typing import Dict, List
import pandas as pd
from models.State import State
from utils import buildUrl
from constants import DATA_FILES_DIR, stateAbbreviations


def __extractState(data: list) -> str:
    """
    Pulls the state's name from what's returned from the API

    Args:
        data (list): data from the API

    Returns:
        str: the stat's name
    """

    name = data[0]
    match = re.search(r', (.*)', name)
    if not match:
        return ''
    return match.group(1)


def __getStatesAndDistricts() -> List[Dict[str, str]]:
    """
    Get all states and their congressional districts from
    the census API

    Returns:
        List[Dict[str, str]]: list of dictionaries, each of which
            contains the state name, census code for the state,
            district number for that particular dictionary,
            and the computed state ID ([state name]-[congressional district number])
    """

    url = buildUrl('NAME')
    res = requests.get(url).json()

    states: Dict[str, State] = {}

    for line in res[1:]:
        name = __extractState(line)

        if line[1] in states:
            state = states[line[1]]
            state.addDistrict(line[2])
        else:
            states[line[1]] = State(name)
            states[line[1]].addDistrict(line[2])

    statesList: List[Dict[str, str]] = []
    for code, state in states.items():
        for district in state.districts:
            stateAbbr = stateAbbreviations[state.name.upper()]

            obj: Dict[str, str] = {
                'stateCode': code,
                'stateName': state.name,
                'stateAbbr': stateAbbr,
                'districtNum': district,
                'stateId': f'{stateAbbr}-{district}'
            }
            statesList.append(obj)

    return statesList


def buildStateIds():
    """
    Creates IDs for each state and congressional district combination.
    e.g., CA-01 for California's 1st congressional district
    """

    logging.info('generating state IDs...')
    states = __getStatesAndDistricts()
    df = pd.DataFrame(states).sort_values(
        ['stateName', 'districtNum'], ascending=[True, True])

    path = Path(f'{DATA_FILES_DIR}/dbo')
    path.mkdir(parents=True, exist_ok=True)

    df.to_csv(f'{path.absolute()}/stateIds.csv', index=False)
    logging.info('stateIDs generated')