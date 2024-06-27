import pandas as pd


def update_points_with_vendors(txt_file, csv_file):
    df = pd.read_csv(csv_file)
    updated_points = []

    with open(txt_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(',')
        objective = parts[0]
        x, y = parts[1], parts[2]

        if objective in df['Objective'].values:
            vendor_info = df[df['Objective'] == objective].iloc[0].to_dict()
            vendor_str = f"Vendor A: {vendor_info['Vendor_A']}\nVendor B: {vendor_info['Vendor_B']}\nVendor C: {vendor_info['Vendor_C']}"
            updated_points.append(f"{objective},{x},{y},{vendor_str}")

    with open(txt_file, 'w') as f:
        for point in updated_points:
            f.write(point + "\n")


if __name__ == "__main__":
    txt_file = 'points.txt'
    csv_file = 'data.csv'
    update_points_with_vendors(txt_file, csv_file)
    print(f"Updated points file saved as: {txt_file}")
