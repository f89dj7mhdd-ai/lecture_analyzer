import subprocess

def run_command(command):

    print("実行:", " ".join(command))

    subprocess.run(command, check=True)