# Tiny Mesh HTTP API Client 

HTTP API Client for the Tiny Mesh API. Allows easy integration of Tiny Mesh Cloud into any
Python codebase.

## Use

This codebase is experimental at best, it's not suitable for any use.


## Example

CLI Usage:

```
$ python3 tinymesh.py --auth user@example:password list network
[
 {...},
 ...
]
```


Programatic Usage:

```
from tinymesh import resources, auth
from pprint import pprint

token = "..."

auth = auth.TokenV1Auth(token)
pprint(resources.Network.list(auth))
```
