# bdl
Business Data Language (BDL) - An open-source language for business data analysis

BDL is a simple data analysis language for non-programmers.

## Install
Download `BDL-Setup.exe` from Releases.

## Usage
```bash
bdl
bdl run file.bdl
bdl --version

## Example
load "sales.csv" as s
filter where region == "Asia"
group by product sum profit
show 10
