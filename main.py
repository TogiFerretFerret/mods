import os
import subprocess
# its windows lol since pyinstaller is windows only anyways
# Make a folder!
main_cwd= os.getcwd()
if os.path.exists("eighttwolauncher"):
    print("Folder 'eighttwolauncher' already exists -  skipping creation.")
    def start_existing(do_login, username):
        if do_login:
            pass
        else:
            print("Skipping login, starting game without authentication.")
            try:
                pcbin_path = os.path.join(os.getcwd(), "eighttwolauncher", "portacraft", "bin", "portablemc.exe")
                mwd = os.path.join(os.getcwd(), "eighttwolauncher", "portacraft", "dotminecraft")
                subprocess.run([pcbin_path, "--main-dir",mwd,"--work-dir",mwd, "start","quilt:1.20.1","--username", username, "-s", "96.239.55.67"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while starting the game: {e}")
    usern=""
    with open("eighttwolauncher/username.txt", "r") as f:
        usern = f.read().strip()
    start_existing(False, usern)
    exit()
else:
    print("Folder 'eighttwolauncher' does not exist - creating it now.")
def create_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=False)
        print(f"Folder '{folder_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")
create_folder("eighttwolauncher")
os.chdir("eighttwolauncher")
# Grab a working copy of python!
py_link="https://www.python.org/ftp/python/3.13.5/python-3.13.5-embed-amd64.zip"
def download_python(link, folder_name):
    import requests
    import zipfile
    import io

    try:
        response = requests.get(link)
        response.raise_for_status()  # Check for HTTP errors

        # Unzip the content into the specified folder
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(folder_name)
        print(f"Python downloaded and extracted into portable folder.")
    except Exception as e:
        print(f"An error occurred while downloading or extracting Python: {e}")
download_python(py_link, "portapython")
def patch_python():
    os.remove("portapython/python313._pth")
    import requests
    import io
    import subprocess
    link="https://bootstrap.pypa.io/get-pip.py"
    try:
        response = requests.get(link)
        response.raise_for_status()  # Check for HTTP errors

        with open("portapython/get-pip.py", "wb") as file:
            file.write(response.content)
        print("get-pip.py downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading get-pip.py: {e}")
    dname=os.getcwd()
    fts=os.path.join(dname, "portapython", "python.exe")
    ftr=os.path.join(dname, "portapython", "get-pip.py")
    subprocess.run([fts, ftr], check=True)
    return os.path.join(dname, "portapython", "Scripts", "pip.exe")
pip_loc=patch_python()
import subprocess
def install_package(package_name, pip_location, targ):
    try:
        subprocess.run([pip_location, "install", package_name, "--no-warn-script-location","--target",targ], check=True)
        print(f"Package '{package_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing the package: {e}")
create_folder("portacraft")
install_package("portablemc[certifi]", pip_loc,"portacraft")
# get path to portacraft
pc_path = os.path.join(os.getcwd(), "portacraft")
os.chdir(pc_path)
create_folder("dotminecraft")
os.chdir("dotminecraft")
mwd=os.getcwd()
def install_mods():
    import requests
    import zipfile
    import io
    from tqdm import tqdm

    mods_link = "https://github.com/TogiFerretFerret/mods/releases/download/brrr'/mods.zip"
    try:
        # Stream the download to show progress
        with requests.get(mods_link, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 8192
            bytes_io = io.BytesIO()
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading mods") as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        bytes_io.write(chunk)
                        pbar.update(len(chunk))
            print("Finished downloading mods. Extracting...")
            bytes_io.seek(0)
            with zipfile.ZipFile(bytes_io) as z:
                files = z.infolist()
                with tqdm(total=len(files), desc="Extracting mods") as extract_pbar:
                    for file in files:
                        z.extract(file, mwd)
                        extract_pbar.update(1)
                print("Mods downloaded and extracted successfully.")
    except Exception as e:
        print(f"An error occurred while downloading or extracting mods: {e}")

print("Downloading mods...")
install_mods()
os.chdir("..")
os.chdir("..") # path is once again eighttwolauncher?
pcbin_path = os.path.join(pc_path , "bin", "portablemc.exe")
def start_game(do_login,username):
    if do_login:
        pass
    else:
        print("Skipping login, starting game without authentication.")
        try:
            subprocess.run([pcbin_path, "--main-dir",mwd,"--work-dir",mwd, "start","quilt:1.20.1","--username", username, "-s", "96.239.55.67"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while starting the game: {e}")
userv=""
print("YOUR SKIN WILL NOT RENDER. SORRY.")
userv=input("Enter your username/if you don't own the game the one you want: ")
with open(os.path.join(main_cwd, "eighttwolauncher", "username.txt"), "w") as f:
    f.write(userv)
start_game(False, userv)
