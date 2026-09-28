from translate import Translator

# 中文翻译成英文
translator = Translator(from_lang="ZH",to_lang="EN")
translation = translator.translate("该配电箱周围没有设置任何安全警示标志，如当心触电等。济南至宁津二标段李家岸干渠大桥二级配电箱箱门损坏")
print (translation)
