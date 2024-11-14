# MyCase-Ledes-Fixer

A utility for transforming timekeeper names in LEDES files.

## Installation

1. Download the latest `MyCase-Ledes-Fixer_Setup.exe` from the [releases](link-to-releases).
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

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Build the executable and installer:**

   ```bash
   python build_release.py
   ```

5. **Locate the build outputs:**
   - The executable will be in the `dist` folder.
   - The Windows installer will be in the `installer` folder.
   - A packaged release version will be available in the `release` folder.

## Usage

1. Launch "MyCase LEDES Fixer" from the Start Menu
2. Drag and drop LEDES files or use the "Add Files" button
3. Choose whether to overwrite original files
4. Click "Process Files" to transform the timekeeper names

## Support

For support, please create an issue in the GitHub repository or contact the developer. 