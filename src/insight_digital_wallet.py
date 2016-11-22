
# coding: utf-8


import collections
import math
import csv
import sys




# define a class PayGraph 
# attributes: vertices and edges
# functions: add_vertex, add_edge, get_successor and bidirectional_bfs
class PayGraph:
    def __init__(self):
        self.vertices = set()
        self.edges = collections.defaultdict(list)
        
    def add_vertex(self, vertex_name):
        if(vertex_name not in self.vertices):
            self.vertices.add(vertex_name)
            
    def add_edge(self, vertex_from, vertex_to):
        if vertex_from == vertex_to:pass
        if (vertex_to not in self.edges[vertex_from]):
            self.edges[vertex_from].append(vertex_to)
        if (vertex_from not in self.edges[vertex_to]):
            self.edges[vertex_to].append(vertex_from)
            
    def __str__(self):
        graph_info = "In the PayGraph, there are: \n"
        graph_info+= "Vertices: " +str(self.vertices) +"\n"
        graph_info+= "Edges: "+ str(self.edges)+"\n"
        return graph_info
    
    def get_successor(self,queue,visited):
        '''
        This function will get adjacent nodes of the nodes in the queue
        input: 
             queue(deque): a list of nodes
             visited(set): a set of nodes that have been visited
        output:
             neighbour_queue(deque): a list nodes that are adjacent from the node in the queue
             visited(set): updated set of nodes that have been visited             
        '''
        neighbour_queue = collections.deque([])
        while queue:
            vertex= queue.popleft()
            for neighbour in self.edges[vertex]:
                if neighbour not in visited:    
                    visited.add(neighbour)
                    neighbour_queue.append(neighbour)        
        return neighbour_queue, visited

    def bidirectional_bfs(self, payer, receiver,max_allowed_degree):
        '''
        This function check whether the degree of separation between two nodes ('payer', 'receiver') is 
        less than or equal to max_allowed_degree. 
        If it is yes, "trusted" will be return, otherwise, "unverified" will be returned.
        
        input:
             payer(string): a node
             receiver(string): a node
             max_allowed_degree(int): the upper boundary of the degree of separation that will be accepted.
        output:
             return "trusted" or "unverified"
        '''
        degree = 1
        payer_successor = collections.deque([payer])
        receiver_successor = collections.deque([receiver])
        payer_visited = set()
        receiver_visited = set()
        
        while payer_successor and receiver_successor and degree<=max_allowed_degree:
            payer_successor, payer_visited = self.get_successor(payer_successor, payer_visited)
            if(set(payer_successor).intersection(receiver_successor) and degree<=max_allowed_degree):
                #print(set(payer_successor).intersection(receiver_successor))
                return "trusted"
            degree+=1
            
            receiver_successor, receiver_visited = self.get_successor(receiver_successor, receiver_visited)
            if(set(payer_successor).intersection(receiver_successor) and degree<=max_allowed_degree):
                #print(set(payer_successor).intersection(receiver_successor))
                return "trusted"
            degree+=1
        return "unverified" 
    




def check_input(line):
# to check whether a line in the input file is a valid input
    flag = False
    if line['payer']!=None and line['receiver']!=None:
        flag=True
    return flag




def create_paygraph(batch_file):
    '''
    This function is to build the graph from the batch_payment file
    input: 
          batch_file(string): the path for batch_payment file  
    output:
          pay_graph(PayGraph): a PayGraph object
    '''
    pay_graph = PayGraph()
    with open(batch_file, 'r') as input_file:
        lines = csv.DictReader(input_file, fieldnames = ("time", "payer","receiver","amount", "message"), delimiter=',', 
                               skipinitialspace=True, quoting=csv.QUOTE_NONE)
        next(lines, None) # the first line is header, it will be skipped.
        for line in lines:
            if check_input(line):
                pay_graph.add_vertex(line['payer'])
                pay_graph.add_vertex(line['receiver'])
                pay_graph.add_edge(line['payer'],line['receiver'])
    return pay_graph
                           




def process_streamfile(stream_file,output_file, graph, max_allowed_degree):
    '''
    This function process the input from the stream_file and write the results to the output_file
    input:
        stream_file(string): the directory path and name of the streamfile
        output_file(string): the directory path and name of the output file
        graph(PayGraph): the graph built based on the transaction in the batchfile
        max_allowed_degree: the threshold of degree of separation between payer and receiver when the relationship is trusted.
    output:
        the result for each piece of transaction is written into the output_file.
    '''
    with open(stream_file,'r') as in_file:
        with open(output_file,'w') as out_file:
            lines = csv.DictReader(in_file, fieldnames = ("time", "payer","receiver","amount", "message"), delimiter=',', 
                               skipinitialspace=True, quoting=csv.QUOTE_NONE)
            next(lines, None) # the first line is header, it will be skipped.
            for line in lines:
                if check_input(line):
                    result = graph.bidirectional_bfs(line['payer'],line['receiver'],max_allowed_degree)
                    out_file.write(result+"\n")
                else:
                    out_file.write("unknow\n")
                    
            




def main():
    batch_file = sys.argv[1]
    stream_file = sys.argv[2]
    output_file_1 = sys.argv[3]
    output_file_2 = sys.argv[4]
    output_file_3 = sys.argv[5]
    
    pay_graph=create_paygraph(batch_file)
    process_streamfile(stream_file,output_file_1,pay_graph,1)
    process_streamfile(stream_file,output_file_2,pay_graph,2)
    process_streamfile(stream_file,output_file_3,pay_graph,4)
    
    
if __name__ == '__main__':
    main()
    




