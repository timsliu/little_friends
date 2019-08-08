# helper functions for LaTex output
#
# Table of contents
# make_table   - turns a python list into a LaTex formatted table
# text2tex     - converts plain formatted text string into
#                LaTex format by handling quotation marks and special
#                characters
# excel2pdf    - main function for converting excel spreadsheet to
#                a pdf
# parse_sheet  - parse a single excel sheet; helper for excel2pdf
# list2string  - convert an excel formatted list to a string
#                helper function for excel2pdf
# special_char - handle special characters to be LaTeX compatible


# Revision history
# 06/26/19    Tim Liu    copied make_table from b2_extra.py
# 06/26/19    Tim Liu    wrote text2tex
# 06/26/19    Tim Liu    copied make_pdf main and helper functions - 
#                        TODO make functions generic
# 06/29/19    Tim Liu    removed global variables from excel2pdf; code
#                        has not been retested
# 08/06/19    Tim Liu    modified how quotes are replaced in text2texex
# 08/08/19    Tim Liu    updated make_table to print correct number of
#                        backslashes


# libraries
import pandas as pd
import datetime as dt
import math


def make_table(c, r, data, title):
    '''prints string of latex formatted table
    inputs: c - list of colum labels
            r - list of row labels
            data - 2D array of data
            title - title of plot
    outputs: prints latex string
    return: none'''
    
    #print formatting
    print('\\begin{center}')
    print('\\begin{tabular}{' + (len(c) + 1)* '|m{1.7 cm}', '|}')
    print('\\hline')
    print('\\multicolumn{%d}{|c|}{%s}\\\\ \\hline' %((len(c)+1), title))
    for col in c:
        print('&', col, end='')
    print('\\\\ \\hline')
    #iterate through data and print data
    for row in range(len(r)):
        print(r[row], end='  ')        
        for col in range(len(c)):
            print(' & ', '%.3f' %data[col][row], end = '')
        print('\\\\ \\hline')
    print('\\end{tabular}')
    print('\\end{center}')
    return


def text2tex(f_in_name, f_out_name):
    '''converts a plain text string to a LaTex formatted
    string. Currently corrects double quotation marks and the following
    special characters: #, %, &, $, >, <
    inputs: f_in_name - input file name
            f_out_name - output file name

    the tex string is saved to a text file under the name f_out_name.
    The function does not handle double nested quotes'''

    print("Parsing file: ", f_in_name)

    
    f_in = open(f_in_name, "r")       # open the input file w/ plaintext
    input_string = f_in.read()        # read contents of the file
    output_string = ""                # string to output

    # convert quotation marks to open and close marks
    for char in input_string:
        print(ord(char))
        if ord(char) == 8220:
            print("open")
            output_string += '"'
        elif ord(char) == 8221:
            print("close")
            output_string += '``'
        else:
            # directly copy any non quotation character
            output_string += char

    # handle special characters
    output_string = output_string.replace("#", "\\#")
    output_string = output_string.replace("%", "\\%")
    output_string = output_string.replace("&", "\\&")
    output_string = output_string.replace("$", "\\$")
    output_string = output_string.replace(">", "$>$")
    output_string = output_string.replace("<", "$<$")

    # open output file
    f_out = open(f_out_name, "w", encoding='utf-8')
    f_out.write(output_string)

    # close input file and generated file
    f_in.close()
    f_out.close()

    print("Tex format file saved!")

    return


def excel2pdf(workbook, sheets):
    '''Converts an excel workbook into a LaTex pdf. Each sheet in the
    workbook becomes a section, the first column of the sheet becomes a
    subsection, each row of the second column is bolded, and
    each remaining column for a row is a paragraph with the column header
    formatted into a header. 

    args:    workbook - name of .xlsx workbook to open
             sheets - list of sheets to parse; elements in list
                     must exactly match the name of sheets in 
                     workbook
    returns: none
    outputs: .tex file named with a timestamp'''

    print("Generating LaTeX from: ", workbook)

    header = open("header.txt", "r");     # open file with LaTeX header
    # format target name to include time
    currentDT = dt.datetime.now()
    timestamp = currentDT.strftime("%m-%d_%H-%M")
    target_name = "target_" + timestamp + ".tex"
    # open target file to write to
    target = open(target_name, "w", encoding='utf-8');

    # read in the header - contains preamble of LaTex output
    header_str = header.read()
    # string to add to the header
    output_string = ""

    # parse each sheet
    for s in sheets:
        output_string += "\n\\newpage"
        output_string += "\n\\section{" + s + "}\n"
        output_string += parse_sheet(s)

    # add ending to the file
    output_string += "\n\\end{document}"

    # handle special characters
    # TODO - change to generic replace function
    output_string = output_string.replace("#", "\\#")
    output_string = output_string.replace("%", "\\%")
    output_string = output_string.replace("&", "\\&")
    output_string = output_string.replace("$", "\\$")
    output_string = output_string.replace(">", "$>$")
    output_string = output_string.replace("<", "$<$")
 
    # write to target file
    target.write(header_str + output_string)

    # close header file and TeX output
    header.close()
    target.close()

    print("Done! - " + target_name + " saved :D")

    return

def parse_sheet(workbook, s):
    '''parses an excel sheet and converts to a TeX string
    args:    workbook - name of workbook to open
             s - sheet name to parse
    return:  sheet_string - TeX string for the sheet
    outputs: none'''

    print("Parsing sheet: ", s)

    # open sheet of excel workbook
    data_sheet = pd.read_excel(workbook, sheet_name=s)
    response_df = pd.DataFrame(data_sheet)

    # map columns to useful labels
    # TODO - rename variables to not be specific
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
    args:    q_responses - list of partner responses [[partner, response]]
    returns: q_string - string representing responses to a question'''

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


def special_char():
	'''converts special characters in a text string to the form that LaTex
	   can interpret'''
    # TODO
	return

