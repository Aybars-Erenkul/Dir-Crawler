import requests
import sys
from os.path import join
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal, QObject, QThreadPool, pyqtSlot
from threading import Thread
import time

file_type_dict = {
    '1': 'dir_', 
    '2': 'file_', 
    '3': 'file_php_', 
    '4': '(dir-file) '
    }

word_type_dict = {
    '1': 'all',
    '2': 'common',
    '3': 'crazy',
    '4': 'extra'
    }

global Output
Output = 'jhg'

class MyApp(QMainWindow):

    global file_type
    global word_type
    

    def __init__(self):
        super(MyApp, self).__init__()

        uic.loadUi("window.ui", self)

        #Define Directory Type Buttons
        self.DirsButton.toggled.connect(self.Dirs_Button)
        self.FilesButton.toggled.connect(self.Files_Button)
        self.FilesPhpButton.toggled.connect(self.Php_Button)
        self.DirsAndFilesButton.toggled.connect(self.DirsAndFiles_Button)

        #Define File Type Buttons
        self.AllButton.toggled.connect(self.All_Button)
        self.CommonButton.toggled.connect(self.Common_Button)
        self.RareButton.toggled.connect(self.Rare_Button)
        self.ExtraButton.toggled.connect(self.Extra_Button)

        self.OutputList.append('DENEME')
        self.scanButton = self.findChild(QPushButton, "ScanButton")
        self.scanButton.clicked.connect(self.start_scan)

    
    def Dirs_Button(self):
        global file_type
        file_type = '1'
    def Files_Button(self):
        global file_type
        file_type = '2'
    def Php_Button(self):
        global file_type
        file_type = '3'
    def DirsAndFiles_Button(self):
        global file_type
        file_type = '4'

    #File Functions
    def All_Button(self):
        global word_type
        word_type = '1'
    def Common_Button(self):
        global word_type
        word_type = '2'
    def Rare_Button(self):
        global word_type
        word_type = '3'
    def Extra_Button(self):
        global word_type
        word_type = '4'

    def start_scan(self):
        
        target = self.DomainInput.text()
        if not (target.startswith('http://') or target.startswith('https://')):
            target = 'https://' + target

        if not target.endswith('/'):
            target += '/'   
        construct_path()

        self.scan = Worker(target, file_path)
        self.scan.signal_Output.connect(self.update_output_list)
        self.scan.start()
        

    
    def update_output_list(self, output):
        print (output)
        print("update fonksiyonuna da girdi")
        self.OutputList.append(output)
        

class Worker(QThread):
    signal_Output = pyqtSignal(str)
    signal_end_scan = pyqtSignal(int)

    output = 'Initializing...'
    def __init__(self, target, file_path):
        QThread.__init__(self)
        Worker.target = target
        Worker.file_path = file_path
        Worker.output = Output


    def run(self):
        info = "Thread Calisti"
        print (info)
        self.signal_Output.emit(info)
        count = 0
        save = ''
        try:
            fl = open(Worker.file_path, 'r')
        except:
            print(f'[+] - Failed to open "{Worker.file_path}". Make sure that file exists.\n')
            
        directory_list = fl.read().strip().splitlines()
        fl.close()

        print('[+] - Searching started ...\n')
        
        for an_item in directory_list:
            an_item = an_item.strip()
            if an_item != '':
                def scan_dir():
                    
                    link = Worker.target + an_item
                    response = request(link)
                    if response is None:
                        print('[+] - Error, check if domain is reachable.')
                        Worker.output = '[+] - Error, check if domain is reachable.'
                        self.signal_Output.emit(Worker.output)
                        return
                    elif response:
                        print(f'\n[+] - Got at - {link} - [{response}]')
                        Worker.output = f'\n[+] - Got at - {link} - [{response}]'
                        self.signal_Output.emit(Worker.output)

                        #count += 1
                Thread(target=scan_dir).start()             
                        
        print(f'\n[!] - All done ({count})')
        end = 1
        self.signal_end_scan.emit(end)   
        

        




def construct_path():
    global file_path
    file_path = join('wordlist', file_type_dict[file_type] + word_type_dict[word_type] + '.wordlist')

def request(url):
    try:
        r = requests.get(url)
        time.sleep(0.5)
        if r.status_code == 404:
            return False
        else:
            return r.status_code
    except Exception as e:
        print('\n[!] - OOps. Got error.\n')
        print(e, '\n')
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
