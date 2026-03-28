# DO NOT MODIFY THIS CELL
from abc import ABC, abstractmethod  
class AbstractSearchInterface(ABC):
    '''
    Abstract class to support search/insert operations (plus underlying data structure)
    
    '''
    @abstractmethod
    def insertElement(self, element):     
        '''
        Insert an element in a search tree
            Parameters:
                    element: string to be inserted in the search tree (string)

            Returns:
                    "True" after successful insertion, "False" if element is already present (bool)
        ''' 
        pass 
    @abstractmethod
    def searchElement(self, element):
        '''
        Search for an element in a search tree
            Parameters:
                    element: string to be searched in the search tree (string)

            Returns:
                    "True" if element is found, "False" otherwise (bool)
        '''
        pass

class Node:
    def __init__(self, val1, val2=None):
        self.left_data,self.right_data = val1,val2
        self.left,self.middle,self.right = None,None,None

class TwoThreeTree(AbstractSearchInterface):
    def __init__(self):
        self.head = None

    def insertElement(self, element):

        # Returns: (promoted_key, left_child, right_child, inserted)
        def insert_recursive(node, key):
            if node.left_data == key or node.right_data == key:
                return None, None, None, False

            if node.left is None and node.middle is None and node.right is None:
                # Leaf with one key
                if node.right_data is None:
                    if key < node.left_data:
                        node.left_data, node.right_data = key, node.left_data
                    else:
                        node.left_data, node.right_data = node.left_data, key
                    return None, None, None, True

                # Leaf with two keys
                smallest, middle, largest = sorted((node.left_data, node.right_data, key))
                node.left_data = smallest
                node.right_data = None
                new_right_node = Node(largest)
                return middle, node, new_right_node, True

            if key < node.left_data:
                branch = "left"
                child = node.left
            elif node.right_data is None or key < node.right_data:
                branch = "middle"
                child = node.middle
            else:
                branch = "right"
                child = node.right

            promoted, left_child, right_child, inserted = insert_recursive(child, key)
            if not inserted or promoted is None:
                return None, None, None, inserted

            # Parent with one key:
            if node.right_data is None:
                if branch == "left":
                    original_left_key = node.left_data
                    original_middle = node.middle
                    node.left_data = promoted
                    node.right_data = original_left_key
                    node.left = left_child
                    node.middle = right_child
                    node.right = original_middle
                else:
                    node.right_data = promoted
                    node.middle = left_child
                    node.right = right_child
                return None, None, None, True

            # Parent with two keys
            old_left = node.left
            old_middle = node.middle
            old_right = node.right
            old_key1 = node.left_data
            old_key2 = node.right_data

            if branch == "left":
                promoted_upward = old_key1
                node.left_data = promoted
                node.right_data = None
                node.left = left_child
                node.middle = right_child
                node.right = None
                new_right_parent = Node(old_key2)
                new_right_parent.left = old_middle
                new_right_parent.middle = old_right
            elif branch == "middle":
                promoted_upward = promoted
                node.left_data = old_key1
                node.right_data = None
                node.left = old_left
                node.middle = left_child
                node.right = None
                new_right_parent = Node(old_key2)
                new_right_parent.left = right_child
                new_right_parent.middle = old_right
            else:
                promoted_upward = old_key2
                node.left_data = old_key1
                node.right_data = None
                node.left = old_left
                node.middle = old_middle
                node.right = None
                new_right_parent = Node(promoted)
                new_right_parent.left = left_child
                new_right_parent.middle = right_child

            return promoted_upward, node, new_right_parent, True

        if self.head is None:
            self.head = Node(element)
            return True

        promoted, left_subtree, right_subtree, inserted = insert_recursive(self.head, element)
        if inserted and promoted is not None:
            self.head = Node(promoted)
            self.head.left = left_subtree
            self.head.middle = right_subtree
        return inserted
    
    

    def searchElement(self, element):     
        curr = self.head
        while curr:
            if curr.left_data == element or curr.right_data == element: 
                return True
            if element < curr.left_data:
                curr = curr.left 
            elif  curr.right_data is None or element < curr.right_data:
                curr = curr.middle
            else:
                curr = curr.right
        return False