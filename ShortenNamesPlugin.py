# Objective:
#   The purpose of this script is to
#       1) remove the lineage from the bacterial name to be able to put the label on network graph
#       2) remove unclassified bacteria to reduce noise

import pandas as pd

def shorten_names(abundance_file, out_file):
    # Assume that samples column is unnamed

    abundance_df = pd.read_csv(abundance_file)
    columns = list(abundance_df.columns)
    columns.remove("Unnamed: 0")

    # Step 1 - remove unclassified bacteria
    columns_to_remove  =[]
    for column in columns:
        if column.split(";")[5]=="__" or column.split(";")[5]=="g__":
            columns_to_remove.append(column)
    abundance_df = abundance_df.drop(columns_to_remove, axis=1)

    # Step 2 - rename columns
    columns = list(abundance_df.columns)
    columns.remove("Unnamed: 0")

    rename_dict = {}
    taxa_count_dict = {}

    for column in columns:
        genus_name = column.split(";")[5].split("__")[1]
        if genus_name not in taxa_count_dict.keys():
            taxa_count_dict[genus_name] = 1
        else:
            taxa_count_dict[genus_name] += 1

        rename_dict[column] = genus_name + ".0" + str(taxa_count_dict[genus_name])
    abundance_df = abundance_df.rename(columns=rename_dict)
    abundance_df = abundance_df.rename(columns={"Unnamed: 0":''})
    abundance_df.to_csv(out_file, index=False)


    all_bacterial_names = list(rename_dict.values())
    print()
    print("file {}".format(abundance_file))
    print("number of bacterias: {}".format(len(all_bacterial_names)))
    print("Columns are successfully renamed.")
    for element in all_bacterial_names:
        if all_bacterial_names.count(element)>1:
            print(element)


class ShortenNamesPlugin:
    def input(self, infile):
        self.inputfile = infile

    def run(self):
        pass

    def output(self, outputfile):
        shorten_names(self.inputfile, outputfile)
