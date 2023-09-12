"""
Main script for command line interface. The script can execute various FrontEnd scripts
in an easy way.
"""

import subprocess
import os

class CommandLineInterface:
    """
    A command-line interface for executing FrontEnd scripts.

    Attributes:
        paths (list): List of paths to folders containing scripts and requirements.txt.
    """

    def __init__(self, input_paths):
        """
        Initialize the CommandLineInterface.

        Args:
            input_paths (list): List of paths to folders.
        """
        self.paths = input_paths

    @staticmethod
    def install_requirements(requirements_file):
        """
        Install required Python packages from a requirements.txt file.

        Args:
            requirements_file (str): The path to the requirements.txt file.
        """
        try:
            subprocess.run(["pip", "install", "-r", requirements_file], check=True)
        except subprocess.CalledProcessError as install_error:
            print(f"Error installing requirements: {install_error}")

    def execute_script(self, script_path):
        """
        Execute a Python script.

        Args:
            script_path (str): The path to the script to be executed.
        """
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as execute_error:
            print(f"Error executing {script_path}: {execute_error}")

    def run(self):
        """
        Run the CommandLineInterface program.
        """
        print("Executing program!")

        for path in self.paths:
            # Install required packages from requirements.txt
            requirements_file = os.path.join(path, "requirements.txt")
            if os.path.exists(requirements_file):
                self.install_requirements(requirements_file)

            while True:
                print("\nChoose an option:")
                print("1. Execute App 1")
                print("5. Exit")

                choice = input("Enter your choice: ")

                if choice == "1":
                    script_to_execute = os.path.join(path, "front_end.py")
                    self.execute_script(script_path=script_to_execute)
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    paths = [
        "/Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/FrontEnd",
        # Add more paths here as needed
    ]
    cli = CommandLineInterface(input_paths=paths)
    cli.run()
