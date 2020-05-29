# connect
Simple file transfer cli tool implemented using sockets in python

# usage
- clone this repo
- ```pip3 install -r requirements.txt``` to install python dependencies
- ```sh depend.sh``` to install system dependencies
- currently tested only for debian based linux distros

# working
- to send files the client and receiver must be connected to same network. 
- users are prompted with what action they want to perform (send or receive). 
- receiver scans the network to find any senders and then prompts user to choose sender from the list while sender waits for someone to join
- sender chooses file to send and then the transfer begins
- after transfer sender can choose to send another file of terminate the connection. the sender is notified in both cases

