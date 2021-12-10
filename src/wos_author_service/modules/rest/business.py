import logging
import traceback
from http import HTTPStatus

import suds
from flask import current_app
from flask_smorest import abort
from lxml import etree

from .datamodels import Author, Publication, BaseResponse, Citation, Pagination
from .utils import author_name_to_query, CustomWosClient

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)


def _refresh_sid():
    try:
        with CustomWosClient(user=current_app.config.get("WOS_USER"), password=current_app.config.get("WOS_PASSWORD")) as client:
            current_app.config["WOS_SID"] = client.connect()
    except suds.WebFault as e:
        if "Request denied by Throttle server" in e.fault.faultstring:
            log.warning("Request denied by Throttle server.")
            current_app.config["WOS_SID"] = None
            abort(HTTPStatus.TOO_MANY_REQUESTS, message="Request denied by Throttle server.")
        else:
            log.error(e.fault.faultstring)
            abort(HTTPStatus.BAD_REQUEST, message="Error when processing request.", messages=e.fault.faultstring)


def _search_author(author_name, query, page, _sid):
    with CustomWosClient(SID=_sid) as client:
        search_results = client.search(query, count=10, offset=((page - 1) * 10 + 1))
        if search_results.recordsFound % 10 == 0:
            total_pages = search_results.recordsFound // 10
        else:
            total_pages = (search_results.recordsFound // 10) + 1

        ns = {'wos': 'http://scientific.thomsonreuters.com/schema/wok5.4/public/FullRecord'}
        root = etree.fromstring(str(search_results.records))
        records = root.xpath('//wos:REC', namespaces=ns)
        publications = []
        for i in range(len(records)):
            wos_id = root.xpath(f'//wos:REC[{i + 1}]/wos:UID', namespaces=ns)[0].text
            title = root.xpath(f'//wos:REC[{i + 1}]//wos:title[@type="item"]', namespaces=ns)[0].text
            authors = root.xpath(
                f'//wos:REC[{i + 1}]/wos:static_data/wos:summary/wos:names/wos:name[@role="author"]/wos:full_name/text()',
                namespaces=ns
            )
            publication_source = root.xpath(f'//wos:REC[{i + 1}]//wos:titles/wos:title[@type="source"]', namespaces=ns)[0].text
            year = root.xpath(f'//wos:REC[{i + 1}]//wos:pub_info/@pubyear', namespaces=ns)[0]
            try:
                volume = root.xpath(f'//wos:REC[{i + 1}]//wos:pub_info/@vol', namespaces=ns)[0]
            except IndexError:
                volume = None

            try:
                issue = root.xpath(f'//REC[{i + 1}]//pub_info/@issue')[0]
            except IndexError:
                issue = None

            citing_articles = []
            citing_articles_offset = 1
            while True:
                citing_articles_result = client.citingArticles(uid=wos_id, offset=citing_articles_offset, count=100)
                citing_articles_root = etree.fromstring(str(citing_articles_result.records))
                citing_articles_records = citing_articles_root.xpath('//wos:REC', namespaces=ns)
                if len(citing_articles_records) == 0:
                    break
                else:
                    for j in range(len(citing_articles_records)):
                        citing_article_wos_id = citing_articles_root.xpath(f'//wos:REC[{j + 1}]/wos:UID', namespaces=ns)[0].text
                        citing_article_year = citing_articles_root.xpath(f'//wos:REC[{j + 1}]//wos:pub_info/@pubyear', namespaces=ns)[0]
                        citing_articles.append(Citation(citation_wos_id=citing_article_wos_id, citation_year=citing_article_year))
                citing_articles_offset += 100

            publication = Publication(
                wos_id=wos_id,
                title=title,
                authors=authors,
                publication_source=publication_source,
                year=year,
                volume=volume,
                issue=issue,
                citations=citing_articles
            )
            publications.append(publication)

        author = Author(author_name=author_name, publications=publications)

        return BaseResponse(
            statusCode=200,
            message="Success",
            data=author,
            exceptionDetail=None,
            page=Pagination(
                page=page,
                totalPages=total_pages
            )
        )


def search_author(author_name, page=1):
    if current_app.config.get("WOS_SID") is None:
        _refresh_sid()
        _sid = current_app.config.get("WOS_SID")
    else:
        _sid = current_app.config.get("WOS_SID")
    query = author_name_to_query(author_name)
    try:
        return _search_author(author_name, query, page, _sid)
    except suds.WebFault as e:
        if "Session not found" in e.fault.faultstring:
            _refresh_sid()
            return search_author(author_name, page)
        elif "Request denied by Throttle server" in e.fault.faultstring:
            log.warning("Request denied by Throttle server.")
            current_app.config["WOS_SID"] = None
            abort(HTTPStatus.TOO_MANY_REQUESTS, message="Sorgu isteği aşıldı, lütfen 5 dakika sonra tekrar deneyiniz.")
        else:
            abort(HTTPStatus.BAD_REQUEST, message="Sorgunuz işlenirken hata oluştu.", messages=e.fault.faultstring)
    except Exception:
        tb = traceback.format_exc()
        abort(HTTPStatus.BAD_REQUEST, message="Sorgunuz işlenirken hata oluştu.", messages=tb)
