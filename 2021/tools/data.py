"""
Set of functions to better import data and chop it to a workable format.
"""
class ReadAndSplit(object):
    input_data = ''
    data_array = []

    def __init__(self, data_path):
        data_read = open(data_path, 'r')
        self.input_data = data_read.read()
        data_read.close()

    def __repr__(self):
        if len(self.data_array) == 0:
            return self.input_data
        else:
            return str(self.data_array)

    def __len__(self):
        return len(self.input_data)

    def __getitem__(self, index):
        if len(self.data_array) == 0:
            return self.input_data[index]
        else:
            return self.data_array[index]

    def split_break(self, data_type="str"):
        """If there is no temp data, it returns the data object split by breaks and stores it in data_array.
        If the data_array already contains data (a previous split), this function uses that data and returns a
        break split for each item in the array."""

        if len(self.data_array) == 0:
            self.data_array = self.input_data.split('\n')
        else:
            temp = []
            for item in self.data_array:
                temp.append(item.split('\n'))
            self.data_array = temp

        if data_type == "int":
            temp = []
            for i in self.data_array:
                temp.append(int(i))

            self.data_array = temp

    def split_double_break(self):
        """If there is no temp data, it returns the data object split by double breaks and stores it in data_array.
        If the data_array already contains data (a previous split), this function uses that data and returns a double
        break split for each item in the array."""

        if len(self.data_array) == 0:
            self.data_array = self.input_data.split('\n\n')
        else:
            temp = []
            for item in self.data_array:
                temp.append(item.split('\n\n'))
            self.data_array = temp

    def split_on(self, split_sign, data_type="str"):
        """If there is no temp data, it returns the data object split by
        the chosen split sign and stores it in data_array.
        If the data_array already contains data (a previous split),
        this function uses that data and returns a split for each item in the array."""

        if len(self.data_array) == 0:
            self.data_array = [int(x) for x in self.input_data.split(split_sign)]
        else:
            temp_1 = []
            for item in self.data_array:
                if type(item) == list:
                    temp_2 = []
                    for i in item:
                        if data_type == "int":
                            lst_int = [int(x) for x in i.split(split_sign)]
                            temp_2.append(lst_int)
                        elif data_type == "str":
                            temp_2.append(i.split(split_sign))
                    temp_1.append(temp_2)
                else:
                    if data_type == "int":
                        lst_int = [int(x) for x in item.split(split_sign)]
                        temp_1.append(lst_int)
                    elif data_type == "str":
                        temp_1.append(item.split(split_sign))
            self.data_array = temp_1

class ReadData(object):
    def __init__(self, path, lines=True, read_int=False):
        with open(path, "r") as f:
            if lines:
                if read_int:
                    self.data = [int(line.rstrip('\n')) for line in f]
                else:
                    self.data = [line.rstrip('\n') for line in f]
            else:
                self.data = f.read()

    def __repr__(self):
        return str(self.data)
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def pop_data(self, index):
        return self.data.pop(index)

    def special_split(self, sign=None, make_int=False):
        def recursive_split(data):
            if type(data) == str:
                if make_int:
                    return [int(i) for i in data.split(sign)]
                return data.split(sign)
            elif type(data) == list:
                if type(data[0]) == str:
                    if make_int:
                        temp = [i.split(sign) for i in data]
                        return [[int(i) for i in top] for top in temp]
                    return [i.split(sign) for i in data]
                elif type(data[0]) == list:
                    return [list(map(recursive_split, i)) for i in data]
        self.data = recursive_split(self.data)