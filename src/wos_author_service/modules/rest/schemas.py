from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    page = fields.Integer()
    totalPages = fields.Integer()


class BaseResponse(Schema):
    data = fields.Dict()
    message = fields.String()
    statusCode = fields.String()
    exceptionDetail = fields.String()
    page = fields.Nested(PaginationSchema)

    class Meta:
        ordered = True


class AuthorSchema(Schema):
    author_name = fields.Str()
    publications = fields.Nested('PublicationSchema', many=True)


class PublicationSchema(Schema):
    wos_id = fields.Str()
    title = fields.Str()
    authors = fields.List(fields.Str())
    publication_source = fields.Str()
    year = fields.Int()
    volume = fields.Str()
    issue = fields.Str()
    citations = fields.Nested('CitationSchema', many=True)


class CitationSchema(Schema):
    citation_wos_id = fields.Str()
    citation_year = fields.Int()


class AuthorSearchResponseSchema(BaseResponse):
    data = fields.Nested(AuthorSchema)


class AuthorSearchRequestSchema(Schema):
    name = fields.Str(required=True)
    page = fields.Int(required=True, validate=validate.Range(min=1))
