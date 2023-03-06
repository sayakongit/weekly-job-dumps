from utils.actions import read_sheet_data

def test():
    data, sheet = read_sheet_data('Jobs', 'Test')
    print(data)
    
test()