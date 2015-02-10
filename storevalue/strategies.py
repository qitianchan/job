#coding:utf8
__author__ = 'qitian'

import datetime

strategies = {}

class StoreValueStrategy(object):
    """An adaptor that processes input arguments and produces an Store.

    Provides a ``set_store_value`` method that receives input arguments and
    produces an instance of base.Engine or a subclass.

    """

    def __init__(self):
        strategies[self.name] = self

    def set_store_value(self, *args, **kwargs):
        """Given arguments, returns a new Store instance."""

        raise NotImplementedError()


class DefaulteStrategy(StoreValueStrategy):

    name = 'fixed'

    def set_store_value(self, store_value, rule, valid_day=365, **kwargs):
        '''
        根据充值的钱数按照赠送规则返回赠送金额及赠送金额过期时间
        :param store_value: 充值金额
        :param rule: 对应规则,是一个dict
        :param out_date:失效时间,以天为单位,默认为一年
        :param kwargs:
        :return: 返回赠送的接额和过期的时间,该时间为一个datatime

        '''
        if not isinstance(rule, dict):
            raise ValueError, u'rule必须是一个dict'
        rule_keys = rule.keys()

        keys = []
        for key in rule_keys:
            if not str(key).isdigit():
                rule.pop(key)
            else:
                keys.append(int(key))

        rule_keys = sorted(keys, reverse=True)

        present = 0
        for v in range(len(rule_keys)):
            times = store_value / rule_keys[v]

            if times:
                present += rule.get(str(rule_keys[v]), rule_keys[v]) * times
                store_value %= rule_keys[v]

        #过期日期
        out_date = datetime.date.today() + datetime.timedelta(days=valid_day)

        return present, out_date

DefaulteStrategy()


class RatioStragety(StoreValueStrategy):

    name = 'ratio'

    def set_store_value(self,store, rule, valid_day=365, **kwargs):
        '''

        :param store:
        :param retio:
        :param valid_day:
        :param kwargs:
        :return:
        '''
        key = rule.keys()[0]
        present = store * rule[key]
        valid_day = datetime.date.today() + datetime.timedelta(days=valid_day)

        return present, valid_day

RatioStragety()



if __name__ == '__main__':
    rule = {'100':100, '200':50, 25:5, 'sdfs':6000}

    print '-------------------------------------------'
    store = DefaulteStrategy()
    present, date = store.set_store_value(576,rule)
    print present, date
    print '--------------------------------------------'

    print strategies.get('ratio').set_store_value(1001, 0.23)
