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
from apps.crm.member.storevalue.dboption import update_store_config


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
            try:
                input = web.input()
                hotel_group = web.ctx.session.login_hotel_info['Group']
                present_type = input.get('present_type')
                cfgname = input.get('cfgname')
                rule = json_to_obj(web.input().get('rule'))
                valid_day = input.get('valid_day')
            except KeyError, e:
                raise KeyError, 'Config StoreValueConfig failed!KeyError:%s'%e

            update_store_config(hotel_group, cfgname, present_type, rule, valid_day)
            return FuncResult(success=True, value='ok')
        except Exception, e:
            return FuncResult(fail=u'添加储值配置失败%s'%e)


