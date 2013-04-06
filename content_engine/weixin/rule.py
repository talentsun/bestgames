# -*- coding: utf-8 -*-
from inspect import isfunction
import re
import random
import string

# 动作规则
# 执行流程: pattern -> handler -> register reply Rule
class Rule(object):
    def __init__(self, config, prex=None):
        if isinstance(config, (str, unicode)):
            #为字符串时，pattern为通过匹配，handler为直接返回该值
            self.name = config
            if prex is not None:
                self.name = prex + '_' + self.name
            self.description = u'发送任意字符，直接返回：' + config
            self.handler = config
        elif isfunction(config):
            #为函数时，pattern为通过匹配，handler为该函数
            self.name = config.name
            if prex is not None:
                self.name = prex + '_' + self.name
            self.description = config.description or '发送任意字符，直接执行函数并返回'
            self.handler = config
        elif isinstance(config, (list, tuple)):
            raise 'no support cfg type: list or tuple'
        elif isinstance(config, dict):
            # config = {
            #     name : 'name',
            #     description : 'description',
            #     pattern : 'pattern',
            #     handler : 'pattern'
            # }
            self.__dict__.update(config)
            self.name = config.get('name', None) or prex or config.get('pattern', None)

        if self.name is None:
            self.name = 'it_is_anonymous_rule'

    # 动作的名称，可选
    name = None

    # 动作的描述，可选
    description = None

    # 匹配规则，判断微信消息是否符合该规则
    # 支持的格式：
    # - {str}    直接返回字符串
    # - {RegExp}    仅匹配文本消息，正则式，把匹配赋值给info.query
    # - {function}    签名为fn(info):boolean
    # - {None}    为空则视为通过匹配
    pattern = None

    # 消息的处理逻辑

    # 当返回非真值{null/false}时继续执行下一个动作，否则回复给用户

    # 支持的格式：
    # - {str}    直接返回字符串
    # - {list}    直接返回数组中的随机子元素
    # - {function}    签名为fn(info, rule):str 直接执行函数并返回
    # - {function}    签名为fn(info, rule, callback(err, reply)) 通过回掉函数返回
    # - {dict}    key为pattern，value为handler，根据匹配的正则去执行对应的handler（主意：因为是dict，所以执行顺序不一定从上到下）
    handler = None

    # 后续动作配置

    # 指定下一次用户回复时要使用的动作

    # 支持的格式：
    # - 动作
    # - 动作数组
    replies = None

    @classmethod
    def convert(self, config, prex=None):
        if config and isinstance(config, Rule):
            return config

        result = []

        if isinstance(config, (str, unicode)):
            result.append(Rule(config))
        elif isfunction(config):
            result.append(Rule(config))
        elif isinstance(config, list):
            result = [Rule(item, prex) for item in config]
        elif isinstance(config, dict):
            if config.has_key('handler'):
                result.append(Rule(config))
            else:
                result = [Rule({ 
                    'pattern': key, 
                    'handler': item },
                    prex) for key,item in config.items()]
        return result

    @classmethod
    def is_match(self, info, rule):
        if rule and not isinstance(rule, Rule):
            rule = Rule(rule)
        p = rule.pattern

        if info is None:
            return False

        if p is None:
            return True

        if isfunction(p):
            return p(rule, info)

        if info.type == 'text' and info.text:
            regex = re.compile(p)
            if regex is not None:
                info.query = regex.match(info.text)
                return info.query is not None
            else:
                info.text.find(p) != -1

        return False

    @classmethod
    def execute(self, info, rule, cb):
        if rule and not isinstance(rule, Rule):
            rule = Rule(rule)

        fn = rule.handler
        if fn is None:
            return None

        if isinstance(fn, list) and len(fn) >= 1:
            fn = fn[random.randint(0, len(fn)-1)]

        if isinstance(fn, (str, unicode)):
            return fn

        if isfunction(fn):
                return fn(rule, info)

        return None
