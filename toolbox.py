def contains(array, element):
        """[summary]Checks for element in list
        
        Arguments:
            array {[type]} -- [description]
            element {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        print ("element: " + element)
        for item in array:
            print("find " + element + " in " + item)
            if item.find(element) == -1:                
                continue
            else:
                print("element " + element + " found!")
                return True
        return False

def compare(dictionary, element, value, exact_match = False):
    """Compares value of element in Dictionary structure
    
    Arguments:
        dictionary {[type]} -- [description]
        element {[type]} -- [description]
        value {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """        
    if exact_match:
        if element in dictionary:
            return dictionary[element] == value
    else:
        for item in dictionary.keys():
            if item.find(element) == -1:
                continue
            else:
                return (str(dictionary[item]) == str(value))
    return False 