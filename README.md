# Insight Data Engineering Code Challenge Submission

1. [Implementation environment] (README.md#implementation-environment)
2. [Details of Implementation] (README.md#details-of-implementation)

##Implementation environment

The code is written and tested in Python 2 and the packages imported are "collections", "csv", "sys", and "math".

##Details of implementation

In the solution, a class "PayGraph" has been defined to encapsulate the attributes and functions such as check whether the degree of separation between two nodes is below a specified threshold. The historical transaction stored in "batch_payment" file are used to built the PayGraph object.

To achieve high efficiency, a bidirectional Breadth-First-Search(BFS) algorithm is implemented. 

The algorithm takes a payer, a receiver and the threshold of the degree of the separation as parameters. It will check whether the degree of separation between the payer and the receiver is beyond the threshold. The three features required by the problem summary of this code challenge can be implemented by simply setting the threshold of the degree of the separation to 1, 2 and 4 respectively.

The bidirectional BFS is faster than normal BFS since it starts searching for common successor from the nodes of both 'payer' and 'receiver'. 

To make the code even faster, some modification has been made to the bidirectional BFS algorithm. In this code challenge problem, there is a threshold of the degree of the separation. Whenever, an iteration of search has reached the threshold but hasn't found common friends of the 'payer' and 'receiver', the search can be stopped and "unverified" warning will be issued.

