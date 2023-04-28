import json
import requests
from typing import Union

from core.models.intents import Intent


class ExecuteIntent:
    def __init__(self, auth: dict):
        self.auth = auth
        self.data: Union[dict, None] = None
        self.intent: Union[Intent, None] = None

        self.headers = self.set_headers()

    def execute_action(self, intent: Intent, data: dict) -> list[str, bool]:
        self.intent = intent
        self.data = data

        try:
            if self.intent.action_method == "POST":
                return self.execute_post()
            elif self.intent.action_method == "GET":
                return self.execute_get()
            elif self.intent.action_method == "PUT":
                return self.execute_put()
            elif self.intent.action_method == "DELETE":
                return self.execute_delete()
            else:
                raise ValueError("Action Method not was found")
        except ValueError:
            return [None, False]

    def execute_post(self) -> list[str, bool]:
        payload = {"data": self.data}
        res = requests.request(
            "POST", self.intent.action_url, json=payload, headers=self.headers
        )
        print(res)
        return [res.text, True]

    def execute_get(self) -> list[str, bool]:
        reservation_id = self.data.get("reservationId")
        res = requests.get(
            f"{self.intent.action_url}{reservation_id}", headers=self.headers
        )
        return [res.text, True]

    def execute_put(self) -> list[str, bool]:
        requests.put(
            self.intent.action_url, data=json.dumps(self.data), headers=self.headers
        )
        return ["", True]

    def execute_delete(self) -> list[str, bool]:
        requests.delete(self.intent.action_url, headers=self.headers)
        return ["", True]

    def set_headers(self) -> dict:
        if self.auth.get("type") == "Bearer":
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth.get('token')}",
            }

        return {}
