# cmap

## Introduction
This repository contains the cmap proof-of-concept source code, sample configuration 
file, and sample CMAP export data file. It was created as part of the CDISC 360
work to demonstrate a way to process the Biomedical Concept CMAPs, validate them,
and create machine-readable Biomedical Concepts from them.

## Getting Started
cxl-load.py is the main program file. It reads in CMAP content created by the CDISC
360 project, generates
* an directed acyclic graph
* a graphML representation of the graph to support visualizations
* a report in Excel document the contents of the graph and highlighting problems
* a JSON-based biomedical concept to be used by programs processing them

This application implements an object-oriented design and a number of supporting classes
combine to comprise the overall application. This program uses a command-line interface.

## Examples
* python cxl_load.py -f HbA1C-Berlin-2020-01-22.cxl -c "Hemoglobin A1C to Hemoglobin Ratio Measurement (C111207)"
* python cxl_load.py -f VS-SYSBP-Metamodel3.cxl -c "Systolic Blood Pressure (C0005823)"
