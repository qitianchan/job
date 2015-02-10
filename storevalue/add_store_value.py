# coding: utf-8
__author__ = 'qitian'

from libs import web
from core.modules.module_handle import api_handle
from core.auth import auth_base
from libs.orm.ormutils import dbtranscoped
from utils.func_api import FuncResult
from core.log.logging_trace import log_trace
from utils.tools import json_to_obj
from models.crm.g_storevalue import StoreValue
from models.crm.g_storevalueconfig import StoreValueConfig
from models.crm.g_storevaluepresent import StoreValuePresent
from datetime import datetime
from apps.crm.member.storevalue.strategies import strategies

ADD_STORE = 1
default_strategy = 'fixed'

class handler(object):
    @auth_base()
    @api_handle(db=True)
    def GET(self):
        log_trace()
        if web.config.debug:
            return self.data_handle()

    @auth_base()
    @api_handle(db=True)
    def POST(self):
        log_trace()
        return self.data_handle()

    @dbtranscoped()
    def data_handle(self):
        try:
            input = web.input()
            group = web.ctx.session.login_hotel_info['Group']
            if not group:
                return FuncResult(fail=u'酒店编码获取错误')
            try:
                add_store_value_info = json_to_obj(input.pop('add_store_value_info'))
                guest_file_ID = add_store_value_info.pop('guest_file_id',None)
                agreement_ID = add_store_value_info.pop('agereement_id',None)
                if not (guest_file_ID or agreement_ID):
                    return FuncResult(fail=u'至少需要一个客历ID或者一个协议ID')

                add_store_value_type = add_store_value_info.pop('add_store_value_type')
                add_store_value = add_store_value_info.pop('add_store_value')
                add_store_value_credits_type = add_store_value_info.pop('add_store_value_credits_type',None)
                remark = add_store_value_info.pop('remark', None)

            except Exception, e:
                raise Exception, u'获取充值信息不正确%s'%e


            create_time = datetime.today()

            store_value = StoreValue()
            store_value.HotelGroupCode = group
            store_value.GuestFileID = guest_file_ID
            store_value.AgreementID = agreement_ID
            store_value.CreateTime = create_time
            store_value.StoreValueType = ADD_STORE   #1存入储值，2:使用储值
            store_value.AddStoreValueType = add_store_value_type
            store_value.AddStoreValue = add_store_value
            store_value.AddStoreValueCrebitType = add_store_value_credits_type
            store_value.Remark = remark
            store_value.save(True)

            #增加充值赠送记录
            store_config = StoreValueConfig().query.filter(StoreValueConfig.HotelGroupCode==group)\
                            .filter(StoreValueConfig.UseFlag == 1).all()

            if not store_config:
                return FuncResult(fail=u'冲值失败，请先在后台会员设置那里配置储值规则')

            valid_day = store_config[0].ValidDay
            cfgname = store_config[0].CfgName
            rule = {}
            for it in store_config:
                rule[it.AddStoreValue] = it.PresentStoreValue

            #获取present值及out_date
            present, out_date = strategies.get(cfgname, strategies.get(default_strategy)).set_store_value(store_value, rule,valid_day)

            leaving_store_value = StoreValuePresent().query.filter(StoreValuePresent.HotelGroupCode) \
                .filter(StoreValuePresent.GuestFileID == guest_file_ID) \
                .filter(StoreValuePresent.OutDate <= create_time).all()
            leaving_value = 0
            for data in leaving_store_value:
                leaving_value += (data.AddPresentValue - data.UseStoreValue)

            store_value_present = StoreValuePresent()

            store_value_present.HotelGroupCode = group
            store_value_present.StoreValueID = store_value.StoreValueID
            store_value_present.GuestFileID = guest_file_ID
            store_value_present.AgreementID = agreement_ID
            store_value_present.AddPresentValue = present
            store_value_present.CreateTime = create_time
            store_value_present.OutDate = out_date
            store_value_present.LeavingStoreValue = leaving_value
            store_value_present.Remark = remark

            store_value_present.save()

            return FuncResult(success=True)
        except Exception, e:
            return FuncResult(fail=u'添加储值失败%s'%e)



if __name__ == '__main__':
    pass