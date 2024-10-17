

class bin_tree_node: # binary tree node that will store the node data and for the character, frequency and the nodes that are connected to it

    def __init__(self, frequency, character, code = "", left = None, right = None): # If the node is a leaf then both the left and the right ndoes will be None type

        self.left = left

        self.right = right

        self.code = code

        self.frequency = frequency

        self.character = character


    def check_if_leaf(self): # checks if the node is a leaf

        try:

            if self.left.character is None and self.right.character is None: # if the left or right is a character then it is not a leaf
                
                return True

        except: # if the node doesnt have a child node then there is an attribute error meaning its a leaf

            return False




def calculate_codes(node): # This will take the node and calculate the code for it


    codes = {}

    new_code = ""

    def recursive_calculate_codes(node, new_code = ""): # recursively calculates the code for the data
        
        new_code += str(node.code) # will add the code to the total code 

        if node.left is not None: # it will put priority for the left node of the queue
            recursive_calculate_codes(node.left, new_code)
        
        if node.right is not None: # the right node has the next priority
            recursive_calculate_codes(node.right, new_code)

        if node.left is None and node.right is None: # this means that it is a leaf node
            codes[node.character] = new_code # creates a leaf node
             
        return codes

    return recursive_calculate_codes(node, new_code)




def convert_data(data, coding): # converts the data from the character to the converted data

    converted_string = ""
    
    for character in data:

        converted_string += coding[character] # uses the frequency dictionary to convert them
        
    return converted_string




def count_frequency(data): # this is to calculate the freqency of the characters and add them to a list
    
    freqency_dict = {}

    for character in data:
        
        if character in freqency_dict:
            freqency_dict[character] += 1
        
        else:
            freqency_dict[character] = 1
    
    return freqency_dict




def nodes_merge_sort(data):

    if len(data) == 0 or len(data) == 1: # will stop the merge sort if the list is empyt or has one element
        
        return data

    #This is the middle of the array and does floor division on it so that it is at an index
    middle = len(data) // 2

    #This will split the data on the middle of the array
    right_array = data[middle:]
    left_array = data[:middle]

    #This will recurse the function until it has been sorted completely
    nodes_merge_sort(left_array)
    nodes_merge_sort(right_array)

    i = 0
    j = 0
    k = 0

    while i < len(left_array) and j < len(right_array): # there are two different arrays that store the values

        if left_array[i].frequency <= right_array[j].frequency:

            data[k] = left_array[i]
            i += 1

        elif left_array[i].frequency > right_array[j].frequency:

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

    return data



def create_nodes_list(data): # This will create a new list and append the list with all the nodes in the frequency
    
    nodes_list = []
    
    data_freqency = count_frequency(data) # This wil create a freqency dictionary 
    
    for character, frequency in data_freqency.items():

        nodes_list.append(bin_tree_node(frequency, character))

    return nodes_list




def generate_tree(nodes_list): # takes the nodes list and then will make it into one tree

    while len(nodes_list) > 1: # the final node will have the whole tree so if there is 1 node then it is the whole tree
        
        nodes_list = nodes_merge_sort(nodes_list) # sorts the data so that the lowest freqency will be at the front
    

        left = nodes_list[1] # the left one will be the second smallest
        right = nodes_list[0] # the right one will have the smallest code

    
        left.code = "0" # left node is represented by 0
        right.code = "1" # right node is represented by 1

        total_freqeuency = left.frequency + right.frequency # new node will have the new total freqency
        new_character = left.character + right.character # the new character is the total character


        nodes_list.remove(left)
        nodes_list.remove(right)
        nodes_list.append(bin_tree_node(total_freqeuency, new_character, code = "", left = left, right = right)) # creates the new node with the new total freqency and character


def get_code_and_tree(data): # returns the code and tree

    nodes_list = create_nodes_list(data) # makes the nodes list with all the characters

    generate_tree(nodes_list) # creates the tree

    tree = nodes_list[0] # the tree is the first node in the list

    data_with_freqeuency = calculate_codes(tree) # gets the frequency from the characters
    code = convert_data(data, data_with_freqeuency) # gets the final code that uses the plain text data
    
    return code, tree # returns the encoded data and the tree

    
 
def decode_data(coded_data, tree): # takes the coded data and the huffman tree
    
    root = tree # we take the root to be the top of the tree
    final_list = [] # the final list takes all the decoded data

    for character in coded_data: # iterates over the coded data
    
        if character == "1": # if the character is 1 then it will go to the right
            root = root.right # the new root is positioned to the right node
        
        elif character == "0": # if the character is 0 then it is pointing to the left node
            root = root.left # new root is at left node
        
        # this will check if the node is a leaf node

        if root.check_if_leaf() is False:

            final_list.append(root.character) # the final list appends the new character
            root = tree # the root is positioned at the tree
        
    return final_list # returns the final decoded list




def get_tree_from_count_freqeuency(count_frequency):

    nodes_list = []
    
    for character, frequency in count_frequency.items():

        nodes_list.append(bin_tree_node(frequency, character))


    while len(nodes_list) > 1: # the final node will have the whole tree so if there is 1 node then it is the whole tree
        
        nodes_list = nodes_merge_sort(nodes_list) # sorts the data so that the lowest freqency will be at the front
    

        left = nodes_list[1] # the left one will be the second smallest
        right = nodes_list[0] # the right one will have the smallest code

    
        left.code = "0" # left node is represented by 0
        right.code = "1" # right node is represented by 1

        total_freqeuency = left.frequency + right.frequency # new node will have the new total freqency
        new_character = left.character + right.character # the new character is the total character


        nodes_list.remove(left)
        nodes_list.remove(right)
        nodes_list.append(bin_tree_node(total_freqeuency, new_character, code = "", left = left, right = right)) 
    
    return nodes_list[0]



