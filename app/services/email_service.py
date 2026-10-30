import httpx

from app.exceptions.email_exception import EmailException


class EmailService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def send_login_mail(self, recipient: str):
        payload = {
            "Messages": [
                {
                    "From": {
                        "Email": "visowmani.123@gmail.com",
                        "Name": "Student Management API",
                    },
                    "To": [
                        {
                            "Email": recipient,
                        }
                    ],
                    "Subject": "Login Successful",
                    "HTMLPart": """
                <h1>Welcome!</h1>
                <p>You have successfully logged in.</p>
            """,
                }
            ]
        }
        try:
            response = await self.client.post(
                "https://api.mailjet.com/v3.1/send", json=payload
            )

            response.raise_for_status()
        except httpx.TimeoutException as error:
            raise EmailException(f"Timeout Error in MailJet Email Service : {error}")

        except httpx.HTTPStatusError as error:
            raise EmailException(
                f"Timeout Error in MailJet Email Service : Status Code - {error.response.status_code} : Text {error.response.text}"
            )
