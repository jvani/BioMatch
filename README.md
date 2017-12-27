<h1 align="center">
BioMatch
</h1>

<p align="center"> 
   <a href="https://github.com/jvani/BioMatch/blob/master/LICENSE"><img src="https://img.shields.io/github/license/jvani/BioMatch.svg"></img></a> <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"> <a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fjvani%2FBioMatch"><img src=https://img.shields.io/twitter/url/https/github.com/jvani/BioMatch.svg?style=social></img></a>
</p>

## Overview
Writing a targetted letter (e.g., Statement of Purpose) is never easy, and finding your audience can be extremely useful. This project uses staff biographies to find individual bios who most closesly resemble a user provided string.

## Example
This code was developed on [https://idss.mit.edu/people/](https://idss.mit.edu/people/). To find similarities with IDSS faculty, run `python biomatch.py` within `BioMatch/biomatch/`. You'll then be prompted to enter your text, and a resulting list of the top 10 most similar staff members will be output. Below is an example using the IDSS mission statement as the input text.

<p align="center">
    <img width="600" src="https://github.com/jvani/BioMatch/blob/master/data/demo.png?raw=true"></img>
</p>

## Project Organization

    ├── README.md
    ├── data
    │   └── idss_bios.json  <- sqlite database.           
    └── biomatch           <- Plotting notebooks.
