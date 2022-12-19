from PIL import Image
import io,os,sys
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.fatal("Usage:python gif2spritesheet.py <inputFile> <outputFile,Option>")
    else:
        OUTPUT_SIZE = (48,48)
        gif = Image.open(f"{sys.argv[1]}")
        output = Image.new("RGBA", (OUTPUT_SIZE[0], OUTPUT_SIZE[1] * gif.n_frames))
        for frame in range(0,gif.n_frames):
            gif.seek(frame)
            extracted_frame = gif.resize(OUTPUT_SIZE)
            position = (0, OUTPUT_SIZE[0] * frame)
            output.paste(extracted_frame, position)
        if(len(sys.argv) >= 3):
            output.save(sys.argv[2],format="PNG")
        else:
            output.save(f"{sys.argv[1].strip('.gif')}.png",format="PNG")
        logging.info("转换完成！")
