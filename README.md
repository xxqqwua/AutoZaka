# AutoZaka

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC-orange)
![Last Commit](https://img.shields.io/github/last-commit/xxqqwua/AutoZaka)

## Overview

AutoZaka is a lightweight automation tool designed to streamline participation in prize drawings on [zaka-zaka.com](https://zaka-zaka.com/). By automating the submission of POST requests using user tokens, AutoZaka saves time and effort for active participants on the website.

## Features

- **Token Management**: Automatically creates and saves a token configuration file (`config.txt`) for future use.
- **POST Request Automation**: Submits POST requests to participate in drawings without manual intervention.
- **Tray Icon with Context Menu**: Offers quick access to exit the program or open the log file through a tray icon.

## Installation

To set up AutoZaka, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AutoZaka.git
   cd AutoZaka
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the program:
   ```bash
   python autozaka.py

## Usage
AutoZaka works as follows:
1. **First Run**:
   * The first time AutoZaka starts up, it checks for the presence of the `config.txt` file. If it is missing, the program prompts you to enter your login and password for zaka-zaka.com.
   * Using your login and password, the program will log in once to your profile and save the token cookie in `config.txt` for future use.
2. **Subsequent Runs**:
   * For future runs, the program automatically reads the saved token and sends the necessary POST requests to participate in drawings without requiring further input.
3. **Exiting the Program:**
   * A tray icon will appear, allowing you to access the following options:
     * **Exit:** Closes the program.
     * **Open Log File:** Opens the log file for review.

## Contribution Guidelines
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.
Please ensure your code adheres to the existing style and includes tests for any new functionality.

## Future Plans
* **Multitasking**: Implement multitasking functionality to allow the program to process multiple tokens simultaneously, increasing efficiency for users with multiple accounts.

## Credits
The program uses a script to solve captcha from [obaskly](https://github.com/obaskly/RecaptchaBypass).

## License
This project is licensed under the Creative Commons BY-NC (Attribution-NonCommercial) License. You are free to share and adapt the material, but it cannot be used for commercial purposes. For more details, visit [Creative Commons BY-NC](https://creativecommons.org/licenses/by-nc/4.0/).
