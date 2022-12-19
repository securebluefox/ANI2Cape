# ANI2Cape
A tool that can convert Windows Animated Cursors (*.ani) to GIF/Pillow Images/Cape format

一个可以将ANI格式文件转化为GIF格式、抽帧转为Pillow Images格式，转为Linux/MacOS可用的指针格式的工具~

- [x] ANI2Pillow Image
- [x] ANI2GIF(ANI2Pillow Image + Pillow Image2GIF)
- [x] ANI2SpriteSheet(ANI2Pillow Image + Pillow Image2SpriteSheet)
- [x] GIF2SpriteSheet(GIF2Pillow Image + Pillow Image2SpriteSheet)
- [ ] ANI2Cape(TODO)

# Usage
`Usage:python XXX.py <inputFile> <outputFile,Option>`

inputFile:需要转化的文件路径。

outputFile：输出的文件路径。默认为<输入文件名>.xxx

# Document
[从Windows动态指针到MacOS动态指针——ANI2GIF](https://www.bilibili.com/read/cv20591812)
