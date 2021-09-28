from qcore_run import *
import glob
import numpy as np
import os
import pandas as pd

def split_word(word):
    list_of_str = [char for char in word]
    del list_of_str[-3:]
    list_of_str = "".join(list_of_str)
    return list_of_str


def run_gbsa(input_fp: str) -> dict:
    """ runs gbsa for dataset and return dict of energy
    average over steps along with filename
    """
    print("here in run_gbsa")
    #     print(input_fp)
    #     os.chdir(input_fp)
    output_dict = {}
    #     print(os.getcwd())

    for input_file in sorted(glob.glob("step_*.xyz")):
        step_name = (input_file.split("_"))[1]
        output_dict[step_name] = qcore_gbsa_energies(input_file)

    # convert to pandas dataframe dict -> pd.DataFrame
    average_energy = np.array(list(output_dict.values())).mean()

    return average_energy


def run_gbsa_dirs(input_fp: str) -> dict:
    """
    returns a dict of the form {mobley_****** : energy}
    """

    output_dict = {}
    for dirs in sorted(os.listdir(input_fp)):
        os.chdir(os.path.join(input_fp, dirs))
        filename = split_word(dirs)
        print(dirs)
        output_dict[filename] = run_gbsa(dirs)


    return output_dict


def convert_dict_pd_df(output_dict: str, reference_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    return pd.DataFrame --> FileHandle | calcDGsolv / Ha | expDGsolv/ kcal/mol
    convert Ha -> kcal/mol
    """
    hartree2kcal = 627.5096080305927
    # read in experimental data
    # convert dict to pandas dataframe

    all_data_df = pd.DataFrame(output_dict.keys(), columns=["FileHandle"])
    all_data_df["calc_DGsolv"] = pd.DataFrame(output_dict.values()) * hartree2kcal
    all_data_df = all_data_df.sort_values(by=['FileHandle'])
    reference_data_df = reference_data_df.sort_values(by=['FileHandle'])
    print(all_data_df)
    print(reference_data_df)

    #     all_data_df['exp_DGsolv'] = np.where((all_data_df['FileHandle'] == reference_data_df['FileHandle']) )
    #     if all_data_df["FileHandle"] == reference_data_df["FileHandle"]:

    all_data_df["exp_DGsolv"] = reference_data_df["expDGsolv"].values.tolist()
    # get experimental data

    return all_data_df