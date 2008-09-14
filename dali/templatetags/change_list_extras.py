from django.contrib.admin.templatetags.admin_list import result_list
from django.template import Library

register = Library()

def extra_result_list(cl):
    results = result_list(cl)
    position = {};
    
    for index, header in enumerate(results['result_headers']):
        if header['text'] == "order":
            position['order'] = index    
        elif header['text'] == "gallery":
            position['gallery'] = index
        elif header['text'] == 'name':
            position['name'] = index
            
    results['position'] = position;
    return results

register.inclusion_tag("admin/dali/Picture/change_list_results.html")(extra_result_list)

    

