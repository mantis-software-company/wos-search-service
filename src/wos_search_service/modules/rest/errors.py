from http import HTTPStatus

from .datamodels import BaseResponse
from .schemas import BaseResponse as BaseResponseSchema
from .views import rest_blueprint


@rest_blueprint.after_request
def wrap_error_request(response):
    if response.status_code >= 400:
        j = response.json
        kwargs = dict()
        if "message" in j:
            kwargs["message"] = j["message"]

        if "errors" in j:
            kwargs["exceptionDetail"] = j["errors"]

        if "code" in j:
            kwargs["statusCode"] = j["code"]

        if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
            kwargs["message"] = "Validation Error"

        _response = BaseResponse(**kwargs)
        _schema = BaseResponseSchema()
        _response = _schema.dumps(_response)
        response.set_data(_response)
        return response
    else:
        return response
