# Script to convert an image or doc file to a csv
import csv
import itertools


from .preprocessor import process_file


def file2csv(
    file_path,
    table_data,
    output_table="output_table.csv",
    output_info="output_info.csv",
):
    text = process_file(file_path, table_data)
    data = text["table"]
    data = [i for i in itertools.zip_longest(*data, fillvalue="")]
    print(data)

    with open(output_table, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerows(data)

    with open(output_info, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["position", "text"])
        csv_writer.writerow(["top", text["top"].replace("\n", "\\n")])
        csv_writer.writerow(["bottom", text["bottom"].replace("\n", "\\n")])

    return (data, (text["top"], text["bottom"]))
