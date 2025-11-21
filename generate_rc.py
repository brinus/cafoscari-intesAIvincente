import subprocess
import os
import glob

def generate_rc():
    qrc_files = glob.glob(os.path.join('resources', '*.qrc'))
    if not qrc_files:
        print("No .qrc files found in the resources directory.")
        return
    for qrc_file in qrc_files:
        base_name = os.path.splitext(os.path.basename(qrc_file))[0]
        output_file = f"rc_{base_name}.py"
        command = [
            "pyside6-rcc",
            qrc_file,
            "-o",
            output_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Generated {output_file} from {qrc_file}")
        else:
            print(f"Error generating {output_file} from {qrc_file}:")
            print(result.stderr)

if __name__ == "__main__":
    generate_rc()