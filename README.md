# DAX30 Analyser

## Introduction

In connection with a SHK ("**S**tudentische **H**ilfs**K**raft") project the AI readiness of the 30 DAX companies shoulb be analysed. For this analysis the following steps were performed:

* compile keywords that are indicators for technology or espacially AI usage
* quantitative analysis of the DAX pdf-reports
* plotting the extracted data
* comparison of the results

For the quantitative analysis and the plotting of the extracted data this tool is for.

## Table of Contents

1. [Introduction](#Introdurction)
2. [How to use](#Howtouse)
   1. [Setup](#Setup)
   2. [Usage](#Usage)
3. [Contributing](#Contributing)
4. [Links](#Links)

## How to use

### Setup

* The tool is written in Python and the version **3.8.6** is used.
* **Installation of used libaries**
  The used libaries (that are not installed by default) are listed in the **`requirements.txt`** file.
  To install them use the command: *pip install -r `requirements.txt`*
* to install the german nlp-model execute:
  `python -m spacy download de_dep_news_trf`

### Usage

The pdf-report should be placed into the `PDF-Data`  folder with the company name as a subfolder. The script is extracting the quantity of the given keywords and exports it into the `extracted_data` folder as a `output_<company name>.xlsx` file. The data is also plotted and saved into the `plots` folder as a `output_<company name>.png` file. In the `main()` function can be choosed if data should be extracted from a pdf or from a existing excel-file.

```python
# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    main(analyse_pdf=False)
```

The `analyse_pdf` parameter is per default on True.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Links

Helpfull links:

* [link](https://letmegooglethat.com/)
