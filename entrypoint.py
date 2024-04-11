import csv
from scipy.stats import f_oneway, tukey_hsd
import matplotlib.pyplot as plt

def create_dictionary_from_csv(csv_file):
    # Initialize an empty dictionary
    data_dict = {}

    # Open the CSV file
    with open(csv_file, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Skip empty rows
            if not row:
                continue
            # Assuming the first column is the name tag and the second column is the location
            name_tag = row[0]
            location = row[1]
            # Add key-value pair to the dictionary
            data_dict[name_tag] = location

    return data_dict


def traverse_row_and_check(csv_file, start_index, data_dict, target_value):
    # Open the CSV file
    with open(csv_file, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Read the first row
        first_row = next(csv_reader)

        # Check if the start index is valid
        if start_index < 0 or start_index >= len(first_row):
            print("Start index is out of range")
            return

        # Initialize an empty list to store matching values
        matching_values = []

        # Iterate through the cells starting from the specified index
        for cell_index in range(start_index, len(first_row)):
            # Get the cell value
            cell_value = first_row[cell_index][1:]
            # Check if the cell value is a key in the dictionary and equals the target value
            if cell_value in data_dict and data_dict[cell_value] == target_value:
                matching_values.append(cell_value)

        return matching_values


def filter_csv(input_csv, output_csv, target_phylum):
    # Open the input CSV file for reading and the output CSV file for writing
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        # Create CSV reader and writer objects
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        # Write the header row to the output CSV file
        header = next(csv_reader)
        csv_writer.writerow(header)

        # Iterate through each row in the input CSV file
        for row in csv_reader:
            # Assuming the phylum is in the second column (index 1)
            phylum = row[1]
            # Check if the phylum is equal to the target phylum
            if phylum == target_phylum:
                # Write the row to the output CSV file
                csv_writer.writerow(row)


def extract_values_from_csv(input_csv, keys_list):
    ABGcyano = []  # List to store values greater than 0 for ABG Standard Media

    # Open the onlycyano CSV file
    with open(input_csv, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Read the first row
        first_row = next(csv_reader)

        first_row = [cell[1:] for cell in first_row]
        # Iterate through the keys list
        for key in keys_list:

            # Iterate through the cells in the first row starting from index 2
            for i in range(2, len(first_row)):
                # Check if the key matches the cell value
                if first_row[i] == key:
                    # Reset the list to store values greater than 0 for each key
                    values_list = []

                    # Iterate through each row in the CSV file
                    for row in csv_reader:
                        # Convert cell value to integer (assuming they are numerical values)
                        cell_value = int(row[i]) if row[i].isdigit() else 0
                        # Add value to the list if it's greater than 0
                        if cell_value > 0:
                            values_list.append(cell_value)

                    # Add the values list to ABGcyano
                    ABGcyano.append(values_list)
                    # Reset the file pointer to the beginning of the file
                    file.seek(0)
                    # Skip the header row
                    next(csv_reader)
                    # Break the loop since the key has been found and processed
                    break

    return ABGcyano


def main():
    ##Create key/value dictionary for location tag to location conversion
    kvdict = create_dictionary_from_csv('.venv/richness_table.csv')
    del kvdict["Sample.name"]

    print(kvdict)

    csv_file = '.venv/full_table.csv'  # Replace 'data.csv' with your CSV file name
    start_index = 2  # Index to start traversing the row from (0-based index)
    target_value = "ABG Standard Media"
    target_value2 = "Rattle snake ledge"
    target_value3 = "Pond ledge"

    # The value to match in the dictionary
    ABG_keys = traverse_row_and_check(csv_file, start_index, kvdict, target_value)
    rattle_keys = traverse_row_and_check(csv_file, start_index, kvdict, target_value2)
    pond_keys = traverse_row_and_check(csv_file, start_index, kvdict, target_value3)

    input_csv = '.venv/full_table.csv'
    output_csv = 'onlycyano.csv'
    target_phylum = 'Cyanobacteria'
    filter_csv(input_csv, output_csv, target_phylum)

    onlycyano_csv = '.venv/onlycyano.csv'
    ABGcyano = extract_values_from_csv(onlycyano_csv, ABG_keys)
    ABGcyano_sum = 0
    for sublist in ABGcyano:
        ABGcyano_sum += sum(sublist)
    ABG_cyanosum = [sum(sublist) for sublist in ABGcyano]

    rattlecyano = extract_values_from_csv(onlycyano_csv, rattle_keys)
    rattlecyano_sum = 0
    for sublist in rattlecyano:
        rattlecyano_sum += sum(sublist)
    rattle_cyanosum = [sum(sublist) for sublist in rattlecyano]

    pondcyano = extract_values_from_csv(onlycyano_csv, pond_keys)
    pondcyano_sum = 0
    for sublist in pondcyano:
        pondcyano_sum += sum(sublist)
    pond_cyanosum = [sum(sublist) for sublist in pondcyano]

    print(ABG_cyanosum)
    print(rattle_cyanosum)
    print(pond_cyanosum)

    lists = [ABG_cyanosum, rattle_cyanosum, pond_cyanosum]
    max_length = max(len(lst) for lst in lists)
    normalized_lists = [lst + [0] * (max_length - len(lst)) for lst in lists]

    # Storing each normalized list into separate lists
    abgnormalized = normalized_lists[0]

    rattlenormalized = normalized_lists[1]

    pondnormalized = normalized_lists[2]


    ##ABGmean = sum(abgnormalized) / len(abgnormalized)
    ##rattlemean = sum(rattlenormalized) / len(rattlenormalized)
    ##pondmean = sum(pondnormalized) / len(pondnormalized)

    print(f_oneway(abgnormalized, rattlenormalized, pondnormalized))
    print(tukey_hsd(abgnormalized, rattlenormalized, pondnormalized))

    ##fig, ax = plt.subplots(1, 1)
    ##ax.boxplot([ABG_cyanosum, rattle_cyanosum, pond_cyanosum])
    ##ax.set_xticklabels(["abg", "rattle", "pond"])
    ##ax.set_ylabel("mean")
    ##plt.show()

    data = {'ABG': ABGcyano_sum, 'Rattlesnake Ledge': rattlecyano_sum, 'Pond Ledge': pondcyano_sum}

    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='green',
            width=0.4)

    plt.xlabel("Location")
    plt.ylabel("No. of cyanobacteria")
    plt.title("Total Cyanobacteria Concentration at Different Locations")
    plt.show()



if __name__ == "__main__":
    main()
