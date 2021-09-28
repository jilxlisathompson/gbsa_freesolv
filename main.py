from gbsa_run import *
from aimd_run import *
import pandas as pd



def main():

    # run aimd
    database_data_fp = "/home/eh19686/gbsa_freesolv/FreeSolv_data_ALL.xlsx"
    fraction = 1.0
    creation_fp = "/home/eh19686/gbsa_freesolv/new_xyzs"
    input_xyz = "/home/eh19686/gbsa_freesolv/og_xyz/outputs"
    output_fp = "/home/eh19686/gbsa_freesolv/aimd_output"
    steps = list(range(0, 1100, 1000))
    reference_data_df = run_frac(database_data_fp, fraction, creation_fp, input_xyz, output_fp, steps)

    # run gbsa

    input_fp = creation_fp
    os.chdir(input_fp)

    output_dict = run_gbsa_dirs(input_fp)
    output_df = convert_dict_pd_df(output_dict, reference_data_df)
    # saving pd.DataFrame as excel
    final_output_fp = "/home/eh19686/gbsa_freesolv/output"
    output_df.to_excel(os.path.join(final_output_fp, "gbsa_output.xlsx"))


if __name__ == "__main__":
    main()
