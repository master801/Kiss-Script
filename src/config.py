#!/usr/bin/python3

import os
import json
import dataclasses

if not __debug__:
    from src import constants
    from src.log import Log
else:
    import constants
    from log import Log


CONFIG_PATH = 'config.cfg'

cfg: dict = dict()
cfg_script_config_type = None


def read_config():
    global cfg

    if os.path.isfile(CONFIG_PATH):
        Log.log_to_file(True, 'Reading config...\n')
        cfg_file = open(CONFIG_PATH, mode='r+', encoding='utf-8')
        cfg = json.load(fp=cfg_file, object_hook=ScriptConfigType.decode)
        cfg_file.close()
        Log.log_to_file(True, 'Read config file!\n')
        pass
    else:
        Log.log_to_file(True, 'Config does not exist!')
        Log.log_to_file(True, 'Creating config file...\n')

        cfg = {
             'currentConfigTypeID': 'cube_v1',
             'scriptConfigTypes': [
                 ScriptConfigType(
                     sct_id='cube_v1',
                     annotation_prefix='@',
                     annotation_suffix='',
                     annotation_types=[
                         'Talk'
                     ],
                     comment=';',
                     ignore=[
                     ]
                 ),
                 ScriptConfigType(
                     sct_id='babel_v1',
                     annotation_prefix='[',
                     annotation_suffix=']',
                     annotation_types=[
                     ],
                     comment=';',
                     ignore=[
                         '*|'
                     ]
                 ),
                 ScriptConfigType(
                     sct_id='norn_v1',
                     annotation_prefix='@',
                     annotation_suffix='',
                     annotation_types=[
                         'name'
                     ],
                     comment=';',
                     ignore=[
                         '*|'
                     ]
                 )
             ]
         }

        cfg_file = open(CONFIG_PATH, mode='x+t', encoding='utf-8')
        json.dump(
            cfg,
            fp=cfg_file,
            ensure_ascii=False,
            indent=2,
            default=ScriptConfigType.encode
        )
        cfg_file.close()

        Log.log_to_file(True, 'Created config file!')
        pass

    global cfg_script_config_type
    for i in cfg['scriptConfigTypes']:
        if i.sct_id == cfg['currentConfigTypeID']:
            cfg_script_config_type = i
            break
        continue
    return


def get_script_config():
    return cfg_script_config_type


@dataclasses.dataclass(init=True, frozen=True)
class ScriptConfigType:
    sct_id: str  # ID of config type

    annotation_prefix: str  # Annotation prefix - Ex: @
    annotation_suffix: str  # Annotation suffix
    comment: str  # Comment - Ex: ;

    ignore: list = dataclasses.field(default_factory=list)  # String to ignore - Ex: *|
    annotation_types: list = dataclasses.field(default_factory=list)  # Annotation types - Ex: name

    @staticmethod
    def decode(unmapped):
        if 'id' in unmapped:
            return ScriptConfigType(
                sct_id=unmapped['id'],
                annotation_prefix=unmapped['annotation_prefix'],
                annotation_suffix=unmapped['annotation_suffix'],
                annotation_types=unmapped['annotation_types'],
                comment=unmapped['comment'],
                ignore=unmapped['ignore']
            )
        else:
            return unmapped

    @staticmethod
    def encode(obj):
        return {
            'id': obj.sct_id,
            'annotation_prefix': obj.annotation_prefix,
            'annotation_suffix': obj.annotation_suffix,
            'annotation_types': obj.annotation_types,
            'comment': obj.comment,
            'ignore': obj.ignore,
        }
