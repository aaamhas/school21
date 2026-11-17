def data_types():
    data_int = 1
    data_str = "1"
    data_float = 3.4
    data_bool = True
    data_list = [1,2]
    data_dict = {1 : '1'}
    data_tuple = (1,2)
    data_set = set([3,3,5])
    lst = [str(type(data_int).__name__), str(type(data_str).__name__),
    str(type(data_float).__name__), str(type(data_bool).__name__), 
    str(type(data_list).__name__), str(type(data_dict).__name__),
    str(type(data_tuple).__name__), str(type(data_set).__name__)]
    result = ", ".join(lst)
    print(f'[{result}]')

if __name__ == '__main__':
    data_types()
    