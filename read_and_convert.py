import pandas as pd
import os
import re
import glob

# read freesolv data into pandas data frame
def reference_data(data_fp: str, fraction: float) -> pd.DataFrame:
    """ fraction = fraction of database to use for calculation, out of 100%
    """

    # data is in xlsx form
    #     os.chdir(data_fp)

    data_df = pd.read_excel(data_fp)
    calc_df = data_df.sample(frac=fraction)

    return calc_df

def creates_master_ds(creation_fp: str, calc_df: pd.DataFrame) -> None:
    """
    creates directorys for aimd xyz outputs
    """
    os.chdir(creation_fp)
#     print(calc_df)
    # takes filehandles and creates directories in creation_fp
    for (columnName, columnData) in calc_df.iteritems():
        if columnName == "FileHandle":
            names = columnData.tolist()
    for file in names:
        os.mkdir(file+ "opt")
    return None


def extract_coords(root_fp: str, FP_coords: str, step_num: int):
    atom_names = []
    all_coords = []
    os.chdir(root_fp)
    with open(FP_coords) as file:
        num_atoms = file.readline()
        for line in file:
            if re.findall(r"\w+ep %i" % (step_num), line):
                for line_s in file:
                    atom_name = re.findall(r'[A-Z] |[A-Z][a-z]\s', line_s)[0:1]
                    print("in extract_coords")
                    atom_names.append(atom_name)
                    all_coords.append(re.split("\s+", line_s)[1:4])
                    if line_s == "\n":
                        break
                    if line_s == num_atoms:
                        break

    atomTypes = [''.join(ele) for ele in atom_names]
    print(atomTypes)

    x_coord = []
    y_coord = []
    z_coord = []
    print("------")
    for i in all_coords:
        x_coord.append(i[0:1])
        y_coord.append(i[1:2])
        z_coord.append(i[-1])

    coords_X = [];
    coords_Y = [];
    coords_Z = []
    x_coords = []
    y_coords = []
    z_coords = []
    for i in x_coord:
        coords_X.append(i[0])

    # print(x_coords)
    for i in y_coord:
        i = '[]'.join(i)
        #         print(i)
        coords_Y.append(i)
    for i in z_coord:
        coords_Z.append(i)
    return coords_X, coords_Y, coords_Z, atomTypes, num_atoms

def write_xyz(fout,x_coords, y_coords, z_coords, atomtypes, file_name,natoms):
    """
    fout: open file
    coords: np.array of coordinates
    title: title section
    atomtypes: interatable list of atomtypes
    no_atoms : int, total number of atoms
    """
    print(file_name)
    natoms = int(natoms)
    fout.write("{a}\n{b}\n" .format(a=natoms,b="FreeSolv water"))
    print("atomtypes here in write_xyz")
    print((atomtypes))
#     print(file_name)
    for i in range(natoms):
        print("i_natoms from write_XYZ")
        print(i)
        fout.write("{} \t {} \t {} \t {}\n" .format(atomtypes[i], x_coords[i], y_coords[i], z_coords[i]))


def master_read_all(steps: list, all_path: str, output_fp: str) -> None:
    #     print(output_fp)

    os.chdir(all_path)
    print(output_fp)
    for file in glob.glob("*_output.xyz"):
        print("file = ", file)
        for i_steps in steps:
            # print(name)
            file_name = file.split("_")[0] + "_" + file.split("_")[1]
            print("step = {a}".format(a=i_steps))
            # calling function to extract coordinates
            x_coords, y_coords, z_coords, atom_names, num_atoms = extract_coords(all_path, file, i_steps)
            print("here num %s" % num_atoms)
            # writing coords to file and store in directory
            # creating file in file_name dir
            print("steps = ", i_steps)
            print(os.path.join(output_fp, file_name, "step" + "_" + str(i_steps) + ".xyz"))
            f_newfile = open(os.path.join(output_fp, file_name, "step" + "_" + str(i_steps) + ".xyz"), 'w')
            # writing file in dirs
            write_xyz(f_newfile, x_coords, y_coords, z_coords, atom_names, file_name, num_atoms)
    return None

