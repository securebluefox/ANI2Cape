from config import capeConfig
from plistlib import dumps,loads,dump,FMT_XML,load
from PIL import Image
import io,os,sys,base64
import logging
import time
import uuid

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

def analyzeANIFile(filePath):
    with open(filePath,'rb') as f:
        if f.read(4) != b'RIFF':
            return {"code":-1,"msg":"File is not a ANI File!"}
        logging.debug('文件头检查完成！')
        fileSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
        # if os.path.getsize(filePath) != fileSize:
        #     return {"code":-2,"msg":"File is damaged!"}
        logging.debug('文件长度检查完成！')
        if f.read(4) != b'ACON':
            return {"code":-1,"msg":"File is not a ANI File!"}
        logging.debug('魔数检查完成！')
        frameRate = (1/60)*1000
        while(True):
            chunkName = f.read(4)
            if chunkName == b'LIST':
                break
            chunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
            if chunkName.lower() == b'rate':
                logging.debug('发现自定义速率！')
                frameRate = frameRate * int.from_bytes(f.read(4), byteorder='little', signed=False)
                logging.warning('发现自定义速率！由于GIF限制，将取第一帧与第二帧的速率作为整体速率！')
                f.read(chunkSize - 4)
            else:
                logging.debug('发现自定义Chunk！')
                f.read(chunkSize)
        listChunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
        if f.read(4) != b'fram':
            return {"code":-3,"msg":"File not a ANI File!(No Frames)"}
        logging.debug('frame头检查完成！')
        frameList = []
        nowSize = 4
        while(nowSize < listChunkSize):
            if f.read(4) != b'icon':
                return {"code":-4,"msg":"File not a ANI File!(Other Kind Frames)"}
            nowSize += 4
            subChunkSize = int.from_bytes(f.read(4), byteorder='little', signed=False)
            nowSize += 4
            frameList.append(f.read(subChunkSize))
            nowSize += subChunkSize
        return {"code":0,"msg":frameList,"frameRate":frameRate}

if __name__ == '__main__':
    capeData = {
        'Author': capeConfig['Author'],
        'CapeName': capeConfig['CapeName'],
        'CapeVersion': capeConfig['CapeVersion'],
        'Cloud': False,
        'Cursors': {},
        'HiDPI': capeConfig['HiDPI'],
        'Identifier': f"local.{capeConfig['Author']}.{capeConfig['CapeName']}.{time.time()}.{str(uuid.uuid4()).upper()}.{time.time()}",
        'MinimumVersion': 2.0,
        'Version': 2.0
    }
    for cursorType in capeConfig['Cursors'].keys():
        cursorSetting = {
            'FrameCount': 1,
            'FrameDuration': capeConfig['Cursors'][cursorType]['FrameDuration'],
            'HotSpotX': capeConfig['Cursors'][cursorType]['HotSpot'][0],
            'HotSpotY': capeConfig['Cursors'][cursorType]['HotSpot'][1],
            'PointsHigh': capeConfig['Cursors'][cursorType]['Size'][0],
            'PointsWide': capeConfig['Cursors'][cursorType]['Size'][1],
            'Representations': []
        }
        res = analyzeANIFile(capeConfig['Cursors'][cursorType]['ANIPath'])
        if res["code"] == 0:
            logging.info('ANI文件分析完成，帧提取完成！')
            cursorSetting['FrameCount'] = len(res["msg"])
            spriteSheet = Image.new("RGBA", (int(cursorSetting['PointsHigh']), int(cursorSetting['PointsWide'] * len(res["msg"]))))
            for frameIndex in range(len(res["msg"])):
                frameImage = Image.open(io.BytesIO(res["msg"][frameIndex]),formats=['cur']).convert('RGBA')
                extracted_frame = frameImage.resize((int(cursorSetting['PointsHigh']), int(cursorSetting['PointsWide'])))
                position = (0, int(cursorSetting['PointsHigh'] * frameIndex))
                spriteSheet.paste(extracted_frame, position)
            
            byteBuffer = io.BytesIO()
            spriteSheet.save(byteBuffer,format="TIFF")
            cursorSetting['Representations'].append(byteBuffer.getvalue())
        capeData['Cursors'][cursorType] = cursorSetting
    
    with open(f"{capeData['Identifier']}.cape",'wb') as f:
        dump(capeData, f, fmt=FMT_XML, sort_keys=True, skipkeys=False)
