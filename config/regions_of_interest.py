import BoundingBox as bb

screen_size_1600x1024 ={"in_game_clock": bb.BoundingBox([805, 26, 18, 14], mode='relative'),
                        "minimap": bb.BoundingBox([6, 812, 241, 235], mode='relative'),
                        "hero_name": bb.BoundingBox([426, 912, 166, 22], mode='relative'),
                        "legion_camp_1": bb.CreepCamp(bb.Point(104, 996), bb.Point(89, 980)),
                        "legion_camp_2": bb.CreepCamp(bb.Point(104, 996), bb.Point(89, 980)),
                        "legion_easy_double_stack": [bb.CreepCamp(bb.Point(104, 996), bb.Point(89, 980)),
                                                     bb.CreepCamp(bb.Point(104, 996), bb.Point(89, 980))]}