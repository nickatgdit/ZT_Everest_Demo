import pandas as pd


# Function to read objectives from a txt file
def read_objectives(txt_file):
    with open(txt_file, 'r') as file:
        objectives = [line.strip() for line in file.readlines()]
    return objectives


# Function to find and update top 3 vendors in the CSV file based on objectives
def update_csv_with_vendors(txt_file, csv_file, output_csv_file):
    # Read the objectives from the txt file
    objectives = read_objectives(txt_file)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Iterate over the objectives and update the CSV file with the top 3 vendors
    for objective in objectives:
        matching_rows = df[df['Objective'] == objective]
        if not matching_rows.empty:
            # Get the top 3 vendors
            top_vendors = matching_rows.nlargest(3, 'Score')['Vendor'].tolist()
            top_vendors_str = ', '.join(top_vendors)

            # Update the CSV file
            df.loc[df['Objective'] == objective, 'Top 3 Vendors'] = top_vendors_str

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_file, index=False)
    print(f"Updated CSV file saved as: {output_csv_file}")


# File paths
txt_file = 'points_update_test.txt'
csv_file = 'data.csv'
output_csv_file = 'updated_data.csv'

# Update the CSV file with top 3 vendors
update_csv_with_vendors(txt_file, csv_file, output_csv_file)
