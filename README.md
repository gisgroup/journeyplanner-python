# rejseplanen-python
Python client for Rejseplanens API

## Installation
    pip install journeyplanner

## Usage
```
from journeyplanner import JourneyPlanner

client = JourneyPlanner()

client.location('elmegade 5 københavn')
```

## Authentication
```
...
client = JourneyPlanner()
client.authenticate('USERNAME', 'PASSWORD')
...
```
