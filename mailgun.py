import requests
from settings import mailgun_API_key, mailgun_base_URL


def email_auth_code(auth_code: int, email: str):
    return requests.post(
        mailgun_base_URL,
        auth=("api", mailgun_API_key),
        data={"from": "OHSEA Verification <mailgun@verification.ohsea.gg>",
              "to": [email],
              "subject": f"OHSEA Verification Code: {auth_code}",
              "template": "discord-verification",
              "v:auth_code": auth_code,
              })
