import pandas as pd

# Load the data
df = pd.read_csv('Evaluation/evaluation_results.csv')

# Define a function to parse parameters
def parse_parameters(pixelation_type, param_string):
    # Initialize dictionary to hold the parameter values
    param_dict = {}
    
    # Remove the surrounding quotes and extra spaces
    param_string = param_string.strip('"').strip()
    
    # Split the string by commas and strip extra spaces
    items = [item.strip() for item in param_string.split(',')]
    
    # Define parameter names based on the pixelation type
    if pixelation_type == "Adaptive Pixelization":
        # Expecting format like "min, block, size-10"
        keys = ['Min Block Size', 'Max Block Size', 'Variance Threshold']
    elif pixelation_type == "Basic Pixelization":
        # Expecting format like "block, size-1"
        keys = ['Block Size']
    elif pixelation_type == "Clustering with Pixelization":
        # Expecting format like "num, clusters-10, block, size-10"
        keys = ['Num Clusters', 'Block Size']
    elif pixelation_type == "Gaussian Blur":
    
        # Expecting format like "kernel, size-11"
        keys = ['Kernel Size']
    else:
        return param_dict

    # Extract values and map them to their corresponding keys
    key_index = 0
    for item in items:
        if '-' in item:
            key = keys[key_index]
            _, value = item.split('-')
            param_dict[key] = value.strip()
            key_index += 1

    return param_dict

# Apply the parsing function to each row based on the pixelation type
df_params = df.apply(lambda row: parse_parameters(row['Pixelation Type'], row['Parameters']), axis=1)

# Convert the list of dictionaries to a DataFrame
df_params = pd.DataFrame(df_params.tolist())

# Join the new parameters DataFrame with the original DataFrame
df = df.join(df_params)

# Save the cleaned data back to a new CSV file
df.to_csv('Evaluation/cleaned_evaluation_results.csv', index=False)
