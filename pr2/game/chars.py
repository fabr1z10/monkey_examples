# import monkey_toolkit
# import settings
#
# data = {}
# shoot_items = {}
#
#
#
#
# def get_character(id):
#     if id not in data:
#         print (' *** character ', id, ' not found!')
#         exit(1)
#     return data[id]
#
# def get_shoot_item(id):
#     if id not in shoot_items:
#         print (' *** shoot item ', id, ' not found!')
#         exit(1)
#     return shoot_items[id]
#
#
#
# def init():
#
#
#     global data
#     global shoot_items
#     import rooms.factories as fact
#     import rooms.actions
#     shoot_items = {
#         'veg1': {
#             'model': 'sprites2/veg1',
#             'bounce_on_walls': False,
#         },
#         'veg2': {
#             'model': 'sprites2/veg2',
#             'bounce_on_walls': False,
#         },
#         'ninji': {
#             'model': 'sprites2/ninji_item',
#             'bounce_on_walls': True,
#             'bounce_callback': rooms.actions.bounce
#         },
#         'shyguy': {
#             'model': 'sprites2/shyguy_item',
#             'bounce_on_walls': True,
#             'bounce_callback': rooms.actions.bounce
#         },
#         'shyguy_red': {
#             'model': 'sprites2/shyguy_item',
#             'palette': 'pal/shyguy_pal_1',
#             'bounce_on_walls': True,
#             'bounce_callback': rooms.actions.bounce
#         },
#         'pow': {
#             'model': 'sprites2/pow',
#             'bounce_on_walls': True,
#             'bounce_callback': rooms.actions.pow_bounce
#         }
#     }
#     data = {
#         'cherry': {
#             'factory': monkey_toolkit.collectible,
#             'args': {
#                 'model': 'sprites2/cherry',
#                 'tag': settings.Tags.generic_collectible
#             }
#         },
#         'mario': {
#             'factory': fact.smb2,
#             'args': {
#                 'model': 'sprites2/mario',
#                 'size': (10, 14, 0),
#                 'speed': 300
#             }
#         },
#         'supermario': {
#             'factory': fact.smb2,
#             'args': {
#                 'model': 'sprites2/supermario',
#                 'size': (10, 14, 0),
#                 'speed': 300,
#                 'tag': settings.Tags.generic_foe
#             }
#         },
#         'pow': {
#             'factory': fact.smb2_foe,
#             'args': {
#                 'model': 'sprites2/pow',
#                 'size': (10, 14, 0),
#                 'speed': 0,
#                 'tag': 0,
#                 'shoot_item': 'pow',
#                 'jump_anim': 'idle',
#                 'walk_anim': 'idle',
#                 'flip': False,
#                 'flip_on_edge': False
#             }
#         },
#         'ninji': {
#             'factory': fact.ninji,
#             'args': {
#                 'model': 'sprites2/ninji',
#                 'size': (10, 14, 0),
#                 'shoot_item': 'ninji',
#                 'foe_item': 'ninji'
#             }
#         },
#         'hoopster': {
#             'factory': fact.hoopster,
#             'args': {
#
#             }
#         },
#
#         'shyguy': {
#             'factory': fact.smb2_foe,
#             'args': {
#                 'model': 'sprites2/shyguy',
#                 'size': (10, 14, 0),
#                 'speed': 20,
#                 'tag': settings.Tags.generic_foe,
#                 'shoot_item': 'shyguy',
#                 'foe_item': 'shyguy',
#                 'idle_anim': 'walk'
#             },
#         },
#         'shyguy_red': {
#             'factory': fact.smb2_foe,
#             'args': {
#                 'model': 'sprites2/shyguy',
#                 'size': (10, 14, 0),
#                 'speed': 20,
#                 'tag': settings.Tags.generic_foe,
#                 'palette': 'pal/shyguy_pal_1',
#                 'shoot_item': 'shyguy_red',
#                 'foe_item': 'shyguy',
#                 'idle_anim': 'walk'
#             }
#         },
#         'veggie': {
#             'factory': fact.smb2_item,
#             'args': {
#                 'model': 'sprites2/veggie',
#                 'size': (8, 8, 0),
#                 'speed': 0,
#                 'tag': settings.Tags.veggie,
#                 'walk_anim': 'idle',
#                 'jump_anim': 'idle'
#             }
#         },
#         'tweeter': {
#             'factory': fact.tweeter,
#             'args': {
#                 'model': 'sprites2/tweeter',
#                 'size': (8, 8, 0),
#                 'speed': 20,
#                 'tag': settings.Tags.generic_foe
#             }
#         }
#     }
#
#
# # characters = {
# #
# #     'mario': {
# #         'factory': helper.smb2_player,
# #         'args': {
# #             'model': 'sprites2/mario',
# #             'size': (10, 14, 0),
# #             'speed': 300
# #         }
# #     },
# #     'supermario': {
# #         'factory': helper.smb2_player,
# #         'args': {
# #             'model': 'sprites2/supermario',
# #             'size': (10, 14, 0),
# #             'speed': 300
# #         }
# #     },
# #     'shyguy': {
# #         'factory': helper.smb2_foe,
# #         'args': {
# #             'model': 'sprites2/shyguy',
# #             'size': (10, 14, 0),
# #             'speed': 20,
# #             'tag': settings.Tags.shyguy
# #         },
# #     },
# #     'shyguy_red': {
# #         'factory': helper.smb2_foe,
# #         'args': {
# #             'model': 'sprites2/shyguy',
# #             'size': (10, 14, 0),
# #             'speed': 20,
# #             'tag': settings.Tags.shyguy,
# #             'pal': 'pal/shyguy_pal_1'
# #         }
# #     },
# #     'veggie': {
# #         'factory': helper.smb2_item,
# #         'args': {
# #             'model': 'sprites2/veggie',
# #             'size': (8, 8, 0),
# #             'speed': 0,
# #             'tag': settings.Tags.veggie,
# #             'walk_anim': 'idle',
# #             'jump_anim': 'idle'
# #         }
# #     },
# #     'tweeter': {
# #         'factory': helper.tweeter,
# #         'args': {
# #             'model': 'sprites2/tweeter',
# #             'size': (8, 8, 0),
# #             'speed': 20,
# #             'tag': settings.Tags.shyguy
# #         }
# #     }
# # }
#
