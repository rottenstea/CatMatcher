
<img src="Logo_small.jpeg" alt="Logo" width="150" align="" style="margin-bottom: -30px;" />

# CatMatcher 
A Python wrapper for the advanced table crossmatching features of STILTS, offering more flexibility than the Topcat frontend 
and simplifying the process of using STILTS via the command line without the need for complex shell scripts. 

## Requirements
- The package should provide a fast and intuitive way for python users to access the full functionality
of the **S**tarlink **T**ables **I**nfrastructure **L**ibrary **T**ool **S**et, short STILTS, cross-matching functionalities.
Said functionalities are more extensive than what is currently offered by the Topcat GUI, especially concerning the handling
of multiple tables at once. 
- The tool should eliminate the need of writing shell scripts and running them in the command line,
instead offering access to the STILTS crossmatch functions by providing python wrappers for the source code. 
- The python package should automatically create the
required shell scripts, taking into account a number of user-specified parameters (e.g., match radius, match type, dropped columns,
column pre- or suffixes, etc.) to get the desired output.
- The package should allow matches between an arbitrary number of tables, and also incorporate the specific pairmatch functions of STILTS.
- The package should be able to work with various common input formats, such as `.fits` and `.csv`at minimum, which may be provided
locally, or accessed via query services like TAP or astroquery.
- All functions and classes should be documented using common documentation software, e.g., Sphinx and be covered by test functions.

### Expected dependencies
- topcat/STILTS software needs to be installed and accessible via the terminal.
- Classic python packages such as: numpy, astropy

### ![Green Badge](https://img.shields.io/badge/NEW-green) Install instructions for STILTS

1. Download and install the package:
   - On MacOS with ``homebrew``: "brew install --cask topcat --no-quarantine" (topcat + STILTS installation)
   - Via the ``stilts.jar`` file from the webpage: https://www.star.bris.ac.uk/~mbt/stilts/
   
2. **Important:** Within the CatMatcher package, STILTS is executed using the `zsh` native to MacOS environments.\
To see if that works on your machine, try typing the command `stilts` into the `zsh` terminal\
(within the virtual environment of CatMatcher, if it was not installed globally).
It should open the software in the terminal and give a basic overview of its parameters.
3. Depending on system architecture, the STILTS-path may need to be added to the `~\.zshrc` source file.\
It will look similar to the example below,
depending on where exactly the STILTS (or topcat) source directory is located:
   - `export PATH="/Applications/TOPCAT.app/Contents/Resources/app:$PATH"`



## User Stories

### Main functionality
1. **Simultaneous crossmatch of _n_ catalogs**\
Alena has 8 different .csv files with stellar coordinates measured on different observation dates. She now needs to
perform a cross-match between all the catalogs to establish a time-domain for each measured source. However, the
Topcat GUI only allows for a simultaneous matching of 4 tables at the same time, which leads to different match results
depending on the specific catalog combinations and match order. Luckily, the STILTS backend is not as
limited. So Alena uses the python wrapper for the STILTS `tmatchn` function to crossmatch all her catalogs at the same time.

 
2. **Crossmatch of a local table with the Gaia DR3 catalog**\
Max has a dataset containing stellar positions in the ICRS frame which he would like to augment with photometric data from
the Gaia DR3 survey for further study. To this end, he uses the `TAPmatch` function, which takes the local table as input,
queries the Gaia database for all sources in the user-specified coordinate range, and returns a cross-match table between the
local table and the online database.



### Extended functionality (Edge cases)

- Alena has performed many cross-matches of different catalogs for her work during the last months. Now she has
to write her results down for publication, but she cannot remember which value she selected for the match radius
_r_. So she provides her catalogs as input to the `tmatchn` function and tries out different plausible values
for _r_. Afterwards, she compares the number of matches she got for each values to the number of matches in her
original catalog and can deduce the right value.


- Peter has a number of tables, some of which are in .fits format while others are in .csv format, which he would like to
cross-match. Before the `tmatchn` routine is employed, the tables need to be brought into the same format. So the script employs
a function that accepts different input formats and transforms them into pd.Dataframes before handing them over to
the matching function.


## Development plan
The focus (= core functionality) of the package is the STILTS function `tmatchn`, which allows the simultaneous cross-matching of
_n_ catalogs based on various user specifications. 

The core functionality will be expanded to other functionalities, e.g., `tmatch2` (cross-matching of two catalogs) or the possibility to cross-match a local table with an online table
using `astroquery`. However, the latter functions are already possible via the Topcat GUI and as such present less
pressing matters. The key advantage of incorporating them into the package will be the `log`-option, which stores 
important crossmatch parameters, such as the matching radius or criteria, in a dedicated log-file.


<p align="center">
  <sub> Logo &copy; 2025 rottenstea. All rights reserved.</sub>
</p>