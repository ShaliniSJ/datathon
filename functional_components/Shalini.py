import pandas as pd
accused_data = pd.read_parquet("Predictive Crime Analytics/AccusedData.parquet")
complainant_details = pd.read_parquet(
    "Predictive Crime Analytics/ComplainantDetailsData.parquet"
)
victim_info = pd.read_parquet("Predictive Crime Analytics/VictimInfoDetails.parquet")
fir_details = pd.read_csv("Predictive Crime Analytics/FIR_Details_Data.csv")

def csv_to_parquet():

    files = ['Predictive Crime Analytics/AccusedData.csv', 'Predictive Crime Analytics/ComplainantDetailsData.csv', 'Predictive Crime Analytics/VictimInfoDetails.csv', 'Predictive Crime Analytics/FIR_Details_Data.csv']
    for i in files:
    # Load CSV file into a pandas DataFrame
        df = pd.read_csv(i)

        # Convert DataFrame to Parquet format
        df.to_parquet(i.split('.')[0] + '.parquet', engine='pyarrow')


def get_victim_info():
    response = {"status": "success", "data": {}}
    print(request.args)
    if request.args.get("filter") == "age":
        # Get the number of victims in each age group = ["19-25","26-35","36-45","46-55","56-65","65+"]
        response["data"]["10-18"] = len(victim_info[(victim_info["age"] >= 10) & (victim_info["age"] <= 18)])
        response["data"]["19-25"] = len(victim_info[(victim_info["age"] >= 19) & (victim_info["age"] <= 25)])
        response["data"]["26-35"] = len(victim_info[(victim_info["age"] >= 26) & (victim_info["age"] <= 35)])
        response["data"]["36-45"] = len(victim_info[(victim_info["age"] >= 36) & (victim_info["age"] <= 45)])
        response["data"]["46-55"] = len(victim_info[(victim_info["age"] >= 46) & (victim_info["age"] <= 55)])
        response["data"]["56-65"] = len(victim_info[(victim_info["age"] >= 56) & (victim_info["age"] <= 65)])
        response["data"]["65+"] = len(victim_info[(victim_info["age"] > 65)])
    return jsonify(response)
