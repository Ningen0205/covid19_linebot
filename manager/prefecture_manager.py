from django.db import models

class prefecture_manager(models.Manager):

    INDEX_HOKKAIDO = [1]
    INDEX_TOHOKU = [2,3,4,5,6,7]
    INDEX_KANTO = [8,9,10,11,12,13,14]
    INDEX_CHUBU = [15,16,17,18,19,20,21,22,23]
    INDEX_KINKI = [24,25,26,27,28,29,30]
    INDEX_CHUGOKU = [31,32,33,34,35]
    INDEX_SHIKOKU = [36,37,38,39]
    INDEX_KYUSHU = [40,41,42,43,44,45,46]
    INDEX_OKINAWA = [47]

    REGION_OBJ = {
        '東北地方': INDEX_TOHOKU,
        '関東地方': INDEX_KANTO,
        '中部地方': INDEX_CHUBU,
        '近畿地方': INDEX_KINKI,
        '中国地方': INDEX_CHUGOKU,
        '四国地方': INDEX_SHIKOKU,
        '九州地方・沖縄': INDEX_KYUSHU + INDEX_OKINAWA
    }

    def __create_arrays(self, index_arrays):
        result = []

        for i in index_arrays:
            prefecture = super().get_queryset().filter(id=i).get()
            result.append(prefecture)

        return result
    
    def get_region_data(self, region_name):
        if self.check_region(region_name):
            return self.__create_arrays(self.REGION_OBJ[region_name])
        else:
            return False
    
    def get_prefecture_data(self, prefecture_name):
        return super().get_queryset().filter(name=prefecture_name).first()
    
    def check_region(self, region_name):
        return region_name in self.REGION_OBJ
    
    def check_prefecture(self, prefecture_name):
        return bool(super().get_queryset().filter(name=prefecture_name).first())