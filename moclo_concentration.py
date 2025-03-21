
import os
import pandas as pd

def parse_csv(path=os.getcwd(), file_name="table.csv"):
    files = [f for f in os.listdir(path) if f == file_name]
    
    for file in files:
        # Read lines from the CSV file
        with open(os.path.join(path, file), "r") as csv_file:
            lines = csv_file.readlines()

        row_count = sum(1 for row in lines)

        fragments_read = pd.read_csv(os.path.join(path,file), skiprows=0, nrows=row_count)

        # print(fragments_read)

        if fragments_read is not None:
            
            #These values are not present in the downloaded tables, this is only a placeholder
            total_lengths = fragments_read["Total"]
            
            insert_lengths = fragments_read["Length"]

            stock_vol = 0.5 * 10**-6 #ul
            total_mol = 50 * 10**-15 #fmol

            output_df = pd.DataFrame()
            output_values = [id for id in range(0, row_count - 1)]

            for i in output_values:

                moles_liter = total_mol / stock_vol
                con_g_L_bp = 650 * moles_liter
                length_total = total_lengths[i]
                length_insert = insert_lengths[i]
                bp_ratio = length_insert / length_total
                needed_conc = 10**3 * (length_total * con_g_L_bp) / bp_ratio 


                # plasmid_dna_ng = stock_vol * final_stock_conc_ngul
                # fragments_ng = plasmid_dna_ng / (total_lengths[i] / insert_lengths[i])
                # total_fmol = (650 * 0.000001 * insert_lengths[i])

                output_values[i] = needed_conc
            
            output_df["Sequence"] = fragments_read["Sequence"]
            output_df["Total Bases"] = total_lengths
            output_df["Insert Bases"] = insert_lengths
            output_df["Stock mol"] = [total_mol for id in range(0, row_count - 1)]
            output_df["Stock Volume L"] = [stock_vol for id in range(0, row_count - 1)]
            output_df["Final Stock Concentration ng/ul"] = output_values

            print(output_df)
            

        else:
            return


if __name__ == "__main__":
    parse_csv()