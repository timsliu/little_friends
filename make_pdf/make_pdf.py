# make_pdf.py 
# this program generates a .tex file from the responses
# to the partner feedback questionnaire
#

# Table of contents
#
#
# Revision History
# 05/13/19    Tim Liu    started file - wrote function headers
# 05/16/19    Tim Liu    updated main to write blank .tex file
# 05/20/19    Tim Liu    completed parse_sheets and list2string
# 05/21/19    Tim Liu    set up for actual feedback
# 06/03/19    Tim Liu    added Tools and Additional sheet to 
#                        ANSWER_SHEETS

# libraries
import pandas as pd
import datetime as dt
import math

# global - workbook to open
# WORKBOOK = "test.xlsx"           # excel workbook to open and parse
WORKBOOK = "feedback.xlsx"

# global - list of sheets in workbook; MUST match sheets of WORKBOOK

# sheets in the test excel file
TEST_SHEETS = ["Planes", "Trains"]                 
# sheets in the actual answer excel
ANSWER_SHEETS = ["OS and PDK", "Dev kit", "Tools", "Use cases", "Additional"]
# match sheets to the file being read       
SHEETS = ANSWER_SHEETS

def main():
    '''main function - opens input spreadsheet and generates LaTex output
    '''

    print("Generating LaTeX from: ", WORKBOOK)

    output_string = ""                  # output string to write to .tex file

    header = open("header.txt", "r");        # open file with LaTeX header
    # format target name to include time
    currentDT = dt.datetime.now()
    timestamp = currentDT.strftime("%m-%d_%H-%M")
    target_name = "target_" + timestamp + ".tex"
    # open target file to write to
    target = open(target_name, "w", encoding='utf-8')

    # read in the header
    header_str = header.read()
    # string to add to the header
    output_string = ""

    # parse each sheet
    for s in SHEETS:
        output_string += "\n\\newpage"
        output_string += "\n\\section{" + s + "}\n"
        output_string += parse_sheet(s)

    # add ending to the file
    output_string += "\n\\end{document}"

    # handle special characters
    output_string = output_string.replace("#", "\\#")
    output_string = output_string.replace("%", "\\%")
    output_string = output_string.replace("&", "\\&")
    output_string = output_string.replace("$", "\\$")
    output_string = output_string.replace(">", "$>$")
    output_string = output_string.replace("<", "$<$")
 
    # write to file
    target.write(header_str + output_string)

    # close header file and TeX output
    header.close()
    target.close()

    print("Done! - " + target_name + " saved :D")

    return

def parse_sheet(s):
    '''parses the excel in a sheet
    inputs: s - sheet name to parse
    outputs: sheet_string - TeX string for the sheet'''

    print("Parsing sheet: ", s)

    # open sheet of excel workbook
    data_sheet = pd.read_excel(WORKBOOK, sheet_name=s)
    response_df = pd.DataFrame(data_sheet)

    # map columns to useful labels
    type_col = response_df.columns[0]     # column identifying question type
    q_col    = response_df.columns[1]     # column identifying question     
    partners = response_df.columns[2:]    # columns with partner names

    
    sheet_string = ""                  # TeX string representation of the sheet
    question_type = "none"             # current question type

    # iterate through the rows
    for index, row in response_df.iterrows():

        # check if row has a new question type
        if row[type_col] != question_type:
            # add subsection with new question category
            sheet_string += "\n\\subsection{" + row[type_col] + "}\n"
            # update to the new question type
            question_type = row[type_col]

        # write the question
        sheet_string += "\n\\textbf{" + row[q_col] + "}\n"
        # list with responses from each partner for a single questions
        q_responses = []
        for partner in partners:
            # extract partner response and add to list
            # include partner name as first field
            q_responses.append([partner, row[partner]])
        # convert partner list to string
        sheet_string += list2string(q_responses)

    # close excel file
    # print what had been parsed

    return sheet_string

def list2string(q_responses):
    '''converts the list of partner responses to a LaTeX string
    inputs: q_responses - list of partner responses [[partner, response]]
    outputs: q_string - string representing responses to a question'''

    # TODO - sort the response by persona

    # string for each question
    q_string = ""

    for response in q_responses:
        # convert response to LaTeX format
        if type(response[1]) != type("string") and math.isnan(response[1]):
            # response is blank - skip and go on to next respondent
            continue
        q_string += "\n\\underline{" + response[0] + ":} "
        q_string += "\n" + str(response[1]) + "\n"

    return q_string




