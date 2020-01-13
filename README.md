# instagram-log-object

## How to set up your log object
```python
log = InstagramLog.Log(filename="log4.gz")
```

## Logging

```python
log.log(context='hello', from_user="from", to_user="to", action="like")
```

## Searching

```python
log.search_user("to") # [alias for search_target]
```

```python
log.search_source(username="from")
```

```python
log.search_target(username="to")
```

## Getting latest as a dictionary

```python
log.latest_as_dict
```

## Deleting log

```python
log.reset()
```