import os
import subprocess

# ANSI color codes for colored output
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def is_dirsearch_installed():
    """
    Check if dirsearch is installed.
    """
    try:
        subprocess.run(['dirsearch', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_dirsearch():
    """
    Install dirsearch using pip.
    """
    try:
        subprocess.run(['pip', 'install', 'dirsearch'], check=True)
        print(colors.GREEN + "dirsearch installed successfully." + colors.ENDC)
    except subprocess.CalledProcessError as e:
        print(colors.FAIL + f"Error installing dirsearch: {e}" + colors.ENDC)

def get_wordlists_from_directory(directory):
    """
    Get a list of wordlist files from the specified directory.
    """
    wordlists = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            wordlists.append(os.path.join(directory, filename))
    return wordlists

def run_dirsearch(url, wordlists, skip_indexes, custom_options):
    """
    Run dirsearch with the provided URL and wordlists, skipping specified indexes.
    """
    for idx, wordlist in enumerate(wordlists, start=1):
        if idx not in skip_indexes:
            command = f"dirsearch -u {url} -w {wordlist} {custom_options}"
            print(colors.BLUE + f"Running dirsearch with Wordlist {idx}:" + colors.ENDC)
            print(colors.HEADER + command + colors.ENDC)
            try:
                subprocess.run(command, shell=True, check=True)
                print(colors.GREEN + f"Dirsearch with Wordlist {idx} completed successfully." + colors.ENDC)
            except subprocess.CalledProcessError as e:
                print(colors.FAIL + f"Error running dirsearch with Wordlist {idx}: {e}" + colors.ENDC)

def main():
    # Print cool banner
    print(colors.HEADER + """

  __  __       _ _   _ _____  _      
 |  \/  |     | | | (_)  __ \(_)     
 | \  / |_   _| | |_ _| |  | |_ _ __ 
 | |\/| | | | | | __| | |  | | | '__|
 | |  | | |_| | | |_| | |__| | | |   
 |_|  |_|\__,_|_|\__|_|_____/|_|_|   
                                     
                                     
          
""" + colors.ENDC)

    # Check if dirsearch is installed and install if not
    if not is_dirsearch_installed():
        print(colors.WARNING + "dirsearch is not installed. Installing..." + colors.ENDC)
        install_dirsearch()

    # Ask for the URL
    url = input(colors.BLUE + "Enter the URL: " + colors.ENDC)

    # Ask for the path to the directory containing wordlist files
    directory = input(colors.BLUE + "Enter the path to the directory containing wordlist files: " + colors.ENDC)

    # Get list of wordlist files from the directory
    wordlists = get_wordlists_from_directory(directory)

    # Display wordlists found in the directory
    print(colors.BLUE + "Wordlists found in the directory:" + colors.ENDC)
    for idx, wordlist in enumerate(wordlists, start=1):
        print(f"{idx}. {wordlist}")

    # Ask user to skip any specific wordlists
    skip_wordlists_input = input(colors.BLUE + "Enter the indexes of wordlists to skip (comma-separated, or leave blank): " + colors.ENDC)
    skip_indexes = [int(index.strip()) for index in skip_wordlists_input.split(',') if index.strip()]

    # Ask user for custom options
    custom_options = input(colors.BLUE + "Enter custom options for dirsearch (leave blank for default): " + colors.ENDC)

    # Run dirsearch with each wordlist, skipping specified indexes
    run_dirsearch(url, wordlists, skip_indexes, custom_options)

if __name__ == "__main__":
    main()
