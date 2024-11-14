import os
import shutil
import subprocess
import sys
import glob

def clean_directories():
    """Clean build, dist and installer directories"""
    dirs_to_clean = ['build', 'dist', 'installer']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name} directory")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable with PyInstaller...")
    result = subprocess.run(['python', '-m', 'PyInstaller', 'mycase_ledes_fixer.spec'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("Error building executable:")
        print(result.stderr)
        sys.exit(1)
    print("Successfully built executable")

def prepare_dist_files():
    """Prepare distribution files by creating proper directory structure"""
    dist_path = os.path.join(os.getcwd(), 'dist')
    if not os.path.exists(dist_path):
        print("Error: dist directory not found")
        sys.exit(1)

    # Create the proper directory structure
    app_dir = os.path.join(dist_path, 'MyCase-Ledes-Fixer')
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)

    # Move all files from dist to the new directory
    for item in os.listdir(dist_path):
        if item != 'MyCase-Ledes-Fixer':  # Skip the directory we just created
            src = os.path.join(dist_path, item)
            dst = os.path.join(app_dir, item)
            if os.path.isfile(src):
                shutil.move(src, dst)
                print(f"Moved {item} to proper directory")

def build_installer():
    """Build the installer using Inno Setup"""
    print("Building installer with Inno Setup...")
    # Path to Inno Setup Compiler (adjust if needed)
    iscc_path = r'"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"'
    
    # Create installer directory if it doesn't exist
    os.makedirs('installer', exist_ok=True)
    
    # Run Inno Setup
    result = subprocess.run(f'{iscc_path} installer.iss', 
                          capture_output=True, text=True, shell=True)
    
    if result.returncode != 0:
        print("Error building installer:")
        print(result.stderr)
        print(result.stdout)
        sys.exit(1)
    print("Successfully built installer")

def create_release_package():
    """Create a release package with the installer and any additional files"""
    release_dir = 'release'
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy installer to release directory
    installer_file = 'installer/MyCase-Ledes-Fixer_Setup.exe'
    if os.path.exists(installer_file):
        shutil.copy2(installer_file, release_dir)
        print(f"Copied installer to {release_dir}")
    else:
        print("Error: Installer not found")
        sys.exit(1)

def main():
    print("Starting build process...")
    clean_directories()
    build_executable()
    prepare_dist_files()
    build_installer()
    create_release_package()
    print("\nBuild process completed!")
    print("Release package created in the 'release' directory")

if __name__ == '__main__':
    main() 