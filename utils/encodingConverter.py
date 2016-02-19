# coding=utf-8
import chardet


def to_encoding(buf, encode, ignoreBelow=0.7):
    '''
    Convert encode the string buffer
    '''
    result = [buf, False]
    try:
        charInfo = chardet.detect(buf)
        if (charInfo['confidence'] >= ignoreBelow):
            result[0] = (buf.decode(charInfo['encoding'])).encode(encode)
            result[1] = True
        else:
            raise Exception('Cannot convert encoding with small precision!')
    except Exception as e:
        print e.message
    return result[0], result[1]
