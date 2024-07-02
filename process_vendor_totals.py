import csv

# Function to calculate total for a list of objectives by vendor
def calculate_vendor_total(vendor, objective_list, objective_totals):
    total = 0
    for objective in objective_list:
        if objective in objective_totals[vendor]:
            total += objective_totals[vendor][objective]
    return total

# Function to calculate percentage for each vendor in each category
def calculate_vendor_percentage(vendor_total, total_count):
    if total_count == 0:
        return 0.0
    return (vendor_total / total_count) * 100

# Main function to process vendor totals
def main():
    # Step 1: Read data.csv and calculate objective totals by vendor
    objective_totals = {}

    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read the header to get vendor names
        vendors = header[1:]  # Extract vendor names from the header
        for row in csv_reader:
            objective_number = row[0].strip()  # Assuming objective number is in the first column
            for i, value in enumerate(row[1:], start=1):
                vendor = vendors[i - 1]  # Get vendor name dynamically from the header
                if vendor not in objective_totals:
                    objective_totals[vendor] = {}
                if objective_number in objective_totals[vendor]:
                    objective_totals[vendor][objective_number] += float(value.strip()) if value.strip() else 0.0
                else:
                    objective_totals[vendor][objective_number] = float(value.strip()) if value.strip() else 0.0

    # Step 2: Define objectives by category
    categories = {
        "User: Target": [
            '1.1.1', '1.2.1', '1.2.2', '1.3.1', '1.4.1', '1.4.2', '1.5.1', '1.5.2', '1.6.1', '1.7.1', '1.8.1', '1.8.2', '1.9.1'
        ],
        "User: Advanced": [
            '1.2.3', '1.2.4', '1.2.5', '1.3.2', '1.4.3', '1.4.4', '1.5.3', '1.5.4', '1.6.2', '1.8.3', '1.8.4', '1.9.3'
        ],
        "Device: Target": [
            '2.1.1', '2.1.2', '2.1.3', '2.2.1', '2.3.2', '2.3.3', '2.4.1', '2.4.2', '2.5.1', '2.6.1', '2.6.2', '2.7.1', '2.7.2'
        ],
        "Device: Advanced": [
            '2.1.4', '2.2.2', '2.3.1', '2.3.5', '2.3.6', '2.3.7', '2.4.3', '2.4.4', '2.7.3'
        ],
        "Application & Workload: Target": [
            '3.1.1', '3.1.2', '3.1.3', '3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.4.1', '3.4.2', '3.4.3', '3.5.1'
        ],
        "Application & Workload: Advanced": [
            '3.2.4', '3.4.4', '3.5.2'
        ],
        "Data: Target": [
            '4.1.1', '4.2.1', '4.2.2', '4.2.3', '4.3.1', '4.3.2', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.5.3', '4.6.1', '4.6.2', '4.7.1'
        ],
        "Data: Advanced": [
            '4.3.3', '4.3.4', '4.3.5', '4.4.5', '4.4.6', '4.5.4', '4.5.5', '4.6.3', '4.6.4', '4.7.2', '4.7.3', '4.7.5', '4.7.6', '4.7.7'
        ],
        "Network & Environment: Target": [
            '5.1.1', '5.1.2', '5.2.1', '5.2.2', '5.2.3', '5.2.4', '5.2.5', '5.3.1', '5.3.2'
        ],
        "Network & Environment: Advanced": [
            '5.4.1', '5.4.2', '5.4.3'
        ],
        "Automation & Orchestration: Target": [
            '6.1.1', '6.1.2', '6.1.3', '6.2.1', '6.2.2', '6.3.1', '6.5.1', '6.5.2', '6.6.1', '6.6.2', '6.6.3', '6.7.1', '6.7.2'
        ],
        "Automation & Orchestration: Advanced": [
            '6.1.4', '6.2.3', '6.4.1', '6.7.3', '6.4.2', '6.5.3', '6.7.4'
        ],
        "Visibility & Analytics: Target": [
            '7.1.1', '7.1.2', '7.2.4', '7.2.1', '7.3.1', '7.1.3', '7.2.2', '7.2.5'
        ],
        "Visibility & Analytics: Advanced": [
            '7.3.2', '7.4.1', '7.5.1', '7.4.2', '7.4.3', '7.4.4', '7.6.1', '7.6.2'
        ]
    }

    # Calculate totals for each vendor in each category
    vendor_totals = {vendor: {} for vendor in vendors}
    for vendor in vendors:
        for category, objectives in categories.items():
            vendor_totals[vendor][category] = calculate_vendor_total(vendor, objectives, objective_totals)

    # Calculate total count (35 vendors per objective)
    total_count = 35

    # Calculate percentages for each vendor in each category
    vendor_percentages = {vendor: {category: calculate_vendor_percentage(vendor_totals[vendor][category], total_count) for category in categories.keys()} for vendor in vendor_totals.keys()}

    # Read existing lines from vendor_totals.txt
    try:
        with open('../vendor_totals.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Prepare a list to hold updated lines
    updated_lines = []

    # Process each line in the file
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:  # Ensure there are at least 3 parts (to check category)
            category = parts[2].strip()
            vendor_updates = []
            for vendor, percentages in vendor_percentages.items():
                if category in percentages:
                    vendor_updates.append(f"({vendor}~{percentages[category]:.2f}%)")
            if vendor_updates:
                updated_line_parts = parts[:3]  # Keep first three parts
                updated_line_parts.append(', '.join(vendor_updates))  # Append vendors and percentages as tuples
                updated_line = ','.join(updated_line_parts) + '\n'
                updated_lines.append(updated_line)
                print(f"Updated line: {updated_line}")  # Debug print
            else:
                updated_lines.append(line)  # If category not found, keep original line
        else:
            updated_lines.append(line)  # If line doesn't have at least 3 parts, keep original line

    # Write updated lines back to vendor_totals.txt
    with open('../vendor_totals.txt', 'w') as file:
        file.writelines(updated_lines)

    print("vendor_totals.txt has been updated successfully.")

    # Print statements with percentage calculation (optional)
    for vendor in vendor_totals.keys():
        print(f"Vendor: {vendor}")
        for category, total in vendor_totals[vendor].items():
            print(f"{category} Total: {total}, Percentage: {vendor_percentages[vendor][category]:.2f}%")

# Entry point of the script
if __name__ == "__main__":
    main()
