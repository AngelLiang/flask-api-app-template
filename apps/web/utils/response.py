# coding=utf-8

from flask import request, jsonify


class ResponseJson(object):

    def __new__(cls, data=None, links=None, pagination=None, *args, **kw):
        response_dict = {}
        if data:
            response_dict['data'] = data
        if links:
            response_dict['links'] = links
        if pagination:
            response_dict['pagination'] = pagination
        response_dict['self'] = request.base_url
        response_dict.update(kw)
        return jsonify(response_dict)
