def qcore_run_command() -> str:
    qcore_locale = "/Users/eh19686/Programs/Qcore/cmake-build-release/qcore"
    # TODO change hardcoded shiz

    qcore_run_str = qcore_locale + " -f json -s "

    return qcore_run_str


def aimd_run_str(input_file: str) -> str:
    output_file_name = input_file.split(".")[0] + "_output"
    input_str = """aimd_run := aimd(
      n_steps = 11000
      time_step = 1 fs
      structure( file = '{input_file}' )
      velocities(
        sampling = 'thermal'
        temperature = 300 kelvin
      )
      gradient(
        xtb(
          temperature = 300 kelvin
          solvation(solvent=water degeneracy_threshold=0.0)
!          charge = CHGSUB
        )
      )
      output_steps = 1000
      output_coordinates = {output_file_name}
      save_to_file = true
      thermostat(
        type = 'andersen'
        temperature = 300 kelvin
        coupling_time = 0.02 ps
      )
    )""".format(input_file=input_file, output_file_name=output_file_name)
    #                 os.path.join(aimd_output_fp, output_file_name))

    return input_str


def gbsa_solvation_run_str(input_file: str) -> str:
    " gbsa solvation calculation input structure string"
    input_str = """gb_run := xtb( 
                            structure(file = '{input_file}')
                            solvation(
                            model = gbsa
                            solvent = {solvent}))""".format(input_file=input_file, solvent="water")
    return input_str


def gbsa_gas_run_str(input_file: str) -> str:
    input_str = """gas_run := xtb( 
                            structure(file = '{input_file}')
                            )""".format(input_file=input_file)

    return input_str


def gbsa_calculation(input_file: str, type_calc: str) -> str:
    if type_calc == "gas":
        gbsa_gas_run_str(input_file)
    elif type_calc == "solvation":
        gbsa_solvation_run_str(input_file)
