import os

# Function to list all Python scripts in a directory
def list_python_scripts(folder):
    scripts = []
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            scripts.append(filename)
    return scripts

# Function to execute scripts in a specific order
def execute_scripts(folder, script_order):
    for script_name in script_order:
        script_path = os.path.join(folder, script_name)
        if os.path.exists(script_path):
            print(f"Executing {script_name}...")
            os.system(f"python {script_path}")
        else:
            print(f"Script '{script_name}' not found in folder.")

# Main function
def main():
    folder = './scripts'  # Specify your folder containing the scripts
    scripts = list_python_scripts(folder)

    if not scripts:
        print(f"No Python scripts found in '{folder}'.")
        return

    print("Available scripts:")
    for idx, script in enumerate(scripts, start=1):
        print(f"{idx}. {script}")

    try:
        order = input("Enter the order of scripts to execute (e.g., '1 3 2'): ").strip()
        script_order = [scripts[int(idx) - 1] for idx in order.split()]
        execute_scripts(folder, script_order)
    except IndexError as e:
        print(f"Invalid script index: {e}")
    except ValueError as e:
        print(f"Invalid input format: {e}")

if __name__ == "__main__":
    main()
