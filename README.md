# Delete Unused IAM Access Keys

Deletes all IAM access keys which are not used at all or haven't been used for over 3 months.

## Dependency

Python3

## Deploy

```
# export aws access keys and IDs in env vars first

# dependencies
pip install -r requirements.txt

# run

python3 main.py 
```
