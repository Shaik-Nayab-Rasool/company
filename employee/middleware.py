class MyMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        print('Hi iam Middleware')

    def __call__(self,req):
        print('Before View')
        response = self.get_response(req)
        print('After View')
        return response