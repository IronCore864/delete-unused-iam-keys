import boto3
from datetime import datetime

iam = boto3.client('iam')

seconds_in_day = 60 * 60 * 24
days_in_month = 30


def get_all_users():
    res = []
    response = iam.list_users()
    for user in response['Users']:
        res.append(user['UserName'])
    return res


def get_all_access_keys_from_user(username):
    res = []
    paginator = iam.get_paginator('list_access_keys')
    for page in paginator.paginate(UserName=username):
        for key_detail in page['AccessKeyMetadata']:
            res.append(key_detail['AccessKeyId'])
    return res


def get_access_key_last_used(access_key_id):
    response = iam.get_access_key_last_used(AccessKeyId=access_key_id)
    return response['AccessKeyLastUsed']['LastUsedDate'] if 'LastUsedDate' in response['AccessKeyLastUsed'] else None


def get_not_used_months(last_used_datetime):
    last_used_naive = last_used_datetime.replace(tzinfo=None)
    not_used_time = datetime.now() - last_used_naive
    return not_used_time.total_seconds() // seconds_in_day // days_in_month


if __name__ == '__main__':
    never_used = []
    not_used_over_3_months = []

    for user in get_all_users():
        keys = get_all_access_keys_from_user(user)
        for key in keys:
            last_used = get_access_key_last_used(key)
            if last_used:
                if get_not_used_months(last_used) >= 3:
                    not_used_over_3_months.append({'name': user, 'key': key})
            else:
                never_used.append({'name': user, 'key': key})
    for user in never_used:
        print("User {} access key ID {} has never been used, deleting now...".format(user['name'], user['key']))
        response = iam.delete_access_key(UserName=user['name'], AccessKeyId=user['key'])
        print("Delete response code: {}".format(response['ResponseMetadata']['HTTPStatusCode']))

    for user in not_used_over_3_months:
        print("User {} access key ID {} not used over 3 months, deleting now ...".format(user['name'], user['key']))
        response = iam.delete_access_key(UserName=user['name'], AccessKeyId=user['key'])
        print("Delete response code: {}".format(response['ResponseMetadata']['HTTPStatusCode']))
