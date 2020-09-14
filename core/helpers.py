class ResponseHelper:
    @staticmethod
    def add_error_code(response, error_code):
        response.data['error_code'] = error_code
        return response


class RequestInfoHelper:
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_user_agent_info(request):
        agent = ''
        if hasattr(request, 'META'):
            agent = request.META.get('HTTP_USER_AGENT', '')
        return agent
