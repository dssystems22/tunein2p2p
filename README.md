# tunein2p2p
Tune in to peer-to-peer!

## Running
To transfer between two nodes enter the following command on both local terminals:

## Build

`python center.py`
`python peer.py`

## Commmands
`center`: Connect to center
`listpeers` : List all peers
`listfiles`: Quit and disconnect

## Instructions
- `python center.py` Run server
- `python peer.py` Run peer 1 and then give a port
- `python peer.py` Run peer 2 and then give a port

In folder:
- Add a dummy file to peer 1 folder

In peer 1:
- `center`: Connect to the center
- `listpeers`: Check peers
- `listfiles`: List files to server

In peer 2:
- `center`: Connect to the center
- `listpeers`: Check peers
- `check`: check a file name

End in each peer:
- `quit`: Quit and disconnect
