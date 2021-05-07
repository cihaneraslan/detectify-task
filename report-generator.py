import xlsxwriter
import pandas

from detectify import get_scan_profiles, get_latest_full_report

# Create a workbook and add a worksheet.
# from xlsxwriter.worksheet import Worksheet

df = pandas.DataFrame()
writer = pandas.ExcelWriter('Findings.xlsx', engine='xlsxwriter')
workbook = writer.book

# workbook = xlsxwriter.Workbook('Findings.xlsx')
header = workbook.add_format({'bold': True})
header.set_pattern(1)  # This is optional when using a solid fill.
header.set_bg_color('orange')
header.set_font_color('black')
header.set_font_size(14)


def set_column_width(self):
    length_list = [len(x) for x in self.columns]
    for i, width in enumerate(length_list):
        self.worksheet.set_column(i, i, width)


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def prepare_worksheet(ws):
    ws.write(0, 0, "Profile Name", header)
    ws.write(0, 1, "Title", header)
    ws.write(0, 2, "Score", header)
    ws.write(0, 3, "Found At", header)
    ws.write(0, 4, "Date", header)


profiles = get_scan_profiles()  # get 2 scan profiles, check if they are verified (status:verified)
for profile in profiles:
    if profile['status'] == "verified":
        row = 1
        col = 0
        score = 'NA'
        profileName = profile['name']
        df.to_excel(writer, sheet_name=f'{profileName}')
        # worksheet = workbook.add_worksheet(profileName)
        worksheet = writer.sheets[f'{profileName}']
        prepare_worksheet(worksheet)
        report = get_latest_full_report(profile['token'])
        if len(report['findings']) == 0:
            print("No findings!")
        else:
            for finding in report['findings']:
                title = finding['title']
                for scores in finding['score']:
                    if scores['version'] == "2.0":  # assumed there is always one score with version 2.0
                        score = scores['score']
                found_at = finding['found_at']
                date = finding['timestamp'].split("T")[0]
                print(profileName, title, score, found_at, date)
                # Iterate over the data and write it out row by row.
                worksheet.write(row, col, profileName)
                worksheet.write(row, col + 1, title)
                worksheet.write(row, col + 2, score)
                worksheet.write(row, col + 3, found_at)
                worksheet.write(row, col + 4, date)
                row += 1
        set_column_width(df)
    if profile['status'] == "unable_to_resolve":
        profileName = profile['name']
        worksheet = workbook.add_worksheet(profileName)
        worksheet.write(0, 0, "Asset could not be resolved on the last analysis, no report available")
workbook.close()
