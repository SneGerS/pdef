
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xb6b\x15L\xa6Gc\x91\x12?^\x9f\x05bv\xfb'
    
_lr_action_items = {'INHERITS':([23,28,30,44,],[-2,-38,39,-37,]),'ON':([53,],[64,]),'STRING':([59,64,],[67,71,]),'LBRACE':([20,21,23,27,28,30,40,41,44,54,55,70,84,],[-2,29,-2,35,-38,-2,-2,-29,-37,66,-31,-28,-30,]),'POLYMORPHIC':([23,28,30,40,41,44,70,],[-2,-38,-2,53,-29,-37,-28,]),'SEMI':([4,19,31,36,37,38,51,61,67,77,82,],[9,25,42,-25,-26,49,-10,-24,76,-9,85,]),'LESS':([20,23,51,],[26,26,62,]),'RBRACE':([35,45,47,48,49,58,66,72,73,75,76,81,85,],[-2,57,-20,-21,60,-19,-2,80,-34,-35,-22,-33,-36,]),'ENUM':([3,5,7,8,9,10,12,14,15,16,17,22,25,42,57,60,65,80,],[-2,13,-5,-6,-3,-17,-16,-4,-14,-15,13,-13,-8,-7,-18,-23,-27,-32,]),'MODULE':([0,],[1,]),'NATIVE':([3,5,7,8,9,10,12,14,15,16,17,22,25,42,57,60,65,80,],[-2,11,-5,-6,-3,-17,-16,-4,-14,-15,11,-13,-8,-7,-18,-23,-27,-32,]),'AS':([19,51,52,71,77,],[24,-10,63,79,-9,]),'COLON':([46,],[59,]),'COMMA':([32,33,34,36,37,38,51,56,61,68,69,77,83,],[-40,-41,43,-25,-26,50,-10,-39,-24,-12,78,-9,-11,]),'GREATER':([32,33,34,51,56,68,69,77,83,],[-40,-41,44,-10,-39,-12,77,-9,-11,]),'IMPORT':([3,5,7,8,9,14,25,42,],[6,6,-5,-6,-3,-4,-8,-7,]),'MESSAGE':([3,5,7,8,9,10,12,14,15,16,17,22,25,42,57,60,65,80,],[-2,18,-5,-6,-3,-17,-16,-4,-14,-15,18,-13,-8,-7,-18,-23,-27,-32,]),'IDENTIFIER':([1,6,11,13,18,24,26,29,35,39,43,45,47,48,50,58,62,63,66,72,73,74,75,76,78,79,81,85,],[4,19,20,21,23,31,33,37,46,51,33,46,-20,-21,37,-19,51,70,74,74,-34,51,-35,-22,51,84,-33,-36,]),'$end':([2,10,12,15,16,17,22,57,60,65,80,],[0,-17,-16,-14,-15,-1,-13,-18,-23,-27,-32,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'message_body':([54,],[65,]),'imports':([3,],[5,]),'variables':([20,23,],[27,30,]),'module':([0,],[2,]),'message':([5,17,],[10,10,]),'native':([5,17,],[16,16,]),'native_option':([35,45,],[47,58,]),'field':([66,72,],[73,81,]),'import':([3,5,],[7,14,]),'type':([39,62,74,78,],[52,68,82,83,]),'variable_list':([26,],[34,]),'enum_value':([29,50,],[36,61,]),'native_options':([35,],[45,]),'enum':([5,17,],[12,12,]),'module_name':([0,],[3,]),'variable':([26,43,],[32,56,]),'types':([62,],[69,]),'enum_values':([29,],[38,]),'definition':([5,17,],[15,22,]),'fields':([66,],[72,]),'message_base':([30,],[40,]),'empty':([3,20,23,30,35,40,66,],[8,28,28,41,48,55,75,]),'definitions':([5,],[17,]),'message_type':([40,],[54,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> module","S'",1,None,None,None),
  ('module -> module_name imports definitions','module',3,'p_module','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',74),
  ('empty -> <empty>','empty',0,'p_empty','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',84),
  ('module_name -> MODULE IDENTIFIER SEMI','module_name',3,'p_module_name','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',91),
  ('imports -> imports import','imports',2,'p_imports','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',98),
  ('imports -> import','imports',1,'p_imports','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',99),
  ('imports -> empty','imports',1,'p_imports','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',100),
  ('import -> IMPORT IDENTIFIER AS IDENTIFIER SEMI','import',5,'p_import','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',107),
  ('import -> IMPORT IDENTIFIER SEMI','import',3,'p_import','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',108),
  ('type -> IDENTIFIER LESS types GREATER','type',4,'p_type','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',117),
  ('type -> IDENTIFIER','type',1,'p_type','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',118),
  ('types -> types COMMA type','types',3,'p_types','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',127),
  ('types -> type','types',1,'p_types','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',128),
  ('definitions -> definitions definition','definitions',2,'p_definitions','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',135),
  ('definitions -> definition','definitions',1,'p_definitions','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',136),
  ('definition -> native','definition',1,'p_definition','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',143),
  ('definition -> enum','definition',1,'p_definition','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',144),
  ('definition -> message','definition',1,'p_definition','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',145),
  ('native -> NATIVE IDENTIFIER variables LBRACE native_options RBRACE','native',6,'p_native','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',152),
  ('native_options -> native_options native_option','native_options',2,'p_native_options','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',162),
  ('native_options -> native_option','native_options',1,'p_native_options','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',163),
  ('native_options -> empty','native_options',1,'p_native_options','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',164),
  ('native_option -> IDENTIFIER COLON STRING SEMI','native_option',4,'p_native_option','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',171),
  ('enum -> ENUM IDENTIFIER LBRACE enum_values SEMI RBRACE','enum',6,'p_enum','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',178),
  ('enum_values -> enum_values COMMA enum_value','enum_values',3,'p_enum_values','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',185),
  ('enum_values -> enum_value','enum_values',1,'p_enum_values','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',186),
  ('enum_value -> IDENTIFIER','enum_value',1,'p_enum_value','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',193),
  ('message -> MESSAGE IDENTIFIER variables message_base message_type message_body','message',6,'p_message','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',200),
  ('message_base -> INHERITS type AS IDENTIFIER','message_base',4,'p_message_base','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',216),
  ('message_base -> empty','message_base',1,'p_message_base','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',217),
  ('message_type -> POLYMORPHIC ON STRING AS IDENTIFIER','message_type',5,'p_message_type','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',226),
  ('message_type -> empty','message_type',1,'p_message_type','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',227),
  ('message_body -> LBRACE fields RBRACE','message_body',3,'p_message_body','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',238),
  ('fields -> fields field','fields',2,'p_fields','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',245),
  ('fields -> field','fields',1,'p_fields','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',246),
  ('fields -> empty','fields',1,'p_fields','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',247),
  ('field -> IDENTIFIER type SEMI','field',3,'p_field','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',254),
  ('variables -> LESS variable_list GREATER','variables',3,'p_variables','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',261),
  ('variables -> empty','variables',1,'p_variables','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',262),
  ('variable_list -> variable_list COMMA variable','variable_list',3,'p_variable_list','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',272),
  ('variable_list -> variable','variable_list',1,'p_variable_list','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',273),
  ('variable -> IDENTIFIER','variable',1,'p_variable','/Users/ivan/Workspace/pdef/python/env/lib/python2.7/site-packages/pdef/parser.py',280),
]
