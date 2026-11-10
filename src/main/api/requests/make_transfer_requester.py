from http import HTTPStatus

import requests

from src.main.api.models.make_transfer_request import MakeTransferRequest
from src.main.api.models.maker_transfer_response import MakeTransferResponse
from src.main.api.requests.requester import Requester
from h11 import Response


class MakeTransferRequester(Requester):
    def post(self, make_transfer_request: MakeTransferRequest) -> MakeTransferResponse | Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=make_transfer_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return MakeTransferResponse(**response.json())
        return response
