import pandas as pd

def update_points_with_vendors(txt_file, csv_file):
    # Read the data from the CSV file
    df = pd.read_csv(csv_file)

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
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Update points with vendor information
    updated_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            x, y, objective = parts[:3]  # Extract x, y, and objective
            # Debug print to check each point being processed
            print(f"Processing point: {x}, {y}, {objective}")
            # Adjust objective format if needed (e.g., remove "OBJ ")
            objective = objective.replace("OBJ ", "")
            if objective in objective_to_vendors:
                vendors_info = ", ".join([f"{k}: {v}" for k, v in objective_to_vendors[objective].items()])
                updated_line = f"{x},{y},{objective},{vendors_info}\n"
                updated_lines.append(updated_line)
                # Debug print to check the updated line
                print(f"Updated line: {updated_line}")
            else:
                updated_lines.append(line)
                # Debug print for unmatched objective
                print(f"No vendor info for objective: {objective}")
        else:
            updated_lines.append(line)

    # Write the updated points back to the points.txt file
    with open(txt_file, 'w') as file:
        file.writelines(updated_lines)

    # Final debug print to confirm writing to file
    print(f"Updated points file saved as: {txt_file}")

# Example usage
txt_file = 'points.txt'
csv_file = 'data.csv'

update_points_with_vendors(txt_file, csv_file)
