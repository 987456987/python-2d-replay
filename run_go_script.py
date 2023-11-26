import subprocess
import sys

def run_go_script(demo_path):
    try:
        # Run the Go script with the demo file path as an argument
        subprocess.run(["go", "run", "parser.go", demo_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the Go script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a command-line argument (demo file path) is provided
    if len(sys.argv) != 2:
        print("Usage: python run_go_script.py <path_to_demo_file>")
        sys.exit(1)

    # Get the demo file path from the command-line argument
    demo_path = sys.argv[1]

    # Run the Go script with the provided demo file path
    run_go_script(demo_path)