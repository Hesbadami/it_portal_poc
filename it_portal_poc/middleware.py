from django.shortcuts import redirect
from user.models import get_user_by_id, get_company_by_user_id
from django.urls import resolve
import json
import re
from django.shortcuts import render

def authenticate(get_response):
    # One-time configuration and initialization.

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.debug_helper['name'] = view_func.__name__
        self.debug_helper['module'] = view_func.__module__
        self.debug_helper['message'] = '"{0}" view caused an error in module "{1}"'.format(
            view_func.__name__, view_func.__module__
        )

    def middleware(request):
        
        data = {}
        user_id = request.session.get('user_id')
        user = get_user_by_id(user_id)
        company = get_company_by_user_id(user_id)
        try:
            request.META['current_user'] = user[0]
            try:
                request.META['current_company'] = company[0]
            except IndexError as e:
                request.META['current_company'] = "ProjektRising"
            #if ([i for i in request.path.split("/") if i or i==0][0]) != "user":
                #if ".".join([i for i in request.path.split("/") if i or i==0][:2]) not in request.META['current_user']['permissions']:
                    #re.findall(r'manage/users/*', "/".join([i for i in request.path.split("/") if i or i==0][:3]))
                    #re.match('manage/users/[0-9]/[0-9]', 'manage/users/1/54')
                    #return redirect('/user/login')
                #    pass
            if ([i for i in request.path.split("/") if i or i==0][0]) not in ["user", "dashboard"]:
                if request.META['current_user']['permissions']:
                    user_permissions = json.loads(request.META['current_user']['permissions'])
                    if len(user_permissions):
                        for user_permission in user_permissions:
                            if(re.match(user_permission, "/".join([i for i in request.path.split("/") if i or i==0][:3]))):
                                permission = True
                                break
                            else:   
                                permission = False
                    else:
                        permission = False
                        
                else:
                    permission = False
                    
                superadmins = [1, 15, 16]
                if not permission and request.META['current_user']['user_id'] not in superadmins:
                
                    return render(request, '403.html', data)
                    
        except IndexError as e:
            print(e)
            if request.path != "/user/login/":
                return redirect('/user/login/')
        
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
            
        return response

    return middleware