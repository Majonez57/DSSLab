import pandas as pd


labels = ['Punch']
features = ["AccelXLow", "AccelYLow", "AccelZLow", "AccelMLow",
            "GyroXLow", "GyroYLow", "GyroZLow", "GyroMLow",
            "AccelXTop", "AccelYTop", "AccelZTop", "AccelMTop",
            "GyroXTop", "GyroYTop", "GyroZTop", "GyroMTop"]

def generateCols(window_size):

    cols = labels + features
    for i in range(window_size-1):
        cols += [x + f'_{i}' for x in features]

    return cols

def sliding_window(input_csv, output_csv, window_size):
    # Read the input CSV into a pandas DataFrame
    data = pd.read_csv(input_csv)
    data = data.drop(['SoundLow'], axis=1)
    
    # Create a list to store the transformed data
    transformed_data = []
    
    # Iterate over each row in the DataFrame
    for i in range(window_size, len(data)):
        # Extract the current row
        current_row = data.iloc[i]
        
        # Extract label and features from the current row
        label = current_row.iloc[0]
        features = current_row.iloc[1:]
        
        # Initialize a list to store the sliding window data
        window_data = []
        
        # Iterate over the previous n rows to create the sliding window
        for j in range(max(0, i - window_size + 1), i + 1):
            # Exclude label from previous rows
            if j != i:
                window_data.extend(data.iloc[j].iloc[1:])
                
        # Combine the current features and the sliding window data
        combined_data = list(features) + window_data
        
        # Append label and combined_data to the transformed data list
        transformed_data.append([label] + combined_data)
    
    # Convert the transformed data to a DataFrame
    transformed_df = pd.DataFrame(transformed_data, columns=generateCols(window_size))
    
    # Save the transformed DataFrame to a new CSV file
    transformed_df.to_csv(output_csv, index=False, header=True)

# Example usage:
window_size = 5
input_csv = "constructedData/binPunches2.csv"
output_csv = f"constructedData/binPunches_window_{window_size}.csv"
sliding_window(input_csv, output_csv, window_size)