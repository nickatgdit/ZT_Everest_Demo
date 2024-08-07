import csv

num_vendors = 0


# Function to calculate percentage based on the superscored method
def calculate_superscored_percentage(total, max_possible_score):
    if max_possible_score == 0:
        return 0.0
    return (total / max_possible_score) * 100


# Function to calculate percentage using the previous method (unspecified)
def calculate_previous_percentage(total, count):
    if count == 0:
        return 0.0
    return (total / count) * 100


# Function to calculate maximum possible score for a list of objectives
def calculate_max_possible_score(objective_list, max_score_per_objective):
    return len(objective_list) * max_score_per_objective


def get_number_of_vendors():
    global num_vendors
    try:
        with open('data.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # Read the header
            num_vendors = len(header) - 1  # Assuming first column is not a vendor
    except FileNotFoundError:
        print("File 'data.csv' not found!")
    except Exception as e:
        print(f"Error reading 'data.csv': {e}")


def main(use_superscored_percentage=True):
    get_number_of_vendors()

    # Step 1: Define objective lists
    user_target_objectives = [
        '1.1.1', '1.2.1', '1.2.2', '1.3.1', '1.4.1', '1.4.2', '1.5.1', '1.5.2', '1.6.1', '1.7.1', '1.8.1', '1.8.2',
        '1.9.1'
    ]
    user_advanced_objectives = [
        '1.2.3', '1.2.4', '1.2.5', '1.3.2', '1.4.3', '1.4.4', '1.5.3', '1.5.4', '1.6.2', '1.8.3', '1.8.4', '1.9.2',
        '1.9.3'
    ]
    device_target_objectives = [
        '2.1.1', '2.1.2', '2.1.3', '2.2.1', '2.3.2', '2.3.3', '2.4.1', '2.4.2', '2.5.1', '2.6.1', '2.6.2', '2.7.1',
        '2.7.2'
    ]
    device_advanced_objectives = [
        '2.1.4', '2.2.2', '2.3.1', '2.3.5', '2.3.6', '2.3.7', '2.4.3', '2.4.4', '2.7.3'
    ]
    application_workload_target_objectives = [
        '3.1.1', '3.1.2', '3.1.3', '3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.4.1', '3.4.2',
        '3.4.3', '3.5.1'
    ]
    application_workload_advanced_objectives = [
        '3.2.4', '3.4.4', '3.5.2'
    ]
    data_target_objectives = [
        '4.1.1', '4.2.1', '4.2.2', '4.2.3', '4.3.1', '4.3.2', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.5.3',
        '4.6.1', '4.6.2', '4.7.1'
    ]
    data_advanced_objectives = [
        '4.3.3', '4.3.4', '4.3.5', '4.4.5', '4.4.6', '4.5.4', '4.5.5', '4.6.3', '4.6.4', '4.7.2', '4.7.3', '4.7.5',
        '4.7.6', '4.7.7'
    ]
    network_environment_target_objectives = [
        '5.1.1', '5.1.2', '5.2.1', '5.2.2', '5.2.3', '5.2.4', '5.2.5', '5.3.1', '5.3.2'
    ]
    network_environment_advanced_objectives = [
        '5.4.1', '5.4.2', '5.4.3'
    ]
    automation_orchestration_target_objectives = [
        '6.1.1', '6.1.2', '6.1.3', '6.2.1', '6.2.2', '6.3.1', '6.5.1', '6.5.2', '6.6.1', '6.6.2', '6.6.3', '6.7.1',
        '6.7.2'
    ]
    automation_orchestration_advanced_objectives = [
        '6.1.4', '6.2.3', '6.4.1', '6.7.3', '6.4.2', '6.5.3', '6.7.4'
    ]
    visibility_analytics_target_objectives = [
        '7.1.1', '7.1.2', '7.2.4', '7.2.1', '7.3.1', '7.1.3', '7.2.2', '7.2.5'
    ]
    visibility_analytics_advanced_objectives = [
        '7.3.2', '7.4.1', '7.5.1', '7.4.2', '7.4.3', '7.4.4', '7.6.1', '7.6.2'
    ]

    # Maximum score per objective
    max_score_per_objective = 2

    objectives_lists = {
        "User: Target": user_target_objectives,
        "User: Advanced": user_advanced_objectives,
        "Device: Target": device_target_objectives,
        "Device: Advanced": device_advanced_objectives,
        "Application & Workload: Target": application_workload_target_objectives,
        "Application & Workload: Advanced": application_workload_advanced_objectives,
        "Data: Target": data_target_objectives,
        "Data: Advanced": data_advanced_objectives,
        "Network & Environment: Target": network_environment_target_objectives,
        "Network & Environment: Advanced": network_environment_advanced_objectives,
        "Automation & Orchestration: Target": automation_orchestration_target_objectives,
        "Automation & Orchestration: Advanced": automation_orchestration_advanced_objectives,
        "Visibility & Analytics: Target": visibility_analytics_target_objectives,
        "Visibility & Analytics: Advanced": visibility_analytics_advanced_objectives
    }

    # Step 2: Read data.csv and calculate objective totals and gaps
    objective_totals = {}
    gap_dictionary = {}
    for key in objectives_lists.keys():
        gap_dictionary[key] = {"count": 0, "names": []}

    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            objective_number = row[0].strip()  # Assuming objective number is in the first column
            scores = [float(value) for value in row[1:] if value.strip()]
            total = sum(scores)
            objective_totals[objective_number] = total

            # Determine which objective list the current objective belongs to
            for key, objectives in objectives_lists.items():
                if objective_number in objectives:
                    # Check if the row contains no 2s
                    if 2 not in scores:
                        gap_dictionary[key]["count"] += 1
                        gap_dictionary[key]["names"].append(objective_number)
                    break

    # Step 3: Calculate totals and max possible scores for each list
    master_dict = {}
    for key, objectives in objectives_lists.items():
        total = sum(objective_totals.get(obj, 0) for obj in objectives)
        max_possible_score = calculate_max_possible_score(objectives, max_score_per_objective)
        master_dict[key] = (total, max_possible_score)

    # Step 4: Calculate grand totals for each pillar
    grand_totals = {
        "User: Grand": master_dict["User: Target"][0] + master_dict["User: Advanced"][0],
        "Device: Grand": master_dict["Device: Target"][0] + master_dict["Device: Advanced"][0],
        "Application & Workload: Grand": master_dict["Application & Workload: Target"][0] +
                                         master_dict["Application & Workload: Advanced"][0],
        "Data: Grand": master_dict["Data: Target"][0] + master_dict["Data: Advanced"][0],
        "Network & Environment: Grand": master_dict["Network & Environment: Target"][0] +
                                        master_dict["Network & Environment: Advanced"][0],
        "Automation & Orchestration: Grand": master_dict["Automation & Orchestration: Target"][0] +
                                             master_dict["Automation & Orchestration: Advanced"][0],
        "Visibility & Analytics: Grand": master_dict["Visibility & Analytics: Target"][0] +
                                         master_dict["Visibility & Analytics: Advanced"][0]
    }

    # Step 5: Read existing lines from totals.txt and update
    with open('totals.txt', 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:  # Ensure there are at least 3 parts (to check key)
            key = parts[2].strip()
            if key in master_dict:
                total, max_possible_score = master_dict[key]
                if use_superscored_percentage:
                    updated_percentage = calculate_superscored_percentage(total, max_possible_score)
                else:
                    updated_percentage = calculate_previous_percentage(total, len(objectives_lists[key]) * num_vendors)
                gap_info = f"{gap_dictionary[key]['count']} ({', '.join(gap_dictionary[key]['names'])})"
                updated_line = f"{parts[0]},{parts[1]},{parts[2]},{updated_percentage:.2f}%,{gap_info}\n"
                updated_lines.append(updated_line)
            elif ": Grand" in key:
                total = grand_totals[key]
                target_key = key.replace("Grand", "Target").strip()
                advanced_key = key.replace("Grand", "Advanced").strip()
                if use_superscored_percentage:
                    max_possible_score = master_dict[target_key][1] + master_dict[advanced_key][1]
                    updated_percentage = calculate_superscored_percentage(total, max_possible_score)
                else:
                    updated_percentage = calculate_previous_percentage(total, (
                                len(objectives_lists[target_key]) + len(objectives_lists[advanced_key])) * num_vendors)
                updated_line = f"{parts[0]},{parts[1]},{parts[2]},{updated_percentage:.2f}%\n"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Step 6: Write updated lines back to totals.txt
    with open('totals.txt', 'w') as file:
        file.writelines(updated_lines)

    # Step 7: Print statements with percentage calculation
    print("totals.txt has been updated successfully.")
    for key, (total, max_score) in master_dict.items():
        if use_superscored_percentage:
            percentage = calculate_superscored_percentage(total, max_score)
        else:
            percentage = calculate_previous_percentage(total, len(objectives_lists[key]) * num_vendors)
        gap_info = f"{gap_dictionary[key]['count']} ({', '.join(gap_dictionary[key]['names'])})"
        print(
            f"{key}: {total}, with {'max possible score' if use_superscored_percentage else 'count of'} {max_score}, percentage: {percentage:.2f}%, gaps (0 or 1): {gap_info}")

    # Print grand totals
    for key, total in grand_totals.items():
        target_key = key.replace("Grand", "Target").strip()
        advanced_key = key.replace("Grand", "Advanced").strip()
        if use_superscored_percentage:
            max_possible_score = master_dict[target_key][1] + master_dict[advanced_key][1]
            percentage = calculate_superscored_percentage(total, max_possible_score)
        else:
            percentage = calculate_previous_percentage(total, (
                        len(objectives_lists[target_key]) + len(objectives_lists[advanced_key])) * num_vendors)
        print(f"{key}: {total}, percentage: {percentage:.2f}%")


if __name__ == "__main__":
    # Set this flag to True or False to choose between superscored percentage and previous method
    use_superscored_percentage = True
    main(use_superscored_percentage)
