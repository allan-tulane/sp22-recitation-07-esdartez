import math, queue
from collections import Counter

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    ## This function is done.
    ## Given any file name, this function reads line by line to count the frequency per character. 
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        l = p.get()
        r = p.get()
        p.put(TreeNode(l, r, (l.data[0]+r.data[0], "")))
        
    # return root of the tree
    return p.get()

# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code={}):
    # TODO - perform a tree traversal and collect encodings for leaves in code
    if ((node.left == None) and (node.right == None)):
        code[node.data[1]] = prefix
    if (node.left != None):
        get_code(node.left,prefix+"0", code)
    if (node.right != None):
        get_code(node.right,prefix+"1", code)
    return(code)

# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
    num_bits = math.ceil(math.log2(len(f.keys())))
    return(sum([num_bits*f[x] for x in f.keys()]))
# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    # TODO
    return(sum([len(C[x])*f[x] for x in f.keys()]))

for fname in ['alice29.txt', 'asyoulik.txt', 'f1.txt', 'fields.c', 'grammar.lsp']:
    print(fname)
    f = get_frequencies(fname)
    fc =fixed_length_cost(f)
    print("Fixed-length cost:  %d" % fc)

    T = make_huffman_tree(f)
    C = get_code(T)
    hc = huffman_cost(C, f)
    print("Huffman cost:  %d" % hc)
    h2f = hc/fc
    print("Huffman v.s. Fixed-length cost:  %f" % h2f)
