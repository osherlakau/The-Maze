# The-Maze
General description:
Create a server that prepares a random maze using two dimensional grid, the server chooses the first tile as a bot. The server connects to the client, and from there it waits for a move / direction from the client (right, down, left, up).
Of course, the entire maze and the bot are visible to the client on the window that opens when the code is run, so that the client knows with each move where he is instructing the bot to go.
The code files:
1. Server.py - Server code that builds a random maze with the bot inside.
2. Client.py - ⁠Client code that tries to solve the maze by controlling the bot's movements.
Used Python libraries: Pygame (window display), Keyboard (buttons setting).
