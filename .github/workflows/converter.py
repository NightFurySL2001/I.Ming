import os
import sys
from fontTools.ttLib import TTFont

input_fontname = os.path.abspath(sys.argv[1])
if not input_fontname.lower().endswith((".ttf", ".otf")):   
    raise ImportError("Not a font file")
subfolder = "compatibility"
font = TTFont(input_fontname)
print("準備導出中……")

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

PLATFORM_UNICODE = 1
PLATFORM_WINDOWS = 3
PLATFORM_WINDOWS_LANG = Map(
    ENGLISH = 0X409,
    CHINESE_CN = 0X804,
    CHINESE_SG = 0X1004,
    CHINESE_TW = 0X404,
    CHINESE_HK = 0XC04,
    CHINESE_MO = 0X1404,
    JAPANESE = 0X411,
    KOREAN = 0X412,
)
NAME_LIST_LOCALIZE = {
    "I.MingCP": "一點明體CP",
    "I.MingVarCP": "一點明體異體CP",
}
RENAME_LIST_EN = {
    "I.MingCP": "PMingI.U",
    "I.MingVarCP": "PMingI.UVar",
}
RENAME_LIST_ZHT = {
    "一點明體CP": "新一細明體",
    "一點明體異體CP": "新一細明體異體",
}


# sample: https://twitter.com/stevenpetryk/status/1504920229251477505
#scale = 1.15
#font['head'].unitsPerEm = 
#    int(font['head'].unitsPerEm / scale)

ascent = int(font["OS/2"].sTypoAscender)
#ascender
font["hhea"].ascent = ascent
font["OS/2"].usWinAscent = ascent

descent = int(font["OS/2"].sTypoDescender)
#descender
font["hhea"].descent = descent
font["OS/2"].usWinDescent = abs(descent)

linegap = abs(descent)
#line gap
font["hhea"].lineGap = linegap
font["OS/2"].sTypoLineGap = linegap

print("刪除其他語言名稱……")
#remove names in other languages
font["name"].removeNames(platformID = PLATFORM_UNICODE)
font["name"].removeNames(langID = PLATFORM_WINDOWS_LANG.CHINESE_CN)
font["name"].removeNames(langID = PLATFORM_WINDOWS_LANG.CHINESE_SG)
font["name"].removeNames(langID = PLATFORM_WINDOWS_LANG.JAPANESE)

current_name = Map(EN="", ZHT="")
new_name = Map(EN="", ZHT="")
for key in RENAME_LIST_EN.keys():
    if key in input_fontname:
        current_name.EN = key
        new_name.EN = RENAME_LIST_EN[key]
        current_name.ZHT = NAME_LIST_LOCALIZE[key]
        new_name.ZHT = RENAME_LIST_ZHT[current_name.ZHT]


print("替換「%s」爲「%s」；「%s」爲「%s」……" % (current_name.EN, new_name.EN, current_name.ZHT, new_name.ZHT))
#change name, sample: https://github.com/chrissimpkins/fontname.py/blob/master/fontname.py
namerecord_list = font["name"].names
for record in namerecord_list:
    name_string = record.string.decode(record.getEncoding())
    record.string = name_string.replace(current_name.EN, new_name.EN).replace(current_name.ZHT, new_name.ZHT)

dir_path, filename = os.path.split(input_fontname)
final_filename = filename.replace(current_name.EN, new_name.EN).replace(current_name.ZHT, new_name.ZHT)
if not os.path.exists(os.path.join(dir_path, subfolder)):
    os.mkdir(os.path.join(dir_path, subfolder))
final_path = os.path.join(dir_path, subfolder, final_filename)
font.save(final_path)
print("導出完成，文件名：" + final_path)
