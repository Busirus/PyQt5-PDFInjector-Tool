<div id="header" align="center">
<h1> PyQt5 PDF Injector V1.0</h1>
</div>



<div id="header" align="center">
  <img src="https://image.noelshack.com/fichiers/2023/12/3/1679476504-gui.png">
</div>

# DISCLAIMER: 

This tool is for educational purposes only. Do not use it for any illegal activities. The author is not responsible for any misuse of this tool.

# Introduction

This Python app allows users to inject malicious payloads into PDF files through a GUI. It supports three injection methods: URL, file, and JavaScript. Users select the input and output PDF files, choose a payload, and the app creates a new PDF with the payload injected. Pre-defined JavaScript payloads are also available. 

# Installation

1. Clone the repository or download the zip file.

```bash
git clone https://github.com/busirus/PyQt5-PDF-Injector.git
```

2. Make sure that Python 3.x is installed.

3. Install the required libraries by running the following command in the terminal:

```bash
pip install -r requirements.txt
```

4. Run the program by executing the following command:

```bash
python main.py 
```

# Usage

1. Run the application by running python main.py
2. Select the input PDF file, the output PDF file, and the injection method (URL, file, or JavaScript)
3. If using the URL injection method, enter the malicious URL in the provided field
4. If using the file injection method, select the file to be injected in the provided field
5. If using the JavaScript injection method, enter the JavaScript code or file path in the provided field
6. Click the "Inject" button to create the new PDF file with the payload injected

# Pre-defined Payloads

The application includes pre-defined JavaScript payloads that can be added by clicking the "Add Payload" button. These payloads include:

Alert Box: Displays an alert box with a message when the PDF is opened.

Denial of Service (DoS): Creates an infinite loop of alert boxes, causing a denial of service attack.

Print Dialog: Opens the print dialog when the PDF is opened.

Open Website: Opens a specified website when the PDF is opened.

Download File: Downloads a specified file when the PDF is opened.

Remote Code Execution (RCE): Executes a specified command on the user's machine and sends the output to a remote server.

Reverse Shell: Opens a reverse shell on the user's machine and sends the output to a remote server.

Remote Access: Sends a specified command to a remote server and receives the output.

Keylogger: Records keystrokes and sends them to a remote server.

Execute Remote JavaScript: Executes a remote JavaScript file.

Clipboard Data Exfiltration: Reads clipboard data and sends it to a remote server.

Webcam Access: Accesses the user's webcam and displays the video.

Screen Capture: Captures the user's screen and sends the screenshot to a remote server.

Get Geolocation: Retrieves the user's geolocation and sends it to a remote server.

List Stored Cookies: Retrieves and sends a list of stored cookies to a remote server.

List Stored Credentials: Retrieves and displays a list of stored credentials.

Get Stored Credentials: Retrieves and displays stored credentials.

Get Browser History: Retrieves and displays the user's browser history.

Get Wifi Passwords: Retrieves and displays the user's saved Wi-Fi passwords.

Play Sound: Plays a specified sound when the PDF is opened.




# License

This project is licensed under the MIT License 
