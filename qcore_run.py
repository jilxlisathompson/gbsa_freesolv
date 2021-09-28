from qcore_run_strings import *
import subprocess
import json


def run_qcore_aimd(input_file: str) -> str:
    aimd_input = aimd_run_str(input_file)
    qcore_input_command_str = qcore_run_command()

    qcore_output = subprocess.run(qcore_input_command_str +
                                  '"' + aimd_input + '"',
                                  capture_output=True, text=True, shell=True)
    print(input_file)
    print(qcore_output.stderr)
    if qcore_output.returncode == 0:
        return qcore_output.stdout
    elif qcore_output.returncode != 0:
        return qcore_output.stderr


def run_qcore_gas(input_file: str):
    qcore_input_command_str = qcore_run_command()

    gas_input = gbsa_gas_run_str(input_file)
    qcore_output = subprocess.run(qcore_input_command_str +
                                  '"' + gas_input + '"',
                                  capture_output=True, text=True, shell=True)
    print(qcore_output.stdout)
    if qcore_output.returncode == 0:
        return qcore_output.stdout
    elif qcore_output.returncode != 0:
        return qcore_output.stderr


def run_qcore_solvation(input_file: str):
    qcore_input_command_str = qcore_run_command()

    solvation_input = gbsa_solvation_run_str(input_file)
    qcore_output = subprocess.run(qcore_input_command_str +
                                  '"' + solvation_input + '"',
                                  capture_output=True, text=True, shell=True)
    print(qcore_output.stderr)
    if qcore_output.returncode == 0:
        return qcore_output.stdout
    elif qcore_output.returncode != 0:
        return qcore_output.stderr


##### HERE #######
def run_calcType(input_file: str, calcType: str) -> str:
    if calcType == "aimd":
        return run_qcore_aimd(input_file)
    elif calcType == "gas":
        return run_qcore_gas(input_file)
    elif calcType == "solvation":
        return run_qcore_solvation(input_file)


def qcore_gbsa_energies(input_file: str) -> dict:
    qcore_output_solvation = run_calcType(input_file, "solvation")

    #     print(json.loads(qcore_output_solvation))

    qcore_results_solvation = json.loads(qcore_output_solvation)

    qcore_output_gas = run_calcType(input_file, "gas")

    qcore_results_gas = json.loads(qcore_output_gas)

    gb_energy = qcore_results_solvation["gb_run"]["energy"]
    gas_energy = qcore_results_gas["gas_run"]["energy"]
    solvation_energy = gb_energy - gas_energy

    return solvation_energy

