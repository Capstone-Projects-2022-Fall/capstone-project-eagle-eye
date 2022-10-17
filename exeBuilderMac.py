import os 
import subprocess
# this is to fix a macOS issue where it doesnt see torch libraries, needs to be run after making a dist
print(os.getcwd())
run = subprocess.run(['pyinstaller', '--noconfirm', 'MACgui.spec'])
os.chdir("dist/gui")
print(os.getcwd())
run = subprocess.run(['rm', 'libtorch_cpu.dylib'])
run = subprocess.run(['rm', 'libc10.dylib'])
run = subprocess.run(['rm', 'libtorch.dylib'])
run = subprocess.run(['rm', 'libtorch_python.dylib'])
run = subprocess.run(['ln', '-s', '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/dist/gui/torch/lib/libtorch_cpu.dylib'])
run = subprocess.run(['ln', '-s', '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/dist/gui/torch/lib/libc10.dylib'])
run = subprocess.run(['ln', '-s', '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/dist/gui/torch/lib/libtorch.dylib'])
run = subprocess.run(['ln', '-s', '/Users/tyler/Documents/GitHub/capstone-project-eagle-eye/dist/gui/torch/lib/libtorch_python.dylib'])
print('COMPLETE')
