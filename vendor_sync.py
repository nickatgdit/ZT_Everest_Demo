import pandas as pd

def update_points_with_vendors(txt_in, csv_in):
    # Read the data from the CSV file
    df = pd.read_csv(csv_in)

    # Strip any leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    if 'Objective' not in df.columns:
        raise KeyError("The 'Objective' column is not found in the CSV file.")

    # Create a dictionary to map objectives to their vendor info
    objective_to_vendors = {}
    for index, row in df.iterrows():
        objective = row['Objective'].strip()  # Ensure stripping of whitespace
        vendors = row.drop('Objective').to_dict()
        objective_to_vendors[objective] = vendors

    # Read points from the points.txt file
    with open(txt_in, 'r') as file:
        lines = file.readlines()

    # Update points with vendor information
    updated_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            x, y, objective = parts[:3]  # Extract x, y, and objective
            # Adjust objective format if needed (e.g., remove "OBJ ")
            objective = objective.replace("OBJ ", "")
            if objective in objective_to_vendors:
                vendors_info = ", ".join([f"{k}: {v}" for k, v in objective_to_vendors[objective].items()])
                updated_line = f"{x},{y},{objective},{vendors_info}\n"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Write the updated points back to the points.txt file
    with open(txt_in, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated points file saved as: {txt_in}")

def main():
    # Define input files
    txt_file = 'points.txt'
    csv_file = 'data.csv'

    # Call function to update points with vendor information
    update_points_with_vendors(txt_file, csv_file)

if __name__ == "__main__":
    main()
