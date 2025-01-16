import argparse
import hashlib
import os
import sys

import pandas as pd
from bs4 import BeautifulSoup


def extract_table(file_path, h1_text=None, h2_text=None):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Locate specific <h1> and <h2> elements
        h1_tag = soup.find("h1", string=h1_text) if h1_text else None
        h2_tag = (
            soup.find("h2", string=h2_text)
            if h1_tag is None
            else h1_tag.find_next("h2", string=h2_text)
        )

        # Determine the starting point to search for the table
        start_point = h2_tag if h2_tag else h1_tag

        if not start_point:
            print(
                f"No valid <h1> or <h2> header specified in {
                    file_path}.  Skipping this file.\n"
            )
            return None

        # find the first <table> after the header
        table = start_point.find_next("table")
        if not table:
            print(
                f"No table found under the specified headers in {
                    file_path}.  Skipping this file.\n"
            )
            return None

        # Extract table rows and cells
        rows = table.find_all("tr")
        table_data = []
        for row in rows:
            cells = row.find_all(["td", "th"])
            table_data.append([cell.get_text(strip=True) for cell in cells])

        # convert to dataframe
        df = pd.DataFrame(table_data)

        # set first row as column headers
        if not df.empty:
            df.columns = df.iloc[0]
            df = df.iloc[1:]

        # reset index and return
        df = df.reset_index(drop=True)

        return df


def get_hash(df):

    # sample first 100 'Match ID' values
    match_id_sample = "".join(df["Match ID"].astype(str).head(100))

    # generate hash
    file_hash = hashlib.sha256(match_id_sample.encode()).hexdigest()[:8]

    return file_hash


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract BO6 tables from Activision user files."
    )

    # source directory argument
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default=os.getcwd(),
        help="Directory containing source HTML files.  Default is current.",
    )

    # output directory argument
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=os.getcwd(),
        help="Directory to save output .csv files to.  Default is current.",
    )

    return parser.parse_args()


def validate_dir(source_dir, output_dir):
    # check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    # check if output directory exists, create if necessary
    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' does not exist.  Creating it...")
        os.makedirs(output_dir)


def main():

    # get directory paths
    args = parse_arguments()

    # get file paths
    source_dir = os.path.abspath(args.source)
    output_dir = os.path.abspath(args.output)

    # validate directories
    validate_dir(source_dir, output_dir)

    print(f"\nSource directory: {source_dir}")
    print(f"Output directory: {output_dir}\n")

    # specify header text
    h1_text = " Call of Duty: Black Ops 6"
    h2_text = "Multiplayer Match Data (reverse chronological)"

    # initialize counters
    files = 0
    fails = 0
    success = 0

    for filename in os.listdir(source_dir):
        if filename.endswith(".html"):
            file_path = os.path.join(source_dir, filename)
            print(f"Processing {file_path}...")

            # extract table
            extracted_table = extract_table(file_path, h1_text=h1_text, h2_text=h2_text)

            # save out table
            if extracted_table is not None:
                # add leading ' to valules in Match ID column so handled as string
                extracted_table["Match ID"] = "'" + extracted_table["Match ID"].astype(
                    str
                )

                # get hash value for filename
                file_hash = get_hash(extracted_table)

                # save csv
                output_filename = f"bo6_data_{file_hash}.csv"
                output_filepath = os.path.join(output_dir, output_filename)
                extracted_table.to_csv(output_filepath, index=False)

                print(f"File saved as: {output_filepath}\n")
                files += 1
                success += 1

            else:
                files += 1
                fails += 1

    print(f"\n{files} files processed, {success} successfully, {fails} failed.")


if __name__ == "__main__":
    main()
