from util.paths.error_404 import error_404
class Router:

    def __init__(self):
        self.route_list = []

    def add_route(self, method, path, action, exact_path=False):
        self.route_list.append(Route(method, path, action, exact_path))

    def route_request(self, request, handler):
        if ".." in request.path:
            error_404(request, handler)
        for r in self.route_list:
             if r.exact_path:
                if r.path == request.path and r.method == request.method:
                    r.action(request, handler)
                    return
             else:
                if request.path.startswith(r.path) and r.method == request.method:
                    r.action(request, handler)
                    return
        error_404(request, handler)
                

class Route:
        def __init__(self, method, path, action, exact_path) -> None:
             self.method = method
             self.path = path
             self.action = action
             self.exact_path = exact_path