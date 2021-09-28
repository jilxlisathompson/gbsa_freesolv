from read_and_convert import *
from qcore_run import *

def run_amid_per_file(input_file: str, aimd_output_fp: str):

    os.chdir(aimd_output_fp)

    run_qcore_aimd(input_file)

    print("input file = ", input_file)

    return None


def run_frac(database_data_fp: str, fraction: float, creation_fp: str, \
             input_xyz: str, output_fp: str, steps: list) -> list:
    """
    returns reference_data_df so that it can be used in gbsa calculations
    # fix write function that does all calculations so that reference_data_df doesnt have to be
    recreated <----- NOTE!
    """
    reference_data_df = reference_data(database_data_fp, fraction)
    names = reference_data_df["FileHandle"].values.tolist()
    # create final output xyz directories
    creates_master_ds(creation_fp, reference_data_df)
    #     for roots, dirs, files in sorted(os.walk(output_fp))
    for files in names:
        files = files + "opt.xyz"
        # run aimd
        run_amid_per_file(files, input_xyz)

        # read master xyz output + write new xyz
        master_read_all(steps, input_xyz, creation_fp)

    return reference_data_df
