import os
import shutil

os.system('pyinstaller dseGeneratorApp.py --name DSEGenerator -w --add-data="./gfx/header.png;gfx" --hidden-import=logger.py --noconfirm')
 
shutil.copytree('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/templates', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/templates')
shutil.copytree('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/output', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/output')
shutil.copytree('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/log', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/log')
shutil.copytree('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/test', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/test')
shutil.copytree('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/data', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/data')
shutil.copy('M:/Dev/Projects/worddsegenerator/wordDSEGenerator/README.pdf', 'M:/Dev/Projects/worddsegenerator/wordDSEGenerator/dist/DSEGenerator/README.pdf')
