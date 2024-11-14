# MyCase-Ledes-Fixer

A utility for fixing timekeeper names in the LEDES files output by MyCase from Firstname Middle Initial Lastname to Lastname, Firstname Middle Initial.

## Installation

1. Download the latest `MyCase-Ledes-Fixer_Setup.exe` from the [releases](release).
2. Run the installer and follow the prompts.
3. The application will be installed and available from the Start Menu.

### Building from Source

1. **Clone the repository:**

   ```bash
   git clone https://github.com/halfprice06/mycase_ledes_fixer.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd mycase_ledes_fixer
   ```

3. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Install Inno Setup Compiler:**

   Download and install the [Inno Setup Compiler](https://jrsoftware.org/isinfo.php), which is required to build the installer.

5. **Build the executable and installer:**

   ```bash
   python build_release.py
   ```

6. **Windows Installer:**

The Windows installer will be in release folder. 

## Usage

1. Launch "MyCase LEDES Fixer" from the Start Menu
2. Drag and drop LEDES files or use the "Add Files" button
3. Choose whether to overwrite original files
4. Click "Process Files" to transform the timekeeper names

## Support

For support, please create an issue in the GitHub repository or contact the developer. 