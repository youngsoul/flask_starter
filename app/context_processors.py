
from flask import request

def is_active_link(link_names):
    current_url_rule = request.url_rule.rule
    if current_url_rule in link_names:
        return "active"
    else:
        return ""

