import os
import re
import pathlib
import subprocess

def validate(input_file_path, actual_file_path, expected_file_path):
    if not os.path.isfile(actual_file_path):
        print(f'{input_file_path}: El .jar no ha generado un fichero de salida')
        return False

    if not os.path.isfile(expected_file_path):
        print(f'{input_file_path}: No se encuentra el fichero {expected_file_path}, ¿qué has tocado?')
        return False

    with open(input_file_path, 'r') as src:
        src.readline()
        coins = [int(c) for c in src.readline().strip().split(' ')]
        amount = int(src.readline())

    solution_found = True
    with open(actual_file_path, 'r') as src:
        try:
            solution_num_coins = int(src.readline())
            solution_coins = [int(c) for c in src.readline().strip().split(' ')]
        except:
            solution_found = False

    solution_exists = True
    with open(expected_file_path, 'r') as src:
        try:
            minimum_num_coins = int(src.readline())
        except:
            solution_exists = False

    if not solution_found and solution_exists:
        print(f'{input_file_path}: Solución no encontrada, pero existe')
        return False

    if solution_found != solution_exists:
        print(f'{input_file_path}: Solución encontrada, pero no existe (???)')
        return False

    if not solution_exists:
        # La solucion no existe, y eso se ha deducido, todo OK
        return True

    if minimum_num_coins < solution_num_coins:
        print(f'{input_file_path}: Se ha encontrado solución con {solution_num_coins}, pero es posible dar el cambio con tan solo {minimum_num_coins}')
        return False

    if sum(solution_coins) != amount:
        print(f'{input_file_path}: La solución dada {solution_coins}, no suma {amount}')
        return False

    if len(solution_coins) != solution_num_coins:
        print(f'{input_file_path}: La solución dada contiene más monedas ({len(solution_coins)})de las indicadas ({solution_num_coins})')
        return False

    return True


def execute_jar_on_input_and_validate(test_number):
    """
    Executes a .jar file on the given input, and verifies the solution is correct
    """
    # Path to the .jar file, assuming it's in the same directory as this script
    jar_path = os.path.join(os.path.dirname(__file__), 'cambio_dinamica.jar')

    # Full path to the .txt file
    input_file_path = os.path.join(os.path.dirname(__file__), 'entradas', f'entrada-{test_number:04d}.txt')
    expected_output_file_path = os.path.join(os.path.dirname(__file__), 'salidas', f'salida-{test_number:04d}.txt')
    actual_output_file_path = os.path.join(os.path.dirname(__file__), f'salida-estudiante-{test_number:04d}.txt')

    command = ['java', '-jar', jar_path, input_file_path, actual_output_file_path]

    # Execute the .jar file with the .txt file as an argument
    subprocess.run(command)

    success = validate(input_file_path, actual_output_file_path, expected_output_file_path)

    pathlib.Path(actual_output_file_path).unlink(missing_ok=True)

    return success

# Example usage
# execute_jar_on_txt_files('/path/to/directory')  # Replace '/path/to/directory' with the actual directory path

numbers = []
pattern = r'entrada-(\d+)\.txt'  # Regex pattern to match 'entrada-NUMBER.txt'
tests_ejecutados = 0
errores = 0

# Iterate over all files in the directory
for filename in os.listdir("entradas"):
    match = re.match(pattern, filename)
    if match:
        # Extract the number from the filename and add it to the list
        test_number = int(match.group(1))
        tests_ejecutados += 1
        if not execute_jar_on_input_and_validate(test_number):
            errores += 1

print(f'Se encontraron errores en {errores} de los {tests_ejecutados} tests ejecutados')


