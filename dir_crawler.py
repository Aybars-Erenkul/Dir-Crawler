import requests
from os.path import join
from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6 import QtWidgets
#from PyQt6.QtWidgets import *
import sys

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

class MyApp(QtWidgets.QMainWindow):
    global file_type
    global word_type

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('window.ui', self)
        
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

        self.ScanButton.clicked.connect(self.start_scan)

        
    #Directory functions
    def Dirs_Button(self):
        global file_type
        file_type = '1'
    def Files_Button(self):
        global file_type
        file_type = 2
    def Php_Button(self):
        global file_type
        file_type = 3
    def DirsAndFiles_Button(self):
        global file_type
        file_type = 4

    #File Functions
    def All_Button(self):
        global word_type
        word_type = 1
    def Common_Button(self):
        global word_type
        word_type = '2'
    def Rare_Button(self):
        global word_type
        word_type = 3
    def Extra_Button(self):
        global word_type
        word_type = 4

    

    #Starting the scan
    def start_scan(self):
        target = self.DomainInput.text()
        if not (target.startswith('http://') or target.startswith('https://')):
            target = 'https://' + target

        if not target.endswith('/'):
            target += '/'        
        construct_path()
        while True:
            count = 0
            save = ''    
            try:
                fl = open(file_path, 'r')
            except:
                print(f'[+] - Failed to open "{file_path}". Make sure that file exists.\n')
                continue
            directory_list = fl.read().strip().splitlines()
            fl.close()

            print('[+] - Searching started ...\n')

            for an_item in directory_list:
                an_item = an_item.strip()
                if an_item != '':
                    link = target + an_item
                    response = request(link)
                    if response is None:
                        print('[+] - Error, check if domain is reachable.')
                        break
                    elif response:
                        print(f'\n[+] - Got at - {link} - [{response}]')
                        output = 'Denemee'
                        self.OutputList.clear()
                        self.update_output_list(output)

                        count += 1
                        
            print(f'\n[!] - All done ({count})')   

    def update_output_list(self, output):
        self.OutputList.append(output)
        output_list = self.OutputList.toPlainText()
        output_list = output_list.split()
        self.OutputList.setPlainText("\n". join(output_list))         
        
def construct_path():
    global file_path
    file_path = join('wordlist', file_type_dict[file_type] + word_type_dict[word_type] + '.wordlist')

def get_ans(qs):
    while True:
        ans = input(qs)
        if ans.lower() == 'y':
            return True
        elif ans.lower() == 'n':
            return False

def request(url):
    try:
        r = requests.get(url)
        if r.status_code == 404:
            return False
        else:
            return r.status_code
    except Exception as e:
        print('\n[!] - OOps. Got error.\n')
        print(e, '\n')
        return None

    

app = QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
app.exec()





if __name__ == '__main__':

    while True:
        count = 0
        save = ''

        print('\n[+] - Enter Target link')
        target = input('[?] --> ')

        if target == '':
            continue

        if not (target.startswith('http://') or target.startswith('https://')):
            target = 'https://' + target

        if not target.endswith('/'):
            target += '/'
        
        print('\n---> Using built-in dictionaries ')
        while True:
            print('\n--> Choose dictionary type? ')
            print('  1. Directory')
            print('  2. Files')
            print('  3. Files (PHP)')
            print('  4. Directory & Files')
            ans = input('[>] ')
            if ans in ['1', '2', '3', '4']:
                file_type = ans
                break
            print('--->Invalid option')
        while True:
            print('\n--> Choose words type? ')
            print('  1. All')
            print('  2. Common')
            print('  3. Crazy')
            print('  4. Extra')
            ans = input('[>] ')
            if ans in ['1', '2', '3', '4']:
                word_type = ans
                break
        file_path = join('wordlist', file_type_dict[file_type] + word_type_dict[word_type] + '.wordlist')
            
        try:
            fl = open(file_path, 'r')
        except:
            print(f'[+] - Failed to open "{file_path}". Make sure that file exists.\n')
            continue
        directory_list = fl.read().strip().splitlines()
        fl.close()

        print('[+] - Searching started ...\n')

        for an_item in directory_list:
            an_item = an_item.strip()
            if an_item != '':
                link = target + an_item
                response = request(link)
                if response is None:
                    print('[+] - Error, check if domain is reachable.')
                    break
                elif response:
                    print(f'\n[+] - Got at - {link} - [{response}]')
                    count += 1
                    
        print(f'\n[!] - All done ({count})')

        if not get_ans('\n[?] - Wanna try again? '):
            exit(0)

