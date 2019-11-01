# multiprocessing 

there are two main functions. 

1) send cumulated tweets(now 100 or == to size of ML model batch size) to SQS as a bundle.
2) keep listening from the Twitter server to get correct Tweets. 



each Processor(core) will 


I used MapReduce multi-processing method to work faster(parallelize the work)


There are times when its important to synchronize two or more threads while concurrently running seperate operations. 
Event object is the simple way to communicate between threads