# See https://www.qrcode.com/en/about/version.html

RAW_CODES = (
    (1, 21,
     (152, 128, 104, 72),
     (41, 34, 27, 17),
     (25, 20, 16, 10),
     (17, 14, 11, 7),
     (10, 8, 7, 4)),

    (2, 25,
     (272, 224, 176, 128),
     (77, 63, 48, 34),
     (47, 38, 29, 20),
     (32, 26, 20, 14),
     (20, 16, 12, 8)),

    (3, 29,
     (440, 352, 272, 208),
     (127, 101, 77, 58),
     (77, 61, 47, 35),
     (53, 42, 32, 24),
     (32, 26, 20, 15)),

    (4, 33,
     (640, 512, 384, 288),
     (187, 149, 111, 82),
     (114, 90, 67, 50),
     (78, 62, 46, 34),
     (48, 38, 28, 21)),

    (5, 37,
     (864, 688, 496, 368),
     (255, 202, 144, 106),
     (154, 122, 87, 64),
     (106, 84, 60, 44),
     (65, 52, 37, 27)),

    (6, 41,
     (1088, 864, 608, 480),
     (322, 255, 178, 139),
     (195, 154, 108, 84),
     (134, 106, 74, 58),
     (82, 65, 45, 36)),

    (7, 45,
     (1248, 992, 704, 528),
     (370, 293, 207, 154),
     (224, 178, 125, 93),
     (154, 122, 86, 64),
     (95, 75, 53, 39)),

    (8, 49,
     (1552, 1232, 880, 688),
     (461, 365, 259, 202),
     (279, 221, 157, 122),
     (192, 152, 108, 84),
     (118, 93, 66, 52)),

    (9, 53,
     (1856, 1456, 1056, 800),
     (552, 432, 312, 235),
     (335, 262, 189, 143),
     (230, 180, 130, 98),
     (141, 111, 80, 60)),

    (10, 57,
     (2192, 1728, 1232, 976),
     (652, 513, 364, 288),
     (395, 311, 221, 174),
     (271, 213, 151, 119),
     (167, 131, 93, 74)),

    (11, 61,
     (2592, 2032, 1440, 1120),
     (772, 604, 427, 331),
     (468, 366, 259, 200),
     (321, 251, 177, 137),
     (198, 155, 109, 85)),

    (12, 65,
     (2960, 2320, 1648, 1264),
     (883, 691, 489, 374),
     (535, 419, 296, 227),
     (367, 287, 203, 155),
     (226, 177, 125, 96)),

    (13, 69,
     (3424, 2672, 1952, 1440),
     (1022, 796, 580, 427),
     (619, 483, 352, 259),
     (425, 331, 241, 177),
     (262, 204, 149, 109)),

    (14, 73,
     (3688, 2920, 2088, 1576),
     (1101, 871, 621, 468),
     (667, 528, 376, 283),
     (458, 362, 258, 194),
     (282, 223, 159, 120)),

    (15, 77,
     (4184, 3320, 2360, 1784),
     (1250, 991, 703, 530),
     (758, 600, 426, 321),
     (520, 412, 292, 220),
     (320, 254, 180, 136)),

    (16, 81,
     (4712, 3624, 2600, 2024),
     (1408, 1082, 775, 602),
     (854, 656, 470, 365),
     (586, 450, 322, 250),
     (361, 277, 198, 154)),

    (17, 85,
     (5176, 4056, 2936, 2264),
     (1548, 1212, 876, 674),
     (938, 734, 531, 408),
     (644, 504, 364, 280),
     (397, 310, 224, 173)),

    (18, 89,
     (5768, 4504, 3176, 2504),
     (1725, 1346, 948, 746),
     (1046, 816, 574, 452),
     (718, 560, 394, 310),
     (442, 345, 243, 191)),

    (19, 93,
     (6360, 5016, 3560, 2728),
     (1903, 1500, 1063, 813),
     (1153, 909, 644, 493),
     (792, 624, 442, 338),
     (488, 384, 272, 208)),

    (20, 97,
     (6888, 5352, 3880, 3080),
     (2061, 1600, 1159, 919),
     (1249, 970, 702, 557),
     (858, 666, 482, 382),
     (528, 410, 297, 235)),

    (21, 101,
     (7456, 5712, 4096, 3248),
     (2232, 1708, 1224, 969),
     (1352, 1035, 742, 587),
     (929, 711, 509, 403),
     (572, 438, 314, 248)),

    (22, 105,
     (8048, 6256, 4544, 3536),
     (2409, 1872, 1358, 1056),
     (1460, 1134, 823, 640),
     (1003, 779, 565, 439),
     (618, 480, 348, 270)),

    (23, 109,
     (8752, 6880, 4912, 3712),
     (2620, 2059, 1468, 1108),
     (1588, 1248, 890, 672),
     (1091, 857, 611, 461),
     (672, 528, 376, 284)),

    (24, 113,
     (9392, 7312, 5312, 4112),
     (2812, 2188, 1588, 1228),
     (1704, 1326, 963, 744),
     (1171, 911, 661, 511),
     (721, 561, 407, 315)),

    (25, 117,
     (10208, 8000, 5744, 4304),
     (3057, 2395, 1718, 1286),
     (1853, 1451, 1041, 779),
     (1273, 997, 715, 535),
     (784, 614, 440, 330)),

    (26, 121,
     (10960, 8496, 6032, 4768),
     (3283, 2544, 1804, 1425),
     (1990, 1542, 1094, 864),
     (1367, 1059, 751, 593),
     (842, 652, 462, 365)),

    (27, 125,
     (11744, 9024, 6464, 5024),
     (3517, 2701, 1933, 1501),
     (2132, 1637, 1172, 910),
     (1465, 1125, 805, 625),
     (902, 692, 496, 385)),

    (28, 129,
     (12248, 9544, 6968, 5288),
     (3669, 2857, 2085, 1581),
     (2223, 1732, 1263, 958),
     (1528, 1190, 868, 658),
     (940, 732, 534, 405)),

    (29, 133,
     (13048, 10136, 7288, 5608),
     (3909, 3035, 2181, 1677),
     (2369, 1839, 1322, 1016),
     (1628, 1264, 908, 698),
     (1002, 778, 559, 430)),

    (30, 137,
     (13880, 10984, 7880, 5960),
     (4158, 3289, 2358, 1782),
     (2520, 1994, 1429, 1080),
     (1732, 1370, 982, 742),
     (1066, 843, 604, 457)),

    (31, 141,
     (14744, 11640, 8264, 6344),
     (4417, 3486, 2473, 1897),
     (2677, 2113, 1499, 1150),
     (1840, 1452, 1030, 790),
     (1132, 894, 634, 486)),

    (32, 145,
     (15640, 12328, 8920, 6760),
     (4686, 3693, 2670, 2022),
     (2840, 2238, 1618, 1226),
     (1952, 1538, 1112, 842),
     (1201, 947, 684, 518)),

    (33, 149,
     (16568, 13048, 9368, 7208),
     (4965, 3909, 2805, 2157),
     (3009, 2369, 1700, 1307),
     (2068, 1628, 1168, 898),
     (1273, 1002, 719, 553)),

    (34, 153,
     (17528, 13800, 9848, 7688),
     (5253, 4134, 2949, 2301),
     (3183, 2506, 1787, 1394),
     (2188, 1722, 1228, 958),
     (1347, 1060, 756, 590)),

    (35, 157,
     (18448, 14496, 10288, 7888),
     (5529, 4343, 3081, 2361),
     (3351, 2632, 1867, 1431),
     (2303, 1809, 1283, 983),
     (1417, 1113, 790, 605)),

    (36, 161,
     (19472, 15312, 10832, 8432),
     (5836, 4588, 3244, 2524),
     (3537, 2780, 1966, 1530),
     (2431, 1911, 1351, 1051),
     (1496, 1176, 832, 647)),

    (37, 165,
     (20528, 15936, 11408, 8768),
     (6153, 4775, 3417, 2625),
     (3729, 2894, 2071, 1591),
     (2563, 1989, 1423, 1093),
     (1577, 1224, 876, 673)),

    (38, 169,
     (21616, 16816, 12016, 9136),
     (6479, 5039, 3599, 2735),
     (3927, 3054, 2181, 1658),
     (2699, 2099, 1499, 1139),
     (1661, 1292, 923, 701)),

    (39, 173,
     (22496, 17728, 12656, 9776),
     (6743, 5313, 3791, 2927),
     (4087, 3220, 2298, 1774),
     (2809, 2213, 1579, 1219),
     (1729, 1362, 972, 750)),

    (40, 177,
     (23648, 18672, 13328, 10208),
     (7089, 5596, 3993, 3057),
     (4296, 3391, 2420, 1852),
     (2953, 2331, 1663, 1273),
     (1817, 1435, 1024, 784)),
)
