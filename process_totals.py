import csv

# Function to calculate total for a list of objectives
def calculate_list_total(objective_list, objective_totals):
    total = 0
    for objective in objective_list:
        if objective in objective_totals:
            total += objective_totals[objective]
    return total

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

def main(use_superscored_percentage=True):
    # Step 1: Read data.csv and calculate objective totals
    objective_totals = {}
    with open('data.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            objective_number = row[0].strip()  # Assuming objective number is in the first column
            total = sum(float(value) for value in row[1:] if value.strip())  # Sum values for each row
            objective_totals[objective_number] = total

    # Step 2: Define objective lists
    user_target_objectives = [
        '1.1.1', '1.2.1', '1.2.2', '1.3.1', '1.4.1', '1.4.2', '1.5.1', '1.5.2', '1.6.1', '1.7.1', '1.8.1', '1.8.2', '1.9.1'
    ]
    user_advanced_objectives = [
        '1.2.3', '1.2.4', '1.2.5', '1.3.2', '1.4.3', '1.4.4', '1.5.3', '1.5.4', '1.6.2', '1.8.3', '1.8.4', '1.9.3'
    ]
    device_target_objectives = [
        '2.1.1', '2.1.2', '2.1.3', '2.2.1', '2.3.2', '2.3.3', '2.4.1', '2.4.2', '2.5.1', '2.6.1', '2.6.2', '2.7.1', '2.7.2'
    ]
    device_advanced_objectives = [
        '2.1.4', '2.2.2', '2.3.1', '2.3.5', '2.3.6', '2.3.7', '2.4.3', '2.4.4', '2.7.3'
    ]
    application_workload_target_objectives = [
        '3.1.1', '3.1.2', '3.1.3', '3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.4.1', '3.4.2', '3.4.3', '3.5.1'
    ]
    application_workload_advanced_objectives = [
        '3.2.4', '3.4.4', '3.5.2'
    ]
    data_target_objectives = [
        '4.1.1', '4.2.1', '4.2.2', '4.2.3', '4.3.1', '4.3.2', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.5.3', '4.6.1', '4.6.2', '4.7.1'
    ]
    data_advanced_objectives = [
        '4.3.3', '4.3.4', '4.3.5', '4.4.5', '4.4.6', '4.5.4', '4.5.5', '4.6.3', '4.6.4', '4.7.2', '4.7.3', '4.7.5', '4.7.6', '4.7.7'
    ]
    network_environment_target_objectives = [
        '5.1.1', '5.1.2', '5.2.1', '5.2.2', '5.2.3', '5.2.4', '5.2.5', '5.3.1', '5.3.2'
    ]
    network_environment_advanced_objectives = [
        '5.4.1', '5.4.2', '5.4.3'
    ]
    automation_orchestration_target_objectives = [
        '6.1.1', '6.1.2', '6.1.3', '6.2.1', '6.2.2', '6.3.1', '6.5.1', '6.5.2', '6.6.1', '6.6.2', '6.6.3', '6.7.1', '6.7.2'
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

    # Step 3: Calculate totals and max possible scores for each list
    user_target_total = calculate_list_total(user_target_objectives, objective_totals)
    user_target_max = calculate_max_possible_score(user_target_objectives, max_score_per_objective)
    user_advanced_total = calculate_list_total(user_advanced_objectives, objective_totals)
    user_advanced_max = calculate_max_possible_score(user_advanced_objectives, max_score_per_objective)
    device_target_total = calculate_list_total(device_target_objectives, objective_totals)
    device_target_max = calculate_max_possible_score(device_target_objectives, max_score_per_objective)
    device_advanced_total = calculate_list_total(device_advanced_objectives, objective_totals)
    device_advanced_max = calculate_max_possible_score(device_advanced_objectives, max_score_per_objective)
    application_workload_target_total = calculate_list_total(application_workload_target_objectives, objective_totals)
    application_workload_target_max = calculate_max_possible_score(application_workload_target_objectives, max_score_per_objective)
    application_workload_advanced_total = calculate_list_total(application_workload_advanced_objectives, objective_totals)
    application_workload_advanced_max = calculate_max_possible_score(application_workload_advanced_objectives, max_score_per_objective)
    data_target_total = calculate_list_total(data_target_objectives, objective_totals)
    data_target_max = calculate_max_possible_score(data_target_objectives, max_score_per_objective)
    data_advanced_total = calculate_list_total(data_advanced_objectives, objective_totals)
    data_advanced_max = calculate_max_possible_score(data_advanced_objectives, max_score_per_objective)
    network_environment_target_total = calculate_list_total(network_environment_target_objectives, objective_totals)
    network_environment_target_max = calculate_max_possible_score(network_environment_target_objectives, max_score_per_objective)
    network_environment_advanced_total = calculate_list_total(network_environment_advanced_objectives, objective_totals)
    network_environment_advanced_max = calculate_max_possible_score(network_environment_advanced_objectives, max_score_per_objective)
    automation_orchestration_target_total = calculate_list_total(automation_orchestration_target_objectives, objective_totals)
    automation_orchestration_target_max = calculate_max_possible_score(automation_orchestration_target_objectives, max_score_per_objective)
    automation_orchestration_advanced_total = calculate_list_total(automation_orchestration_advanced_objectives, objective_totals)
    automation_orchestration_advanced_max = calculate_max_possible_score(automation_orchestration_advanced_objectives, max_score_per_objective)
    visibility_analytics_target_total = calculate_list_total(visibility_analytics_target_objectives, objective_totals)
    visibility_analytics_target_max = calculate_max_possible_score(visibility_analytics_target_objectives, max_score_per_objective)
    visibility_analytics_advanced_total = calculate_list_total(visibility_analytics_advanced_objectives, objective_totals)
    visibility_analytics_advanced_max = calculate_max_possible_score(visibility_analytics_advanced_objectives, max_score_per_objective)

    # Step 4: Prepare master dictionary and objectives lists
    master_dict = {
        "User: Target": (user_target_total, user_target_max),
        "User: Advanced": (user_advanced_total, user_advanced_max),
        "Device: Target": (device_target_total, device_target_max),
        "Device: Advanced": (device_advanced_total, device_advanced_max),
        "Application & Workload: Target": (application_workload_target_total, application_workload_target_max),
        "Application & Workload: Advanced": (application_workload_advanced_total, application_workload_advanced_max),
        "Data: Target": (data_target_total, data_target_max),
        "Data: Advanced": (data_advanced_total, data_advanced_max),
        "Network & Environment: Target": (network_environment_target_total, network_environment_target_max),
        "Network & Environment: Advanced": (network_environment_advanced_total, network_environment_advanced_max),
        "Automation & Orchestration: Target": (automation_orchestration_target_total, automation_orchestration_target_max),
        "Automation & Orchestration: Advanced": (automation_orchestration_advanced_total, automation_orchestration_advanced_max),
        "Visibility & Analytics: Target": (visibility_analytics_target_total, visibility_analytics_target_max),
        "Visibility & Analytics: Advanced": (visibility_analytics_advanced_total, visibility_analytics_advanced_max)
    }

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
                objectives_list = objectives_lists[key]
                if use_superscored_percentage:
                    updated_percentage = calculate_superscored_percentage(total, max_possible_score)
                else:
                    updated_percentage = calculate_previous_percentage(total, len(objectives_list) * 35)
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
            percentage = calculate_previous_percentage(total, len(objectives_lists[key]) * 35)
        print(f"{key}: {total}, with {'max possible score' if use_superscored_percentage else 'count of'} {max_score}, percentage: {percentage:.2f}%")

if __name__ == "__main__":
    # Set this flag to True or False to choose between superscored percentage and previous method
    use_superscored_percentage = True
    main(use_superscored_percentage)
