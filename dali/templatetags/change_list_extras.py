from django.contrib.admin.templatetags.admin_list import result_list
from django.template import Library

register = Library()

def extra_result_list(cl):
    return result_list(cl)
    
register.inclusion_tag("admin/dali/Picture/change_list_results.html")(extra_result_list)

    

