#coding=utf-8

import hmac

def get_signature(key, content):
    return hmac.new(key, content).hexdigest()