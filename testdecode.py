import base64

with open('base64tsts.txt', 'rb') as file:
    dataraw = file.read()


dataraw = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADBQTFRFA6b1q Ci5/f2lt/9yu3 Y8v2cMpb1/DSJbz5i9R2NLwfLrWbw m T8I8////////SvMAbAAAABB0Uk5T////////////////////AOAjXRkAAACYSURBVHjaLI8JDgMgCAQ5BVG3//9t0XYTE2Y5BPq0IGpwtxtTP4G5IFNMnmEKuCopPKUN8VTNpEylNgmCxjZa2c1kafpHSvMkX6sWe7PTkwRX1dY7gdyMRHZdZ98CF6NZT2ecMVaL9tmzTtMYcwbP y3XeTgZkF5s1OSHwRzo1fkILgWC5R0X4BHYu7t/136wO71DbvwVYADUkQegpokSjwAAAABJRU5ErkJggg=='.replace(' ', '+')
data = dataraw.split(',', 1)[1]
#print(data)

imgdata = base64.b64decode(data)
imgdata = bytearray(data).decode("base64")
#img = dataraw.decode("base64")


filename = 'some_image.jpg'

with open(filename, 'wb') as f:
    f.write(imgdata)