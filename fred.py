from ProjectFiles.api_keys import fred_key
import requests
import pandas as pd

def main():
    base_url = "https://api.stlouisfed.org/fred/"

    obs_endpoint = "series/observations"

    series_id = "CPIAUCSL"
    start_date = "2000-01-01"
    end_date = "2023-06-30"
    ts_frequency = "q"
    ts_units = pc1

    obs_params = {
        "series_id": series_id,
        "api_key": fred_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
        "frequency": ts_frequency,
        "units": ts_units
    }

    response = requests.get(base_url + obs_endpoint, params=obs_params)

    if response.status_code == 200:
        res_data = response.json()
        obs_data = pd.DataFrame(res_data["observations"])
        obs_data["date"] = pd.to_datetime(obs_data["date"])
        obs_data.set_index("date", inplace=True)
        obs_data["value"] = obs_data["value"].astype(float)
    else:
        print("Failed to request data successfully. Status: ", response.status_code)
        return "na"

if __name__ == "__main__":
    main()