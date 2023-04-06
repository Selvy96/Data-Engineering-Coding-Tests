import json
import requests
import csv

# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type

BASE_URL = "https://courttribunalfinder.service.gov.uk/search/results.json?postcode="

def get_ten_nearest_courts(postcode: str) -> list[dict]:
    """Retrieves the ten nearest courts to a given postcode"""
    response = requests.get(f"{BASE_URL}{postcode}")

    data = response.json()
    nearest_ten_courts = []

    for court in data:
        if "dx_number" in court.keys():
            dx_number = court["dx_number"]
        else:
            dx_number = None
        name = court["name"]
        distance = court["distance"]
        types = court["types"]
        court_dict = {"name": name, "dx_number": dx_number, "distance": distance, "types": types}
        nearest_ten_courts.append(court_dict)
    return nearest_ten_courts


def get_nearest_court() ->:
    """Finds nearest court of correct type for person"""
    data_list = []
    with open('people.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nearest_ten_courts = get_ten_nearest_courts(row["home_postcode"])
            nearest_ten = nearest_ten_courts.copy()
            nearest_court = []
            while len(nearest_court) == 0:
                if row["looking_for_court_type"] in nearest_ten_courts[0]["types"]:
                    nearest_court.append(nearest_ten_courts[0])
                nearest_ten_courts.pop(0)

            output_dict = {
                "name": row["person_name"], 
                "desired_court_type": row["looking_for_court_type"], 
                "home_postcode": row["home_postcode"],
                "nearest_court_of_type": nearest_court[0]["name"],
                "dx_number": nearest_court[0]["dx_number"],
                "distance": nearest_court[0]["distance"]
                }
            data_list.append(output_dict)
    return(data_list)

if __name__ == "__main__":

    get_nearest_court()
