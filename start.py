import subprocess

def install_dependencies():
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing dependencies: {e}")

def run_main():
    try:
        subprocess.run(["python", "main.py"])
    except FileNotFoundError:
        print("Error: main.py file not found.")
    except Exception as e:
        print(f"An error occurred while running main.py: {e}")

if __name__ == "__main__":
    print("Installing dependencies...")
    install_dependencies()
    print("\nRunning main.py...")
    run_main()
