from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint

from .business import search_author
from .schemas import AuthorSearchResponseSchema, AuthorSearchRequestSchema

rest_blueprint = Blueprint("Author Search", "author_search", url_prefix="/api/v1/wos/author",
                           description="Wos Author Search")


@rest_blueprint.route("/search")
class AuthorSearchCollection(MethodView):
    @rest_blueprint.arguments(AuthorSearchRequestSchema, location="json")
    @rest_blueprint.response(HTTPStatus.OK, AuthorSearchResponseSchema)
    def post(self, args):
        return search_author(author_name=args.get("name"), page=args.get("page"))