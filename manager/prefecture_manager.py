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

    def __create_arrays(self, index_arrays):
        result = []

        for i in index_arrays:
            prefecture = super().get_queryset().filter(id=i).get()
            result.append(prefecture)

        return result
    
    def hokkaido(self):
        return self.__create_arrays(self.INDEX_HOKKAIDO)
    
    def tohoku(self):
        return self.__create_arrays(self.INDEX_TOHOKU)
    
    def kanto(self):
        return self.__create_arrays(self.INDEX_KANTO)
    
    def chubu(self):
        return self.__create_arrays(self.INDEX_CHUBU)
    
    def kinki(self):
        return self.__create_arrays(self.INDEX_KINKI)
    
    def shikoku(self):
        return self.__create_arrays(self.INDEX_SHIKOKU)
    
    def kyushu(self):
        return self.__create_arrays(self.INDEX_KYUSHU)

    def okinawa(self):
        return self.__create_arrays(self.INDEX_OKINAWA)
    
    def get_region_data(self, region_name):
        if self.check_region(region_name):
            if region_name == '北海道':
                return self.hokkaido()
            elif region_name == '東北':
                return self.tohoku()
            elif region_name == '関東':
                return self.kanto()
            elif region_name == '中部':
                return self.chubu()
            elif region_name == '近畿':
                return self.kinki()
            elif region_name == '四国':
                return self.shikoku()
            elif region_name == '九州':
                return self.kyushu()
            elif region_name == '沖縄':
                return self.okinawa()
        else:
            return False
    
    def get_prefecture_data(self, prefecture_name):
        return super().get_queryset().filter(name=prefecture_name).first()
    
    def check_region(self, region_name):
        return region_name in {'北海道','東北','関東','中部','近畿','四国','九州','沖縄'}
    
    def check_prefecture(self, prefecture_name):
        return bool(super().get_queryset().filter(name=prefecture_name).first())