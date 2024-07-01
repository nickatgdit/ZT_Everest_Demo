import csv

# Step 1: Read data.csv and calculate objective totals
objective_totals = {}

with open('data.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        objective_number = row[0].strip()  # Assuming objective number is in the first column
        total = sum(float(value) for value in row[1:] if value.strip())  # Sum values for each row
        objective_totals[objective_number] = total

# Step 2: Calculate totals for each list
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

# Function to calculate total for a list of objectives
def calculate_list_total(objective_list, objective_totals):
    total = 0
    for objective in objective_list:
        if objective in objective_totals:
            total += objective_totals[objective]
    return total

# Calculate totals for each list
user_target_total = calculate_list_total(user_target_objectives, objective_totals)
user_advanced_total = calculate_list_total(user_advanced_objectives, objective_totals)
device_target_total = calculate_list_total(device_target_objectives, objective_totals)
device_advanced_total = calculate_list_total(device_advanced_objectives, objective_totals)
application_workload_target_total = calculate_list_total(application_workload_target_objectives, objective_totals)
application_workload_advanced_total = calculate_list_total(application_workload_advanced_objectives, objective_totals)
data_target_total = calculate_list_total(data_target_objectives, objective_totals)
data_advanced_total = calculate_list_total(data_advanced_objectives, objective_totals)
network_environment_target_total = calculate_list_total(network_environment_target_objectives, objective_totals)
network_environment_advanced_total = calculate_list_total(network_environment_advanced_objectives, objective_totals)
automation_orchestration_target_total = calculate_list_total(automation_orchestration_target_objectives, objective_totals)
automation_orchestration_advanced_total = calculate_list_total(automation_orchestration_advanced_objectives, objective_totals)
visibility_analytics_target_total = calculate_list_total(visibility_analytics_target_objectives, objective_totals)
visibility_analytics_advanced_total = calculate_list_total(visibility_analytics_advanced_objectives, objective_totals)

# Function to calculate percentage
def calculate_percentage(total, count):
    if count == 0:
        return 0.0
    return (total / count) * 100

# Dictionary with categories and their totals
master_dict = {
    "User: Target": user_target_total,
    "User: Advanced": user_advanced_total,
    "Device: Target": device_target_total,
    "Device: Advanced": device_advanced_total,
    "Application & Workload: Target": application_workload_target_total,
    "Application & Workload: Advanced": application_workload_advanced_total,
    "Data: Target": data_target_total,
    "Data: Advanced": data_advanced_total,
    "Network & Environment: Target": network_environment_target_total,
    "Network & Environment: Advanced": network_environment_advanced_total,
    "Automation & Orchestration: Target": automation_orchestration_target_total,
    "Automation & Orchestration: Advanced": automation_orchestration_advanced_total,
    "Visibility & Analytics: Target": visibility_analytics_target_total,
    "Visibility & Analytics: Advanced": visibility_analytics_advanced_total
}

# Lists of objectives corresponding to each category
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

# Read existing lines from totals.txt
with open('totals.txt', 'r') as file:
    lines = file.readlines()

# Process each line in the file
updated_lines = []
for line in lines:
    parts = line.strip().split(',')
    if len(parts) >= 3:  # Ensure there are at least 3 parts (to check key)
        key = parts[2].strip()
        if key in master_dict:
            updated_value = master_dict[key]
            objectives_list = objectives_lists[key]
            updated_percentage = calculate_percentage(updated_value, len(objectives_list) * 35)  # Calculate percentage
            updated_line = f"{parts[0]},{parts[1]},{parts[2]},{updated_percentage:.2f}%\n"  # Update line with percentage and percentage sign
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)  # If key not found in master_dict, keep original line
    else:
        updated_lines.append(line)  # If line doesn't have at least 3 parts, keep original line

# Write updated lines back to totals.txt
with open('totals.txt', 'w') as file:
    file.writelines(updated_lines)

print("totals.txt has been updated successfully.")

# Print statements with percentage calculation
print(f"User Target Total: {user_target_total}, with count of {len(user_target_objectives) * 35}, percentage: {calculate_percentage(user_target_total, len(user_target_objectives) * 35):.2f}%")
print(f"User Advanced Total: {user_advanced_total}, with count of {len(user_advanced_objectives) * 35}, percentage: {calculate_percentage(user_advanced_total, len(user_advanced_objectives) * 35):.2f}%")
print(f"Device Target Total: {device_target_total}, with count of {len(device_target_objectives) * 35}, percentage: {calculate_percentage(device_target_total, len(device_target_objectives) * 35):.2f}%")
print(f"Device Advanced Total: {device_advanced_total}, with count of {len(device_advanced_objectives) * 35}, percentage: {calculate_percentage(device_advanced_total, len(device_advanced_objectives) * 35):.2f}%")
print(f"Application & Workload Target Total: {application_workload_target_total}, with count of {len(application_workload_target_objectives) * 35}, percentage: {calculate_percentage(application_workload_target_total, len(application_workload_target_objectives) * 35):.2f}%")
print(f"Application & Workload Advanced Total: {application_workload_advanced_total}, with count of {len(application_workload_advanced_objectives) * 35}, percentage: {calculate_percentage(application_workload_advanced_total, len(application_workload_advanced_objectives) * 35):.2f}%")
print(f"Data Target Total: {data_target_total}, with count of {len(data_target_objectives) * 35}, percentage: {calculate_percentage(data_target_total, len(data_target_objectives) * 35):.2f}%")
print(f"Data Advanced Total: {data_advanced_total}, with count of {len(data_advanced_objectives) * 35}, percentage: {calculate_percentage(data_advanced_total, len(data_advanced_objectives) * 35):.2f}%")
print(f"Network & Environment Target Total: {network_environment_target_total}, with count of {len(network_environment_target_objectives) * 35}, percentage: {calculate_percentage(network_environment_target_total, len(network_environment_target_objectives) * 35):.2f}%")
print(f"Network & Environment Advanced Total: {network_environment_advanced_total}, with count of {len(network_environment_advanced_objectives) * 35}, percentage: {calculate_percentage(network_environment_advanced_total, len(network_environment_advanced_objectives) * 35):.2f}%")
print(f"Automation & Orchestration Target Total: {automation_orchestration_target_total}, with count of {len(automation_orchestration_target_objectives) * 35}, percentage: {calculate_percentage(automation_orchestration_target_total, len(automation_orchestration_target_objectives) * 35):.2f}%")
print(f"Automation & Orchestration Advanced Total: {automation_orchestration_advanced_total}, with count of {len(automation_orchestration_advanced_objectives) * 35}, percentage: {calculate_percentage(automation_orchestration_advanced_total, len(automation_orchestration_advanced_objectives) * 35):.2f}%")
print(f"Visibility & Analytics Target Total: {visibility_analytics_target_total}, with count of {len(visibility_analytics_target_objectives) * 35}, percentage: {calculate_percentage(visibility_analytics_target_total, len(visibility_analytics_target_objectives) * 35):.2f}%")
print(f"Visibility & Analytics Advanced Total: {visibility_analytics_advanced_total}, with count of {len(visibility_analytics_advanced_objectives) * 35}, percentage: {calculate_percentage(visibility_analytics_advanced_total, len(visibility_analytics_advanced_objectives) * 35):.2f}%")
