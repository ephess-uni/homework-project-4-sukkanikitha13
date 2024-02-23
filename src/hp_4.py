# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    old_date_objs = list()
    reform_dates = list()
    
    for date in old_dates:
        old_date_objs.append(datetime.strptime(date, '%Y-%m-%d'))
        
    for dates in old_date_objs:
        reform_dates.append(dates.strftime("%d %b %Y"))
    return reform_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not (isinstance(start, str)):
        raise TypeError("Start is not a string")
    elif not isinstance(n, int):
        raise TypeError("n is not a integer")
    else:
        N_date_list = []
        start_date = datetime.strptime(start, '%Y-%m-%d')
        for day in range(n):
            date_obj = (start_date, datetime.timedelta(day = day)).isoformat()
            N_date_list.append(date_obj)
        return N_date_list
    

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    N_date_list = date_range(start_date, len(values))
    N_date_list_values = list()
    for (i, j) in zip(range(len(values)), values):
        N_date_list_values.append((N_date_list[i], j))
    return N_date_list_values


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)
    with open(infile, newline='') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            patronid = row['patron_id']
            return_date = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            late_day = (return_date - due_date).days

            if late_day > 0:
                late_fee = late_day * 0.25
                late_fees[patronid] += late_fee
            else:
                late_fees[patronid] = 0.00

    with open(outfile, 'w') as csvfile:
        write = DictWriter(csvfile, fieldnames=['patron_id','late_fee'])
        write.writeheader()
        for patron_id, fee in late_fees.items():
            write.writerow({
                'patron_id': patron_id,
                'late_fee': f'{fee:.2f}',
            })

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
