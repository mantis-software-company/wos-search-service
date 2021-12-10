# wos-search-service

WOS Search Service is a RESTful web service that provides access to the Web of Science (WOS) citation data.
It use Web of Science SOAP API to access WOS data. You need premium API account in order use this service.

Mantis Software Company has no relation with Thomson Reuters, Web of Science and Web of Science WWS API. 
This web service is just a wrapper, was built top on [wos python package](https://github.com/enricobacis/wos).
See [this section](https://github.com/enricobacis/wos#faq-i-cannot-connect-) for more information.

Currently , the service supports the following WOS search queries:
- Author search (with combinations of author name)


## Environment Variables
- `__SERVICE_WOS_USER`: Username to access WOS SOAP API
- `__SERVICE_WOS_PASSWORD`: Password to access WOS SOAP API

