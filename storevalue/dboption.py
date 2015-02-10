#coding:utf8
__author__ = 'qitian'
# from libs import web
from core.modules.module_handle import api_handle
from core.auth import auth_base
from models.crm.g_storevalue import StoreValue
from models.crm.g_storevalueconfig import StoreValueConfig
from models.crm.g_storevaluepresent import StoreValuePresent

def update_store_present(hotel_group_code,  store_value_type,add_store_value_type, add_store_value,
                         usetype,hotelcode, add_store_value_crebit_type=None, guestfileID=None,
                         agreementID=None,usebustype=None, use_bus_code=None, use_store_value=None,remark=None,**kwargs):
    #更改g_storevalue表
    store = StoreValue()
    #TODO:完善这个函数功能，使之可复用，参数太多了，实用性不高

def get_store_present(*args, **kwargs):
    pass
    #TODO:获取储值及赠送值



def update_store_config(hotel_group_code,cfgname, present_type, rule, valid_day):
    '''
    更新储值配置信息
    :param hotel_group_code:
    :param cfgname:
    :param present_type:
    :param rule: rule必须是一个字典,key是对应的stoveValue, value就是赠送的钱数,如果赠送类型是key默认为1
    :return:
    '''
    #删除先前对应的数据
    StoreValueConfig().query.filter(StoreValueConfig.HotelGroupCode == hotel_group_code)\
        .filter(StoreValueConfig.PresentType == present_type).delete()

    #将其它类型的配置设置为不可用状态
    other_config = StoreValueConfig().query.filter(StoreValueConfig.HotelGroupCode == hotel_group_code)\
        .filter(StoreValueConfig.PresentType != present_type).all()
    for v in other_config:
        v.UseFlag = 0


    if not isinstance(rule, dict):
        raise ValueError, 'rule must be a dict object'

    for key in rule.keys():
        config = StoreValueConfig()
        config.HotelGroupCode = hotel_group_code
        config.CfgName = cfgname
        config.PresentType = present_type
        config.AddStoreValue = int(key)
        config.PresentStoreValue = int(rule[key])
        config.ValidDay = valid_day
        config.save()


if __name__ == '__main__':

    pass
