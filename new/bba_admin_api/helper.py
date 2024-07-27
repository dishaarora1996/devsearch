


def custom_filters(request, search:dict, excludes:list):
    valid_filters = ['id', 'all', 'page_size', 'page', 'order_by']
    valid_filters = valid_filters+excludes
    print(valid_filters)
    for filter_name, filter_value in request.query_params.items():
        if filter_name not in valid_filters and filter_value:
            temp_val = filter_value
            if filter_name.endswith('__in'):
                temp_val = filter_value.split(',')
            if filter_name.endswith('__isnull'):
                temp_val = True if temp_val == 'true' else False
            search[f'{filter_name}'] = temp_val
    print(request.query_params)
    print(search)
    print("*"*10)
    return search
