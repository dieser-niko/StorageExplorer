# StorageExplorer
This script can show the sizes for a selected folder (includes subfolders)

It was created due to Windows limitations, as it cannot display the memory of folders due to performance issues.

## How to use

The only requirement is python, there are no additional packages for default installation.

Also tested with [PyPy](https://pypy.org) since the scanning process takes some time.

### Please note:
The script takes some time for bigger folders. Even if it looks like it's crashing, just wait.

For the GUI version there's no window update since this is also resource consuming and it's not really possible to 
show anything on the window while scanning. A progress bar would be pointless since the amount of files might differ.

### main.py
Example syntax:
`python3 main.py --path C:\ -o`

Argument | Description | Default
--- | --- | ---
-p/--path | Path to the folder whose subfolders will be scanned. | ./
-o/--output | if given, the raw data will be printed | False

### gui.py
Example syntax:
`python3 gui.py --path C:\`

Argument | Description | Default
--- | --- | ---
-p/--path | Path to the folder whose subfolders will be scanned | File selector

When opening, the filemanager will appear if the argument wasn't used.

After the scan is completed, a list appears which shows the size (currently only in bytes)

You also can navigate through the folders
