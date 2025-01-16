# Black Ops 6 Data Table Extractor

This is a script that will strip the Black Ops 6 Data Table from the html file Activision provides when you request your personal data.  I requested my information after watching TheXclusiveAce youtube video here:  https://www.youtube.com/watch?v=dZ6Zw8tADVo&t=25s and found that two weeks later Activision sends a large html file containing all game data from the past few years.

I wrote a quick script to extract the tables - figuring other people might be having problems getting their data I figured I'd clean it up and put it out there.

It is a simple command line script that will open all html files in the current working directory, extract only the Black Ops 6 game data, create a unique file name and save out to a csv file.  Separate csv files will be created for each extractable html file in the source directory.

No user identifiable data is saved to the csv or otherwise transmitted.

## Installation and Usage

### From Source:

Get the bo6_extract.py and requirements.txt into your preferred directory.

Create your venv or use whatever environment and pip install -r requirements.txt.

Once dependencies are installed, copy the html file provided by Activision to the same directory as the bo6_extract.py file.

From this directory, run "python3 bo6_extract.py" and the script will parse the html file and create the resultant csv in the same directory.


### Windows:

In /dist/windows/ you will find bo6_extract.exe.

Copy this exe file to the directory containing your Activision provided html file.

From the command prompt, navigate to this directory and run "bo6_extract.exe"


### Mac OS:

In /dist/macos/ you will find bo6_extract.

Copy this file to the directory containing your Activision provided html file.

From the command line, navigate to this directory and run "./b06_extract"


### Command Line Options:

By default the script looks for the html file in the current working directory, but optionally, from the command line you can specify:

    -s, --source    to specify the directory containing the source html file from activision
    -o, --output    to specify the directory you with the resultant csv file to be written

The script will repeat for all html files in the source directory and save all resultant csv files to the output directory.
