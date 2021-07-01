import random
import pymongo

from settings import DBuser, DBpass, DBurl
from datetime import datetime

from mailgun import email_auth_code

client = pymongo.MongoClient(f"mongodb+srv://{DBuser}:{DBpass}@{DBurl}")
db = client['ohsea']
registered = db['registered_users']
verification = db['pending_verifications']
edu_emails = db['edu_emails']
invites = db['pending_invites']


async def addVerification(user: dict):
    # generate random auth codes
    auth_code = None
    while True:
        auth_code = random.randint(100000, 999999)

        # break out if auth code isn't taken
        if not await authCodeTaken(auth_code):
            break

    # set auth code
    user['auth_code'] = auth_code
    # set timestamp
    user['created'] = datetime.now()
    # add to database
    verification.insert_one(user)

    # email user their auth code
    response = email_auth_code(auth_code, user['email'])


async def emailTaken(email: str):
    # search databases for that email
    search1 = verification.find_one({"email": email})
    search2 = registered.find_one({"email": email})
    # return bool if it was found or not
    return search1 is not None or search2 is not None


async def authCodeTaken(auth_code: int):
    # search database for that auth token
    search = verification.find_one({"auth_code": int(auth_code)})
    # return bool if it was found or not
    return search is not None


async def idTaken(id: int):
    # search database for that id
    search = registered.find_one({"_id": int(id)})
    # return bool if it was found or not
    return search is not None


async def verifyUser(id, auth_code):
    # search database for that user from auth token
    user = verification.find_one({"auth_code": int(auth_code)})
    # remove from verification database
    verification.delete_one({"auth_code": int(auth_code)})
    # remove auth code field
    user.pop('auth_code')
    # update timestamp
    user['created'] = datetime.now()
    # update _id to discord id
    user['_id'] = id
    # add default invited amount
    user['invited'] = 0
    # add to registered database
    registered.insert_one(user)

    # return name of person verified in the form (First L)
    return f"{user['first_name']} {user['last_name'][0]}"


async def isEDUEmail(email: str, address=False):
    # split address from email if not an address
    if not address:
        email = email.split('@')[1]
    # search the database for that email address
    search = edu_emails.find_one({'address': email})
    return search is not None


async def addEDUEmail(address: str):
    edu_emails.insert_one({'address': address})


async def getUserFromId(user_id: int):
    # must only run if you know the user id exists
    return registered.find_one({'_id': user_id})


async def newInvite(user_id: int, inviter_id: int):
    invites.insert_one({'_id': user_id, 'inviter': inviter_id})


async def removeInvite(user_id: int):
    invites.delete_one({'_id': user_id})


async def wasInvited(user_id: int):
    # search database for that id
    search = invites.find_one({"_id": user_id})
    # return bool if it was found or not
    return search is not None


async def useInvite(user_id: int):
    # search database for that id
    search = invites.find_one({"_id": user_id})
    if search is None:
        return
    else:
        registered.update_one({'_id': search['inviter']},
                              {'$inc': {'invited': 1}},
                              upsert=False)
