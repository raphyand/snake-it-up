"""Records utility module to assist in pickle processing"""
__author__ = 'Raphael S. Andaya'
__email__ = 'raphyand@csu.fullerton.edu'
__maintainer__ = 'raphyand'

class RecordList():
    """Records List Class"""
    def __init__(self):
        self.record_list = []

    def append(self, record):
        """Records List Class append to list"""
        self.record_list.append(record)

    def get_list(self):
        """Records List Class to retrieve list"""
        return self.record_list

    def sort(self):
        """Records List Class to sort all records in list"""
        self.record_list.sort(key=lambda rl: rl.get_score(), reverse= True)

class Record():
    """Records Class"""
    def __init__(self, score, date_time, time_elapsed):
        self._score = score
        self._date_time = date_time
        self._time_elapsed = time_elapsed

    def get_score(self):
        return self._score

    def get_date_time(self):
        return self._date_time
    
    def get_time_elapsed(self):
        return self._time_elapsed

    def write_record(self):
        write_score = str(self.get_score())
        write_date_time = str(self.get_date_time())
        write_time_elapsed = str(self.get_time_elapsed())
        output = 'Score: ' + write_score + '| Date: ' + write_date_time + '| Time Elapsed: ' + write_time_elapsed
        return output