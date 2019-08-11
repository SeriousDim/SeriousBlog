from flask import current_app

def add_index(index, model):
    if not current_app.elastic_search:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elastic_search.index( \
        index = index, doc_type = index, id = model.id, body = payload)

def remove_index(index, model):
    if not current_app.elastic_search:
        return
    current_app.elastic_search.delete( \
        index=index, doc_type=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elastic_search:
        return [], 0
    res = current_app.elastic_search.search( \
        index=index,
        body={'query':
                  {'multi_match':
                       {'query': query,
                        'fields': ['*']
                        }
                   },
              'from': (page - 1) * per_page,
              'size': per_page
        })
    ids = [int(hit['_id']) for hit in res['hits']['hits']]
    return ids, res['hits']['total']['value']