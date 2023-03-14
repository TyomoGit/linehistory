"""
linehistory
(c)2023 Tyomo
"""

import calendar
import random
import re
from datetime import datetime

class History:
    history_data: list[str]
    asterisk: bool
    DATE_PATTERN: str = r'^\d{4}/\d{2}/\d{2}\(.+\)$'
    YMD_PATTERN: str = "%Y/%m/%d"
    
    def __init__(self, data: str, asterisk: bool = False) -> None:
        """
        asterisk:
        If True, an asterisk is appended to each line of output.
        """

        _data = data.splitlines()

        isFormal = False
        for line in _data:
            if re.match(self.DATE_PATTERN, line):
                isFormal = True
                break
        if isFormal == False:
            raise Exception("Invalid history data.")

        if "のトーク履歴" in _data[0]:
            self.history_data = _data[3:]
        else:
            self.history_data = _data

        self.asterisk = asterisk

    def search_by(self, arg: datetime | str = "") -> str:
        """
        If a datetime type is entered, the search is performed on that date.
        If a str type is entered, the search is performed using the keyword.
        If no argument is specified, the history is output at random.
        """
        if isinstance(arg, datetime):
            return self.search_by_date(date=arg)
        elif isinstance(arg, str):
            return self.search_by_keyword(keyword=arg)
        elif arg == "":
            return self.search_by_random()
        else:
            raise Exception("invalid argument")

    def search_by_date(self, date: datetime) -> str:
        date_input = date
        count_start: int = -1
        count_stop: int = -1
        count_flag: bool = False
        output: str = ""

        for i, line in enumerate(self.history_data):
            if re.match(self.DATE_PATTERN, line):
                date_tmp = datetime.strptime(line[:10], self.YMD_PATTERN)

                if date_tmp == date_input:
                    count_start = i
                    count_flag = True
                    output += f"{line}\n"
                elif count_flag and date_input < date_tmp:
                    count_stop = i
                    break
            elif count_flag:
                output += f"{line}\n"
                if i == len(self.history_data) - 1:
                    count_stop = i
                    break
        
        if count_start == -1:
            output = "There is no history of this date.\n"
        else:
            output += f"{count_stop - count_start}行\n"
        return self.__make_output(data=output)

    def search_by_random(self) -> str:
        today: int = int(datetime.today().timestamp())
        first: int = 0
        for line in self.history_data:
            if re.match(self.DATE_PATTERN, line):
                first = int(datetime.strptime(line[:10], self.YMD_PATTERN).timestamp())
                break

        result: str = "There is no history of this date."
        while "There is no history of this date." in result:
            random_num = random.randint(first, today)
            date = datetime.fromtimestamp(random_num)
            result = self.search_by_date(date)
        return self.__make_output(data=result)

    def search_by_keyword(self, keyword: str) -> str:
        count = 0
        output = ''
        date = datetime(1,1,1)
        LOWER_LIMIT = 1
        if len(keyword) >= LOWER_LIMIT:
            max_date = datetime.min
            for line in self.history_data:
                if re.match(self.DATE_PATTERN, line):
                    if datetime.strptime(line[:10], self.YMD_PATTERN) >= max_date:
                        date = datetime.strptime(line[:10], self.YMD_PATTERN)
                        max_date = date
                else:
                    if keyword in line: #00:00 riku aaaa
                        count += 1
                        if re.match(r'^\d{2}:\d{2}.*', line):  #時刻を削除
                            line = line[6:]
                        if len(line) >= 61:
                            line = line[:60] + '…'
                        output += str(date)[:11].replace('-', '/') + " " + line + '\n'
        if output == '':
            output = 'Not found.'

        return self.__make_output(data= f"{count}件\n{output}")

    def create_calendar(self, month: datetime) -> str:
        if not isinstance(month, datetime):
            raise Exception("invalid argument.")
        
        _year = month.year
        _month = month.month
        cal = calendar.month(_year, _month, w=4).replace(f" {_year}", f"_{_year}")
        min_date = datetime(_year, _month, 1)
        days: list[int] = []

        loop_flag: bool = False
        for i, line in enumerate(self.history_data):
            if re.match(self.DATE_PATTERN, line):
                _date = datetime.strptime(line[:10], self.YMD_PATTERN)
                if _date.year == _year and _date.month == _month:
                    loop_flag = True
                    days.append(_date.day)
                elif loop_flag and _date.month > min_date.month:
                    break
        for day in days:
            cal = cal.replace(f" {day}", f"_{day}", 1)
        return cal
    
    def __make_output(self, data: str) -> str:
        if self.asterisk == True:
            return History.add_asterisk(message=data)
        else:
            return data
    
    @staticmethod
    def add_asterisk(message: str) -> str:
        result: str = ""
        for line in message.splitlines():
            result += f"*{line}\n"
        return result
