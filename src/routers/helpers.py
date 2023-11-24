def jsonify(payload, message="success", total=-1, status=200):
    """jsonify a payload"""

    n = -1 if not isinstance(payload, list) else len(payload)
    return {
        "payload": payload,
        "message": message,
        "status": status,
        "count": n,
        "total": total,
    }
