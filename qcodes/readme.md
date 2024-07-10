# Files:

## scan code test.ipynb 

Example code.

## qc_measure.py

A package for general 1d and 2d scans using qcodes. A measurment log (DOCX file) and DAT data are generated aside to the qcodes db file, making your data and log available to more researchers. 

## qc_fast1d.py

A package for fast 1d and 2d scans using triggers between a Qdevil DAC and an Keysight DMM. Fast because trigger and instrument buffer are used.  

# Instructions:

Use Python 3.11 or higher. Time.sleep() may wait tens of milliseconds longer in lower Python versions.

Change "lineterminator" to line_terminator in qc_measure.py if old pandas versions are installed. This parameter name changed.

# Snapshots:

Scan code (1d scan is a special kind of 2d scan, complicated measurements are availble by complicated "Parameters"):

![image](https://github.com/cover-me/repository/assets/22870592/92a26e2a-ef71-4ce6-bd96-8d94a572e546)

Measurement log

![image](https://github.com/cover-me/repository/assets/22870592/95bccb56-bf16-4c42-99a8-5112d6e33315)

Data files

![image](https://github.com/cover-me/repository/assets/22870592/befd7f58-30ca-405b-9be0-ba51bb51744f)


Schematic diagram for fast scans


![image](https://github.com/cover-me/repository/assets/22870592/7ab6313f-b254-418e-bd84-1b15bb4d6dae)
