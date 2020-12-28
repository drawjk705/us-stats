from typing import Dict

SURVEY_TYPE = 'acs1'
YEAR = 2019

DB = 'usCensus'
DATA_FILES_DIR = 'dataFiles'
API_BASE_URL = f'https://api.census.gov/data/{YEAR}/acs/{SURVEY_TYPE}'

CENSUS_TOPICS_URL = 'https://api.census.gov/data/{YEAR}/acs/{SURVEY_TYPE}/groups.json'

stateAbbreviations: Dict[str, str] = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "AMERICAN SAMOA": "AS",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "DISTRICT OF COLUMBIA": "DC",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "GUAM": "GU",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "NORTHERN MARIANA IS": "MP",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "PUERTO RICO": "PR",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "VIRGIN ISLANDS": "VI",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY"
}


# https://api.census.gov/data/2019/acs/acs1/groups.html
schemasToTables: Dict[str, Dict[str, str]] = {
    'healthInsurance': {
        'coverageTypeByAgeAndEducation': 'HEALTH INSURANCE COVERAGE STATUS AND TYPE BY AGE BY EDUCATIONAL ATTAINMENT',
        'whiteOnlyCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (WHITE ALONE)',
        'blackCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (BLACK OR AFRICAN AMERICAN ALONE)',
        'usIndianAndAlaskaNativeCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (AMERICAN INDIAN AND ALASKA NATIVE ALONE',
        'asianCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (ASIAN ALONE)',
        'hawaiianNativeCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE)',
        'otherRaceCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (SOME OTHER RACE ALONE)',
        'biracialCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (TWO OR MORE RACES)',
        'whiteNoLatinoCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (WHITE ALONE, NOT HISPANIC OR LATINO)',
        'latinoHispanicCoverage': 'HEALTH INSURANCE COVERAGE STATUS BY AGE (HISPANIC OR LATINO)'
    },
    'education': {
        'educationalAttainment': 'CITIZEN, VOTING-AGE POPULATION BY EDUCATIONAL ATTAINMENT',
        'individualPovertyStatusByEducation': 'POVERTY STATUS IN THE PAST 12 MONTHS OF INDIVIDUALS BY SEX BY EDUCATIONAL ATTAINMENT',
        'familyPovertyStatusByHouseholderEducation': 'POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE BY EDUCATIONAL ATTAINMENT OF HOUSEHOLDER',
        'earningsBySexByEducation': 'MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER',
        'homeOwnershipByEducation': 'TENURE BY EDUCATIONAL ATTAINMENT OF HOUSEHOLDER',
        'insuranceCoverageByEducation': 'HEALTH INSURANCE COVERAGE STATUS AND TYPE BY AGE BY EDUCATIONAL ATTAINMENT'
    },
    'economics': {
        'povertyStatus': 'CITIZEN, VOTING-AGE POPULATION BY POVERTY STATUS',
        'employmentStatus': 'EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER',
        'employmentStatusByEducation': 'EDUCATIONAL ATTAINMENT BY EMPLOYMENT STATUS FOR THE POPULATION 25 TO 64 YEARS',
        'income': 'HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)',
        'medianIncome': 'MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS',
    },
    'resources': {
        'internetAccess': 'PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD',
        'educationByTechAccess': 'EDUCATIONAL ATTAINMENT BY PRESENCE OF A COMPUTER AND TYPES OF INTERNET SUBSCRIPTION IN HOUSEHOLD',
        'laborForceStatusByTechAccess': 'LABOR FORCE STATUS BY PRESENCE OF A COMPUTER AND TYPES OF INTERNET SUBSCRIPTION IN HOUSEHOLD',
    }
}