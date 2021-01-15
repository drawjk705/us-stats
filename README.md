[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Release](https://github.com/drawjk705/us-data/workflows/Release/badge.svg)
![CI](https://github.com/drawjk705/us-data/workflows/CI/badge.svg)

# US-Data

Want to work with US Census data? Look no further.

## Getting started

### View all datasets

If you you're not sure what Census dataset you're interested in, the following code will take care of you:

```python
from us_data.census import listAvailableDataSets()

listAvailableDataSets()
```

This will present you with a pandas DataFrame listing all available datasets from the US Census API. (This includes only aggregate datasets, as they other types [of which there are very few] don't play nice with the client).

### Selecting a dataset

Before getting started, you need to [get a Census API key](https://api.census.gov/data/key_signup.html), and set the following the environment variable `CENSUS_API_KEY` to whatever that key is, either with

```bash
export CENSUS_API_KEY=<your key>
```

or in a `.env` file:

```
CENSUS_API_KEY=<your key>
```

Say you're interested in the American Community Survey 1-year estimates for 2019. Look up the dataset and survey name in the table provided by `listAvailableDataSets`, and execute the following code:

```python
from us_data.census import getCensus

dataset = getCensus(year=2019, datasetType="acs", surveyType="acs1")
```

The `dataset` object will now let you query any census data for the the ACS 1-year estimates of 2019. We'll now dive into how to query this dataset with the tool. However, if you aren't familiar with dataset "architecture", check out [this](#dataset-architecture) section.

### Arguments to `getCensus`

This is the signature of `getCensus`:

```python
def getCensus(year: int,
              datasetType: str = "acs",
              surveyType: str = "acs1",
              cacheDir: str = CACHE_DIR,        # cache
              shouldLoadFromExistingCache: bool = False,
              shouldCacheOnDisk: bool = False,
              replaceColumnHeaders: bool = True,
              logFile: str = DEFAULT_LOGFILE):  # us_data.log
    pass
```

-   `year`: the year of the dataset
-   `datasetType`: type of the dataset, specified by [`listAvailableDatasets`](#which-dataset)
-   `surveyType`: type of the survey, specified by [`listAvailableDatasets`](#which-dataset)
-   `cacheDir`: if you opt in to on-disk caching (more on this below), the name of the directory in which to store cached data
-   `shouldLoadFromExistingCache`: if you have cached data from a previous session, this will reload cached data into the `Census` object, instead of hitting the Census API when that data is queried
-   `shouldCacheOnDisk`: whether or not to cache data on disk, to avoid repeat API calls. The following data will be cached:
    -   Supported Geographies
    -   Group codes
    -   Variable codes
-   `replaceColumnHeaders`: whether or not to replace column header names for variables with more intelligible names instead of their codes
-   `logFile`: name of the file in which to store logging information

###### A note on caching

While on-disk caching is optional, this tool, by design, performs in-memory caching. So a call to `dataset.getGroups()` will hit the Census API one time at most. All subsequent calls will retrieve the value cached in-memory.

## Making queries

### Supported geographies

Getting the [supported geographies](#supported-geographies) for a dataset as as simple as this:

```python
dataset.getSupportedGeographies()
```

This will output a DataFrame will all possible supported geographies (e.g., if I can query all school districts across all states).

### Geography codes

If you decide you want to query a particular geography (e.g., a particular school district within a particular state), you'll need the [FIPS](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code#FIPS_state_codes) codes for that school district and state.

So, if you're interested in all school districts in Colorado, here's what you'd do:

1. Get FIPS codes for all states:

```python
from us_data.census import GeoDomain

dataset.getGeographyCodes(GeoDomain("state", "*"))
```

2. Get FIPS codes for all school districts within Colorado (FIPS code `08`):

```python
dataset.getGeographyCodes(GeoDomain("school district", "*"),
                          GeoDomain("state", "08"))
```

Note that geography code queries must follow supported geography guidelines.

### Groups

Want to figure out what groups are available for your dataset? No problem. This will do the trick for ya:

```python
dataset.getGroups()
```

...and you'll get a DataFrame with all groups for your dataset.

#### Searching groups

`dataset.getGroups()` will return a lot of data that might be difficult to slog through. In that case, run this:

```python
dataset.searchGroups(regex=r"my regex")
```

and you'll get a filtered DataFrame with matches to your regex.

#### Groups autocomplete

If you're working in a Jupyter notebook and have autocomplete enabled, running `dataset.groups.`, followed by a tab, will trigger an autocomplete menu for possible groups by their name (as opposed to their code, which doesn't have any inherent meaning in and of itself).

```python
dataset.groups.SexByAge   # code for this group
```

### Variables

You can either get a DataFrame of variables based on a set of groups:

```python
dataset.getVariablesByGroup(dataset.groups.SexByAge,
                            dataset.groups.MedianAgeBySex)
```

Or, you can get a DataFrame with all variables for a given dataset:

```python
dataset.getAllVariables()
```

This second operation, can, however, take a lot of time.

#### Searching variables

Similar to groups, you can search variables by regex:

```python
dataset.searchVariables(r"my regex")
```

And, you can limit that search to variables of a particular group or groups:

```python
dataset.searchVariables(r"my regex",
                        dataset.groups.SexByAge)
```

#### Variables autocomplete

Variables also support autocomplete for their codes, as with groups.

```python
dataset.variables.EstimateTotal_B01001  # code for this variable
```

(These names must be suffixed with the group code, since, while variable codes are unique across groups, their names are not unique across groups.)

### Statistics

Once you have the variables you want to query, along with the geography you're interested in, you can now make statistics queries from your dataset:

```python
from us_data.census import GeoDomain

variables = dataset.getVariablesForGroup(dataset.groups.SexByAge)

dataset.getStats(variables["code"].tolist(),
                 GeoDomain("school district", "*"),
                 GeoDomain("state", "08"))
```

## Experimental: Political Party

(Right now, this will work only with state & congressional district political parties.)

### Requirements

For this package to work, you must [get an API key from ProPublica](https://www.propublica.org/datastore/api/propublica-congress-api), whose API this uses, and set the following the environment variable `PROPUBLICA_CONG_KEY` to whatever that key is, either with

```bash
export PROPUBLICA_CONG_KEY=<your key>
```

or in a `.env` file:

```
PROPUBLICA_CONG_KEY=<your key>
```

### The package

If you're interested in looking at the political party of the state or congressional district, the `congress` package will serve you well:

```python
from us_data.congress import getCongress

cong = getCongress(116)
```

This will return a client for querying data on a particular congress (in the above example, the 116th Congress).

Right now, this enables only getting lists of Representatives and Senators:

```python
cong.getRepresentatives() # DataFrame with all representatives
cong.getSenators()        # DataFrame with all senators
```

You can use [`pandas.merge`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html) to perform an inner join on the congressional district or state data to find that region's political leaning.

## Dataset "architecture"

US Census datasets have 3 primary components:

1.  [Groups](#groups)
2.  [Variables](#variables)
3.  [Supported Geographies](#supported-geographies)

### Groups

A group is a "category" of data gathered for a particular dataset. For example, the `SEX BY AGE` group would provide breakdowns of gender and age demographics in a given region in the United States.

Some of these groups' names, however, are a not as clear as `SEX BY AGE`. In that case, I recommend heading over to the survey in question's [technical documentation](https://www2.census.gov/programs-surveys/) which elaborates on what certain terms mean with respect to particular groups. Unfortunately, the above link might be complicated to navigate, but if you're looking for ACS group documentation, [here's](https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2019_ACSSubjectDefinitions.pdf) a handy link.

### Variables

Variables measure a particular data-point. While they have their own codes, you might find variables which share the same name (e.g., `Estimate!!:Total:`). This is because each variable belongs to a [group](#group). So, the `Estimate!!:Total` variable for `SEX BY AGE` group is the total of all queried individuals in that group; but the `Estimate!!:Total` variable for `POVERTY STATUS IN THE PAST 12 MONTHS BY AGE` group is the total of queried individuals for _that_ group. (It's important when calculating percentages that you work within the same group. So if I want the percent of men in the US, whose total number I got from `SEX BY AGE` I should use the `Estimate!!:Total:` of that group as my denominator, and not the `Estimate!!:Total:` of the `POVERTY STATUS` group).

Variables on their own, however, do nothing. They mean something only when you query a particular [geography](#supported-geographies) for them.

### Supported Geographies

Supported geographies dictate the kinds of queries you can make for a given dataset. For example, in the ACS-1, I might be interested in looking at stats across all school districts. The survey's supported geographies will tell me if I can actually do that; or, if I need to refine my query to look at school districts in a given state or smaller region.
