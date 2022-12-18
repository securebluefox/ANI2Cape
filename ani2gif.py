from PIL import Image
import io,os,sys
import logging

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
    if len(sys.argv) < 2:
        logging.fatal("Usage:python ani2gif.py <inputFile> <outputFile,Option>")
    else:
        res = analyzeANIFile(sys.argv[1])
        GIFframes = []
        if res["code"] == 0:
            logging.info('ANI文件分析完成，帧提取完成！')
            for frame in res["msg"]:
                frameImage = Image.open(io.BytesIO(frame),formats=['CUR']).convert('RGBA')
                GIFframes.append(frameImage)
            if(len(sys.argv) >= 3):
                GIFframes[0].save(sys.argv[2],format="GIF",save_all=True, append_images=GIFframes[1:], optimize=False, duration=res["frameRate"], loop=0, transparency=0, disposal=2)
            else:
                GIFframes[0].save(f"{sys.argv[1].strip('.ani')}.gif",format="GIF",save_all=True, append_images=GIFframes[1:], optimize=False, duration=res["frameRate"], loop=0, transparency=0, disposal=2)
            logging.info('GIF生成完成！')
        else:
            logging.fatal(res["msg"])
