from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from getpass import getpass
import pandas as pd


def get_available_data(api: SentinelAPI,
                       username: str,
                       password: str,
                       dir_geojson: str,
                       date1: date,
                       date2: date,
                       producttype: str = "SLC") -> pd.DataFrame:
    """Obtain Sentinel-1's available datasets

    Args:
        api (SentinelAPI): SentinelAPI class
        username (str): usename of SentinelHub
        password (str): password of SentinelHub
        dir_geojson (str): directory to AoI geojson file
        date1 (date): search beginning date
        date2 (date): search end date

    Returns:
        pd.DataFrame: dataframe which contains obtained data information

    Reference:
        https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide/FullTextSearch?redirectedfrom=SciHubUserGuide.3FullTextSearch
    """

    footprint = geojson_to_wkt(read_geojson(dir_geojson))
    products = api.query(
                footprint,
                date=(date1.strftime('%Y%d%m'),
                      date2.strftime('%Y%d%m')),
                platformname='Sentinel-1',
                producttype=producttype)

    products_df = api.to_dataframe(products)

    return products_df


# def add_datafile_to_local_datalist(local_data_list: str,
#                                    input_file_uuid: str)

if __name__ == "__main__":
    username = input("Sentinel Hub Username: ")
    password = getpass()

    dir_output = "raw_data/tokyo_bay_sample"
    dir_geojson = "aois/tokyo_bay.geojson"

    start_date = date(2019, 1, 1)
    end_date = date(2020, 1, 1)

    api = SentinelAPI(username, password,
                      'https://scihub.copernicus.eu/dhus')

    s1_df = get_available_data(api, username, password,
                               dir_geojson, start_date, end_date)
    out_df_name = \
        "tokyo_bay_{}_{}".format(start_date.strftime('%Y%d%m'),
                                 end_date.strftime('%Y%d%m'))

    s1_df.to_csv("output/s1_df.csv")
