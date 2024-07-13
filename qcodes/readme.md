# Files:

## scan code test.ipynb 

Example notebook.

## qc_measure.py

A package for general 1d and 2d scans using qcodes. A 1d scan is a special 2d scan.

- A measurment log (DOCX file) and DAT data are auto generated aside to the qcodes db file, making your data and log available to more researchers who are not familiar with database stuffs.

- Integrated with qtplot for real time visualization (see snapshots below). For versions since 20240711.

- Values from multiple instruments can be fetched in a parallel way (use threads). For versions since 20240712.

## qc_fast1d.py

A package for fast 1d and 2d scans using triggers between a Qdevil DAC and an Keysight DMM. Fast because trigger and instrument buffer are used.  

# Instructions:

Use Python 3.11 or higher. Time.sleep() may wait tens of milliseconds longer in lower Python versions.

Change "lineterminator" to line_terminator in qc_measure.py if old pandas versions are installed. This parameter name changed.


# Snapshots:

Scan code (1d scan is a special kind of 2d scan, complicated measurements are availble by complicated "Parameters"):


![a](https://github.com/cover-me/repository/assets/22870592/0f2b6c36-21f9-4fc2-8a91-9f369de70fb6)


Measurement log

![image](https://github.com/cover-me/repository/assets/22870592/95bccb56-bf16-4c42-99a8-5112d6e33315)

Data files

![image](https://github.com/cover-me/repository/assets/22870592/befd7f58-30ca-405b-9be0-ba51bb51744f)


Schematic diagram for fast scans


![image](https://github.com/cover-me/repository/assets/22870592/7ab6313f-b254-418e-bd84-1b15bb4d6dae)


# Notes for qcodes

(1) Under the "User Folder", create a new "Data Folder" to store the files during a cooldown/experiment. The "Data Folder" will include ipynb codes, db and dat data files, docx measurement logs, and pptx summaries. Copy the address of the "Data Folder" in the address bar, as it will be used in (3).

- The "User Folder" is typically located at X:\UserData\[UserName], where X could be drive C or another drive. For convenience, it is recommended to use the last system drive for the "User Folder".

- A suggested name for the "Data Folder" is: [cooldown information] [sample information] [UserName], e.g., 20240707-233PPMS 20221222-InAs2DEGJJ15 XXX.

- The pptx document is for discussion during the experiment. Name it with a prefix the same as the db file name (see step 5), and add a suffix (if multiple ppt files are needed) as appropriate.

- The docx document: If you use the qc_measure.py script mentioned in (5), the measurement code will automatically create this document; otherwise, you can ignore this part of instruction. The file name will be the same as the db file name. This document is used for semi-automatic experimental logging and further analysis/discussion when the ppt file cannot provide sufficient details. When opening the docx file, select the "web view" in the bottom right corner. The measurement code will automatically generate records to this document. You can conveniently insert figures into this document using qtplot (click "copy" and then ctrl+v to paste, or directly click "to Word", similar to inserting figures into ppt).

(2) Start -> Search and open the Anaconda Powershell Prompt.

- If the "Data Folder" is not on drive C, but on drive X, run "X:" to switch the directory to drive X.

- If the "Data Folder" is on drive C, you may need to open the prompt with administrator privileges, otherwise jupyter lab may not have permission to save data in C:\UserData (depending on the operating system settings).

(3) Run "cd PATH", where PATH is the path of the "Data Folder" copied in (1).

(4) Run "jupyter lab" to open jupyter lab in the "Data Folder".

- In jupyter lab, you can use absolute paths (starting from the drive letter, X:\a\b\c), or relative paths relative to the ipynb file (without the drive letter, a\b\c, .\a\b\c, ..\a\b\c, ....\a\b\c, etc. .\means the current directory, can be omitted; ..\means the parent directory, ..\..\means the grandparent directory). It is recommended to use relative paths, so that the paths still work even if the entire folder is copied to another location, without the need to modify the code.

(5) Measurement. Copy the measurement code into the "Data Folder". If you don't have your own measurement code, you can download the latest qc_measure.py and the corresponding example scan_code_test.ipynb ([link](https://github.com/cover-me/repository/tree/master/qcodes)) to the "Data Folder".

- [cooldown information] [sample information] [UserName] is also a good name for qcodes' db file, which contains measurement data and station snapshots.

- If using qc_measure.py, manually open qtplot for real-time data visualization.
