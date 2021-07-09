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
