import linehistory as lh
from datetime import datetime

his = lh.History.of("/Users/riku/Library/Mobile Documents/com~apple~CloudDocs/🐸GAshare/history.txt")
# print(his.search_by_date(datetime(2023, 11, 13)))
print(his.range_after(datetime(2024, 1, 13)))