# Distributed Resource Manager

**Python Implementation of a Client\Server application that allows multi-client remote resource management using Sockets.** 

### Usage:
**Run Server:**
```
python3 lock_server.py <PORT> <NUMBER_OF_RESOURCES> <NUMBER_OF_LOCKS_ALLOWED_BY_RESOURCE> <NUMBER_OF_LOCKS_ALLOWED_IN_A_MOMENT> <CONCESSION TIME>
```

**Run Client:**
```
python3 lock_client.py <HOST> <PORT> <CLIENT_ID>
```

**Client Comands:**
```
LOCK <RESOURCE NUMBER>     : [11, True] or [11, False] or [11, None]
RELEASE <RESOURCE NUMBER>  : [21, True] or [21, False] or [21, None]
TEST <RESOURCE NUMBER>     : [31, True] or [31, False] or [31, disable] or [31, None]
STATS <RESOURCE NUMBER>    : [41, <Number of Locks in the resource K>] or [41, None]
STATS-Y                    : [51, <Number of Locked Resources in Y]
STATS-N                    : [61, <Number of Available Resources]
```
