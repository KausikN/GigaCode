'''
Summary
Library of File Processing Functions made by ME
'''

# Imports
import os

# Util Functions
def GetBytesFromFile(filepath):
    return bytearray(open(filepath, 'rb').read())

# Compression Algos
# Runner Length
def RunnerLength_Compress(filepath=None, data=None, groupLength=1, countFormat='dec'):
    compressed_bytes = str(groupLength) + '_' # Header is groupLength followed by '_' to indicate end of value
    if not filepath == None:
        data_bytes = GetBytesFromFile(filepath)
    elif not data == None:
        data_bytes = bytearray(data, encoding='utf8')

        if len(data_bytes) < groupLength or groupLength == 0:
            return None

        curGroup = None
        curCount = 0
        for bg in range(groupLength, len(data_bytes)+1, groupLength):
            if curGroup == None:
                curGroup = data_bytes[bg-groupLength:bg]
                curCount = 1
            elif data_bytes[bg-groupLength:bg] == curGroup:
                curCount += 1
            else:
                compressed_bytes += curGroup.decode('utf8')
                if countFormat == 'dec':
                    compressed_bytes += str(curCount) + '_'
                elif countFormat == 'hex':
                    compressed_bytes += str(hex(curCount)) + '_'
                curGroup = data_bytes[bg-groupLength:bg]
                curCount = 1

        compressed_bytes += curGroup.decode('utf8')
        if countFormat == 'dec':
            compressed_bytes += str(curCount) + '_'
        elif countFormat == 'hex':
            compressed_bytes += str(hex(curCount)) + '_'

        if len(data_bytes) % groupLength != 0:
            data_leftout = data_bytes[(int(len(data_bytes) / groupLength) * groupLength):]
            compressed_bytes += data_leftout.decode('utf8')


    return bytearray(compressed_bytes, encoding='utf8')

def RunnerLength_Decompress(filepath=None, data=None, countFormat='dec'):
    decompressed_bytes = ''
    if not filepath == None:
        data_bytes = GetBytesFromFile(filepath).decode('utf8')
        groupLength = int(data_bytes[:data_bytes.index('_')])
        data_bytes = data_bytes[data_bytes.index('_')+1:]
    elif not data == None:
        data_bytes = data.decode('utf8')
        groupLength = int(data_bytes[:data_bytes.index('_')])
        data_bytes = data_bytes[data_bytes.index('_')+1:]

        while(data_bytes != None and data_bytes.find('_') != -1 and len(data_bytes) >= groupLength):
            group = data_bytes[:groupLength]
            count = 0
            if countFormat == 'dec':
                count = int(data_bytes[groupLength:data_bytes.find('_')])
            elif countFormat == 'hex':
                count = int(data_bytes[groupLength:data_bytes.find('_')], base=16)
            decompressed_bytes += group * count
            if ((data_bytes.find('_') + 1) == len(data_bytes)):
                data_bytes = None
            else:
                data_bytes = data_bytes[data_bytes.find('_')+1:]
        
        if data_bytes != None:
            decompressed_bytes += data_bytes
        

    return bytearray(decompressed_bytes, encoding='utf8')