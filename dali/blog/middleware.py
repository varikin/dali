class SetRemoteAddrFromForwardedFor(object):
    """
    Sets the remote address in the request correctly from
    HTTP_X_FORWARDED_FOR header.
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip

