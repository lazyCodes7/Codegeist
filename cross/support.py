def cross_origin(origin="*"):
    def cross_origin(func):
        @functools.wraps(func)
        def _decoration(*args, **kwargs):
            ret = func(*args, **kwargs)
            _cross_origin_header = {"Access-Control-Allow-Origin": origin,
                                    "Access-Control-Allow-Headers":
                                        "Origin, X-Requested-With, Content-Type, Accept"}
            if isinstance(ret, tuple):
                if len(ret) == 2 and isinstance(ret[0], dict) and isinstance(ret[1], int):
                    # this is for handle response like: ```{'status': 1, "data":"ok"}, 200```
                    return ret[0], ret[1], _cross_origin_header
                elif isinstance(ret, basestring):
                    response = make_response(ret)
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return response
                elif isinstance(ret, Response):
                    ret.headers["Access-Control-Allow-Origin"] = origin
                    ret.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return ret
                else:
                    raise ValueError("Cannot handle cross origin, because the return value is not matched!")
            return ret

        return _decoration

    return cross_origin