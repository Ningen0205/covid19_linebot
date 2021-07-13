from .models import infection, prefecture

def create_message_header():
    return infection.manager.latest_date_time()

def create_message_body(target):
    message = ''
    if prefecture.manager.check_region(target):
        # 地方なら
        region_data = prefecture.manager.get_region_data(target)
        infection_array = infection.manager.latest_region_prefecture_data(region_data)

        for i in infection_array:
            message += f'{i.prefecture.name}:{i.infection} \n'

    elif prefecture.manager.check_prefecture(target):
        # 都道府県なら
        prefecture_obj = prefecture.manager.get_prefecture_data(target)
        latest_infection_data = infection.manager.latest_prefecture_data(prefecture_obj=prefecture_obj)
        message += f'{latest_infection_data.prefecture.name}:{latest_infection_data.infection}'
    elif target == '全国':
        japan_infection_data = infection.manager.latest_prefecture_all_data()
        for i in japan_infection_data:
            message += f'{i.prefecture.name}:{i.infection} \n'
    
    else:
        message = '都道府県を正しく入力してください。'
    
    return message