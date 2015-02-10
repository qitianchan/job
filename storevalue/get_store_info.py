#coding: utf8
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

            guest_file_ID = input.get('guest_file_id')
        #TODO:返回储值信息

        except Exception, e:
            return FuncResult(fail=u'获取储值信息失败%s'%e)