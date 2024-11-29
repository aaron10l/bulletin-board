# Project 2: Simple Bulletin Board Using Socket Programming
### Team Members 

**Akshat Chaturvedi**
**Aaron Alvarez**
**Ethan Reed**

## Introduction

This project implements a client-server bulletin board system using unicast sockets. The application consists of two parts:

1. A public message board where users can join, post messages, and interact with others.
2. Private message boards allowing users to join multiple groups and exchange group-specific messages.

## Features
### Part 1: Public Message Board

**Users can:**

1. Connect to the server using a unique username.
2. Post public messages visible to all users.
3. Retrieve the last two messages posted before joining.
4. View a list of connected users.
5. Retrieve specific messages by ID.
6. Leave the group.

### Part 2: Private Message Boards

**Users can:**

1. View and join available groups.
2. Participate in multiple groups simultaneously.
3. Post and retrieve group-specific messages.
4. View group members.
5. Leave individual groups.

## Technologies Used

**Programming Languages :** Python

**Sockets :** TCP sockets for communication

**Protocol :** Custom-designed

## Commands and Usage

### General Commands

%connect 127.0.0.1 65432 : Connect to the server. // The IP address should the IP address of the server and the port should be the one to connect to.

%exit : Disconnect from the server

### Part 1: Public Message Board

%join: Join the public message board.

%post <subject> <content>: Post a public message.

%users: View all connected users.

%message <message_id>: Retrieve a specific message by ID.

%leave: Leave the public group.

### Part 2: Private Message Boards

%groups: List all available groups.

%groupjoin <group_id/name>: Join a specific group.

%grouppost <group_id/name> <subject> <content>: Post a message to a specific group.

%groupusers <group_id/name>: View users in a group.

%groupleave <group_id/name>: Leave a specific group.

%groupmessage <group_id/name> <message_id>: Retrieve a specific group message by ID.

## Installation and Execution

### Server

1. Navigate to the server directly.
2. Run the server : python3 server.py 65432

### Client

1. Navigate to the client directory.
2. Run the client : python3 client.py 

## Issues and Limitations

1. The server might not handle a large number of simultaneous clients efficiently due to limitations in multithreading or network bandwidth.
2. The clients might disconnect unexpectedly due to weak error handling.
3. Synchronization issues may arise when multiple users join, leave, or post messages in the same group simultaneously.
4. Messages and user data are not saved permanently.They are lost if the server is restarted unless persistence is implemented.


## Acknowledgements

**Instructor: Prof. Giovani Abuaitah**

**Course: CS4065 Computer Networks and Networked Computing**



    
   
