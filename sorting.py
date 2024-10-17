import datetime

def inner_func(data, sort_by = "alphabetical"):

    if len(data) > 1:
        

        #This is the middle of the array rounded to the nearest whole number
        middle = len(data) // 2

        #This will split the data on the middle of the array
        
        left_array = data[:middle]
        right_array = data[middle:]


        #This will recurse the function until it has been sorted completely
        inner_func(left_array)
        inner_func(right_array)

        i = 0
        j = 0
        k = 0




        while i < len(left_array) and j < len(right_array):

            compare_left_array = left_array[i]["file_name"]
            compare_right_array = right_array[j]["file_name"]


            if sort_by == "alphabetical" or sort_by == "reverse_alphabetical":
                compare_left_array = left_array[i]["file_name"]
                compare_right_array = right_array[j]["file_name"]

            
            elif sort_by == "datetime":

                la_datetime = left_array[i]["raw_datetime"]
                ra_datetime = right_array[j]["raw_datetime"]

                left_time_data = f"""{la_datetime["day"]}/{la_datetime["month"]}/{la_datetime["year"]} {la_datetime["hour"]}:{la_datetime["minute"]}"""
                right_time_data = f"""{ra_datetime["day"]}/{ra_datetime["month"]}/{ra_datetime["year"]} {ra_datetime["hour"]}:{ra_datetime["minute"]}"""
                
                format_data = "%d/%m/%y %H:%M"
                compare_left_array = datetime.datetime.strptime(left_time_data, format_data)
                compare_right_array = datetime.datetime.strptime(right_time_data, format_data)
               


            if compare_left_array < compare_right_array:


                data[k] = left_array[i]
                i += 1

            else:

                data[k] = right_array[j]
                j += 1

            k += 1

        #This will check if there are any elements left in the left array
        while i < len(left_array):

            data[k] = left_array[i]
            i += 1
            k += 1

        #This will check if there are any elements left in the right array
        while j < len(right_array):
            
            data[k] = right_array[j]
            j += 1
            k += 1



def merge_sort(data, sort_by = "alphabetical"):
    
    new_data = data
    inner_func(new_data)

    if sort_by == "reverse_alphabetical":
        return new_data[::-1]
    
    else:
        return new_data

