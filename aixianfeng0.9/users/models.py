from django.db import models

# Create your models here.


class Main(models.Model):
    img = models.CharField(max_length=200) # 图片
    name = models.CharField(max_length=100) # 名称
    trackid = models.CharField(max_length=16) # 通用id

    class Meta:
        abstract = True        #抽象类


class MainWheel(Main):
    # 轮播banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


# 主要展示的商品
class MainShow(Main):
    categoryid = models.CharField(max_length=16) # 分类名称
    brandname = models.CharField(max_length=100) # 分类图片
    img1 = models.CharField(max_length=200)      # 图片1
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100) # 名称1
    price1 = models.FloatField(default=0)        # 优惠价格1
    marketprice1 =models.FloatField(default=1)   # 原始价格1
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 =models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 =models.FloatField(default=1)


    class Meta:
        db_table = 'axf_mainshow'


# 闪购 -- 左侧类型表
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)            # 类型id
    typename = models.CharField(max_length=100)         # 类型名称
    childtypenames = models.CharField(max_length=200)   # 子类型名称
    typesort = models.ImageField(default=1)             # 排序类型

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(max_length=16)         # 商品id
    productimg = models.CharField(max_length=200)       # 商品图片
    productname = models.CharField(max_length=100)      # 商品名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)        # 规格
    price = models.FloatField(default=0)                # 折后价
    marketprice = models.FloatField(default=1)          # 原价
    categoryid = models.CharField(max_length=16)        # 分类id
    childcid = models.CharField(max_length=16)          # 子分类id
    childcidname = models.CharField(max_length=100)     # 子分类id的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)          # 排序
    productnum = models.IntegerField(default=1)         # 销量排序

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True) # 用户名
    password = models.CharField(max_length=256)             # 密码
    email = models.CharField(max_length=64, unique=True)    # 邮箱
    # False 代表女
    sex = models.BooleanField(default=False)                # 性别
    icon = models.ImageField(upload_to='icons')             # 头像
    is_delete = models.BooleanField(default=False)          # 是否删除
    t_ticket = models.CharField(max_length=255)

    class Meta:
        db_table = 'axf_users'


# 购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)             # 关联用户
    goods = models.ForeignKey(Goods)                # 关联商品
    c_num = models.IntegerField(default=1)          # 商品个数
    is_select = models.BooleanField(default=True)   # 是否选择

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)             # 关联用户
    o_num = models.CharField(max_length=64, null=True)         # 订单编号
# 0 代表已下单, 但是未付款 , 1 已付款未发货  , 2 已付款 已发货
    o_status = models.IntegerField(default=0)       # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)            # 关联的商品
    order = models.ForeignKey(OrderModel)       # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品个数

    class Meta:
        db_table = 'axf_order_goods'