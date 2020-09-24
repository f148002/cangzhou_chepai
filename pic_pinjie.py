from PIL import Image
import io

def getfull(namea,locationlist):
    old = Image.open(namea)
    new = Image.new('RGB',(260,116))  #260,116是完整验证码的大小，10x58的小方块一共有56块。一行26个，即260。上下两行，即116。
    shang = []
    xia = []
    for location in locationlist:
        if location['y'] == str(-58):
            shang.append(old.crop((abs(int(location['x'])),58,abs(int(location['x']))+10,116)))
        if location['y'] == str(0):
            xia.append(old.crop((abs(int(location['x'])),0,abs(int(location['x']))+10,58)))
    #粘贴
    i = 0
    for ima in shang:
        new.paste(ima,(i,0))   #根据图片左上角的坐标来粘贴
        i +=10
    i = 0
    for imx in xia:
        new.paste(imx,(i,58))
        i +=10
    new.save("yes.jpg")

def compare(yes,no):
    for xzhou in range(0,260):
        for yzhou in range(0,116):
            pianyi = offset(yes,no,xzhou,yzhou)
            if pianyi == None:
                pass
            else:
                return pianyi

def offset(yes,no,x,y):
    pix1 = yes.getpixel((x,y))
    pix2 = no.getpixel((x,y))
    for rgb in range(0,3):
        if pix1[rgb] - pix2[rgb] > 48:
            print (x)
            print(y)
            return x  #这就是偏移量


def is_pixel_equal(img1, img2, x, y):
    '''
        判断两张图片的同一像素点的RGB值是否相等
    '''
    pixel1, pixel2 = img1.load()[x, y], img2.load()[x, y]
    # print(pixel1,pixel2)
    # 设定一个比较基准
    sub_index = 60

    # 比较
    if abs(pixel1[0] - pixel2[0]) < sub_index and abs(pixel1[1] - pixel2[1]) < sub_index and abs(
            pixel1[2] - pixel2[2]) < sub_index:
        return True
    else:
        return False


def get_gap_offset(img1, img2):
    '''
        获取缺口的偏移量
    '''
    x = int(img1.size[0] / 4.2)
    for i in range(x, img1.size[0]):
        for j in range(img1.size[1]):
            # 两张图片对比,(i,j)像素点的RGB差距，过大则该x为偏移值
            if not is_pixel_equal(img1, img2, i, j):
                x = i
                return x
    return x

if __name__ == '__main__':
    img1 = r'G:\Users\f148002\Downloads\big.jpg'
    img1 = Image.open(img1)
    img2 = r'G:\Users\f148002\Downloads\big2.jpg'
    img2 = Image.open(img2)

    result = get_gap_offset(img1,img2)

    print(result)