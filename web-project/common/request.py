class Pageable:
    size = 5
    page = 1
    count = 0
    
    def __init__(self, request, size = 5, page = 1):
        self.size = size
        self.page = page
        try:
            self.size = int(request.GET.dict().pop('page.size'));
            self.page = int(request.GET.dict().pop('page.page'));
        except:
            pass
