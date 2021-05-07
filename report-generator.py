import xlsxwriter

from detectify import get_scan_profiles, get_latest_full_report
from xlsxwriter.worksheet import Worksheet

# Create a workbook
workbook = xlsxwriter.Workbook('Findings.xlsx')
header = workbook.add_format()
alignment = workbook.add_format()


# Define header format
def _define_headers():
    header.set_bold(True)
    header.set_pattern(1)  # This is optional when using a solid fill.
    header.set_bg_color('orange')
    header.set_font_color('black')
    header.set_font_size(14)


# Define cell alignment
def _set_alignment():
    alignment.set_align('left')


# Prepare worksheet headers and column width
def prepare_worksheet(profile_name: str, empty: bool) -> Worksheet:
    if empty:
        ws = workbook.add_worksheet(profile_name)
        ws.set_column(0, 0, 50)
    else:
        _define_headers()
        _set_alignment()
        ws = workbook.add_worksheet(profile_name)
        ws.write(0, 0, "Profile", header)
        ws.write(0, 1, "Title", header)
        ws.write(0, 2, "Score", header)
        ws.write(0, 3, "Found At", header)
        ws.write(0, 4, "Date", header)
        ws.set_column(0, 0, 30)
        ws.set_column(1, 1, 40)
        ws.set_column(2, 2, 10)
        ws.set_column(3, 3, 50)
        ws.set_column(4, 4, 15)
    return ws


def fill_excel(report: dict, profilename: str, worksheet: Worksheet):
    row = 1
    col = 0
    score = 'NA'
    if len(report['findings']) == 0:
        print("No findings!")
    else:
        report['findings'].sort(key=lambda x: x['title'], reverse=False)
        for finding in report['findings']:
            title = finding['title']
            for scores in finding['score']:
                if scores['version'] == "2.0":  # assumed there is always one score with version 2.0
                    score = scores['score']
            found_at = finding['found_at']
            date = finding['timestamp'].split("T")[0]
            print(profilename, title, score, found_at, date)
            # Iterate over the data and write it out cell by cell.
            worksheet.write(row, col, profilename, alignment)
            worksheet.write(row, col + 1, title, alignment)
            worksheet.write(row, col + 2, score, alignment)
            worksheet.write(row, col + 3, found_at, alignment)
            worksheet.write(row, col + 4, date, alignment)
            row += 1
        worksheet.add_table(0, 0, row - 1, 4, {'banded_rows': True, 'header_row': False})  # Format data as table


if __name__ == '__main__':
    # Get scan profiles that are authorized by API Key and Secret Key
    profiles = get_scan_profiles()
    for profile in profiles:
        if profile['status'] == "verified":
            formatted_worksheet = prepare_worksheet(profile['name'], False)
            rep = get_latest_full_report(profile['token'])  # Get the latest report for a specific scan profile via API
            fill_excel(rep, profile['name'], formatted_worksheet)
        if profile['status'] == "unable_to_resolve":
            formatted_worksheet = prepare_worksheet(profile['name'], True)
            formatted_worksheet.write(0, 0, "Asset could not be resolved on the last analysis, no report available")
    workbook.close()
