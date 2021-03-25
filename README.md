1. REDCap Epic Integration - Data Reformation Script

Background --
- Recent pilot integration to pull data directly from EHR
- The exported file is heavily cluttered with empty cells due to fixed vs. longitudinal/time-dependent data variants

Problem --
- Data from EHR is exported with exorbitant empty cells due to mixing of fixed vs. time-dependent variables
- Solution: Reformat, group by subclass and output data as separate sheets in a master document

Approach --
1. Select CSV
    - Old approach: sys.argv to indicate the file path of CSV (requires switching  windows to 'Finder' and copying/dragging filepath to console)
    - New appproach: tkinter askopenfilename( ) module (allows for direct file selection & auto exit if input format is incompatible, ie. raw vs. labelled data)
2. Parse CSV
    - The script currently reads CSV in labelled data format  ** amend to read raw files as well **
    - Tool: csvreader
3. Identify subclass per row
    - Rename empty subclass for Demographics,  assign CSV column spans associated for each subclass
4. Maintain identifier linkages
    - Identifier column is empty in all rows bar 'Demographic' data, store in dictionary: record number (key): identifier  (value)
5. Group rows by subclass
    - Subclass dictionary, key = subclass, value = empty list
    - Table headers at index 0 of empty list
    - Data appended to list for corresponding key
6. Write new spreadsheet with sheets for each subclass
    - Conversion of data to dataframe w/ Pandas
    - Iteration of Pandas  df.to_excel(sheet_name = subgroup name) ** csv.writerow can cause incorrect number formatting ie. read as date; use df or prepend/append value with "" to lock string **
7. Secure data  
    - Log as timestamped data w/ strftime(datetime.today( ), %y-%m-%d) ** strftime = datetime ⇒ string, strptime = string ⇒ datetime **
    - Save to working directory; *gitignore .xlsm files
