# SleekCompressor

![Platform](https://img.shields.io/badge/platform-Windows-0078D6.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A simple, powerful, and completely offline video compressor for Windows, built with Python and FFmpeg.

![SleekCompressor Demo](https-placeholder-for-your-demo.gif)
*(Replace this with a link to your own demo GIF after uploading)*

## ✨ Features

*   **100% Offline & Private:** Your video files are never uploaded. Compression happens entirely on your machine.
*   **Powerful Compression Engine:** Leverages the industry-standard FFmpeg for high-quality and efficient video compression.
*   **Simple & Intuitive UI:** A clean, modern interface built with CustomTkinter. Drag-and-drop is not implemented, but the file browser is straightforward.
*   **Adjustable Quality:** Easily control the trade-off between file size and video quality with a simple CRF slider.
*   **No Installation Needed (Standalone):** The final executable works on any Windows 10/11 machine without needing to install Python or any dependencies.
*   **Open Source:** The code is clean, commented, and easy to understand.

## 🛠️ How to Build From Source

To build this project yourself, you will need the following prerequisites installed on your system.

### Prerequisites

*   **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
*   **FFmpeg**: You must download the FFmpeg essentials build and have `ffmpeg.exe` available. [Download FFmpeg from Gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
*   **Inno Setup**: The tool used to create the Windows installer. [Download Inno Setup](https://jrsoftware.org/isinfo.php)

### Build Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/SleekCompressor.git
    cd SleekCompressor
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Place `ffmpeg.exe` in the root folder:**
    After downloading and unzipping FFmpeg, copy `ffmpeg.exe` from its `bin` folder into the root of this project directory.

4.  **Build the standalone executable using PyInstaller:**
    This command bundles the Python app and `ffmpeg.exe` into a single, professional `.exe` file.
    ```bash
    pyinstaller --name "SleekCompressor" --onefile --windowed --icon="logo.ico" --add-binary "ffmpeg.exe;." app.py
    ```
    Your final application will be located in the `dist` folder.

5.  **Build the professional installer:**
    Right-click the `installer_script.iss` file and select "Compile". This will use Inno Setup to create a `SleekCompressor_Setup.exe` file in a new `Release` folder.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

*   The incredible [FFmpeg](https://ffmpeg.org/) project.
*   The [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library for making modern GUIs with Python easy.
*   [PyInstaller](https://pyinstaller.org/) for bundling the application.
*   [Inno Setup](https://jrsoftware.org/isinfo.php) for creating the installer.
