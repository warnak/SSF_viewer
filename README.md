# SSF_viewer
A visualization tool for SSF (Shakti Standard Format) interchunk dependency data in Indian Languages


This is a tool that cleans up SSF data according to the requirements by Graphviz, and plots it with the dependency relations on arcs, the chunks in UTF on nodes, and their POS Tags.


Requirements:

- wxconv from https://github.com/ltrc/indic-wx-converter
- graphviz from https://graphviz.gitlab.io/download/
- Interchunk Dependency data in SSF format. (Any number of sentences can be input together).
- Python 3+


Running the tool

- After Installing dependencies as above, and unzipping the folder: `chmod +x ssf_viewer.sh`
- and then to run : `./ssf_viewer.sh <path/to/file>`


Viewing the Graphs

- wait for a few moments and find a folder called `Dependency_Graphs` created in the same directory as the bash file.
- In this directory, find another directory with the name `<input file name>`
- This contains the images in `.svg` format for each of the sentences input with the name `sent_<sentenceID>` and their respective `.dot` files.


Changing settings

- Currently the tool assumes `Hindi` as the input language, `wx` as the input format, and `svg` as output file format, future releases will make these customisable from the terminal.
- To customise it in version 1, you will have to find the respective sections, in the bash code itself.


Notes

- Please ensure that the `preproc.py` file, and the `ssf-viwer.sh` file are in the same directory.


Made by Mukund (https://github.com/warnak) and Aditya (https://github.com/Maverick139)
