from rest_framework import serializers

from users.models import OrderGoodsModel,Goods


class OrderGoodsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderGoodsModel
        fields = ['id', 'goods_num', 'goods_id', 'order_id']


    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['productid'] = instance.goods.productid
        data['productimg'] = instance.goods.productimg
        data['productlongname'] = instance.goods.productlongname
        data['price'] = instance.goods.price
        data['o_num'] = instance.ordermodel.o_num
        data['o_status'] = instance.ordermodel.o_status
        data['user_id'] = instance.usermodel.id
        data['user_username'] = instance.usermodel.username
        return data
# class GoodsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Goods
#         fileds = ['id', 'productid', 'productimg', 'productlongname', 'specifics', 'price', 'marketprice']
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#
#         return data