
# from astropy.utils.data import download_file
# import matplotlib.image as mpimg
# from matplotlib.colors import Normalize
# from scipy import ndimage
from astropy import table
# from astropy.nddata import Cutout2D


# scanning the files from directory - VVVV
def scan_data(drz_search_path):
    drzlist = glob.glob(drz_search_path)  # "C:/Users/user/Documents/Astro/SN/*/*/*drz.fits"
    listlen = len(drzlist)
    print "num of tot drz.fits files =", listlen
    snlist=[]
    filelist=[]
    instlist=[]
    filtlist=[]
    for n in range(0, listlen):
        path_list=drzlist[n].split(os.sep)  #split the path (temp for current path)
        snlist.append(path_list[1])   #create a list of sn (by folder)
        filelist.append(path_list[3])  #create a list of file name
        hdulist = fits.open(drzlist[n])
        instlist.append(hdulist[0].header['INSTRUME'])
        if instlist[n] == 'WFC3':
            filtlist.append(hdulist[0].header['FILTER'])
        elif instlist[n] == 'WFPC2':
              filtlist.append(hdulist[0].header['FILTNAM1'])
        else:
              filtlist.append(hdulist[0].header['FILTER1'])
        hdulist.close()
    return snlist, filelist, instlist, filtlist

# scanning matching positions - VVVV
def csvscan(snlist, csv_path):
    csvlist = []
    RAlist = []
    DEClist = []
    reader = csv.reader(open(csv_path, "rb"))  # 'C:\Users\user\Desktop\data2.csv'
    for row in reader:
        csvlist += row
    for n in range(0, len(snlist)):
        ind = csvlist.index(snlist[n]) # finding the index of row with matching ra-dec
        RAlist.append(csvlist[ind+1])
        DEClist.append(csvlist[ind+2])
    return RAlist, DEClist

# VVVV
def create_table(snlist, filelist, instlist, filtlist, RAlist, DEClist):
    data_table = Table([snlist, filelist, instlist, filtlist, RAlist, DEClist], names=('sn', 'file', 'inst', 'filt', 'ra', 'dec'))
    return data_table


# displaying image - VVVV
def disp_img(data_table, row, col_name):
    join = os.path.join("C:\Users\user\Desktop\drz", data_table[row][col_name]) #C:\Users\user\Desktop\drz
    hdulist = fits.open(join)  # 'C:\Users\user\Desktop\drz\u2e63801t_drz.fits'
    img = hdulist[1].data  # define image data as hdulist[1] # alternitvely:  img=hdulist['sci'].data
    zmin, zmax = zscale(img)  # # displaying in Z scale
    plt.imshow(img, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
    plt.colorbar()  # the color bar on the side
    plt.suptitle(data_table[row]['sn'], fontsize=16, fontweight='bold')
    plt.title((data_table[row]['inst'], data_table[row]['filt'], data_table[row]['ra'], data_table[row]['dec']))  # plot the sn name
    plt.xlabel('Y')  # label the bars
    plt.ylabel('X')
    plt.show()
    hdulist.close()  # close only when done, otherwise doesn't work


# creating specific SN data_table
def sub_table(data_table, snname, col_name):
        sn_table = []
        for n in range(0, len(data_table)):
            if data_table[n][col_name] == snname:
                sn_table.append(data_table[n])
        return sn_table


# turning ra from article to deg - VVVV
def ra2deg(sn_table, n):
    rd = sn_table[n]['ra_h']*15 + sn_table[n]['ra_m']*0.25 + sn_table[n]['ra_s']*(1/240)
    return rd


# turning dec from article to deg - VVVV
def dec2deg(sn_table, n):
    dd = sn_table[n]['dec_d']*15 + sn_table[n]['dec_m']*0.25 + sn_table[n]['dec_s']*(1/240)
    return dd


# turning ra dec position to px according to current pic (check with ds9) - VVVV
def wcs2pix(sn_table, n):
    join = os.path.join("C:\Users\user\Desktop\drz", sn_table[n]['file']) #C:\Users\user\Desktop\drz
    hdu = fits.open(join)
    w = WCS(hdu[1].header)
    xpx, ypx = w.all_world2pix(354.064, 2.159, 1) # (sn_table[n]['rd'], sn_table[n]['dd'], 1)
    return xpx, ypx


# slicing all array around position +- n
def img_crop(img, xpx, ypx, delta):
    cropped = img[ypx-delta:ypx+delta, xpx-delta:xpx+delta]
    return cropped


# stacking certain sn - VVVV
def stacking(sn_table, col_name, xpx, ypx, delta):
    stack = []
    print ('dont forget to change from 1 to zero when you finish the check')
    for n in range(1, len(sn_table)):
        join = os.path.join("C:\Users\user\Desktop\drz", sn_table[n][col_name])
        stack.append(fits.getdata(join))  #gets the array from first headr with array - this case img. could have choosen header
    #print(stack[0].shape)
    #print(stack[0])
    for n in range(0, len(stack)):
        stack[n] = stack[n][ypx-delta:ypx+delta, xpx-delta:xpx+delta]
    stack_image = np.zeros_like(stack[0])  #np.zeros(shape=stack[0])
    for n in range(0, len(stack)):
        stack_image += stack[n]
        return stack_image

"""
for n in range(0, len(stack)):
    plt.figure()
    plt.imshow(stack[n])

for n in range(0, len(stack)):
    print(stack[n].max(), stack[n].min())

# finding the min array
def min_array(stack):
    mini = stack[0].shape
    for n in range(0, len(stack)):
        print(stack[n].shape)
        if stack[n].shape < mini:
            mini = stack[n].shape
    return mini

if __name__ == "__main__":
    fits.info('C:\Users\user\Desktop\drz\u2e63801t_drz.fits')
    hdulist[0].header  #could use for [1] image as well
    hdulist[0].header['instrume']  #print the instrument
    #hduslist? # general help,alt way: help(img)
    # start ordering from here

    #rotate
    rotate_img = ndimage.rotate(img, 90)
    plt.imshow(rotate_img, cmap='gray', norm=LogNorm, interpolation='nearest')  #print image

def fits_load(data_table, row, col):
    # join = os.path.join("C:\Users\user\Desktop\drz", data_table[row][col])
    hdus = fits.open(join) #'C:\Users\user\Desktop\drz\u2e63801t_drz.fits'
    primary = hdus[0].data  # Primary (NULL) header data unit
    img = hdus[1].data      # Intensity data
    err = hdus[2].data      # Error per pixel
    dq = hdus[3].data       # Data quality per pixel
    #hdus[1].header
    hdus.close()  # close only when done, otherwise doesn't work

    counts --> flux (how do i check it woks?)
    photflam = hdulist[1].header['photflam']
    exptime = hdulist[1].header['exptime']
    img *= photflam / exptime

    numppy array:
    print img[0]  #print the 0 line in the array
    img.shape  #the size of the array
    img.dtype.name  #tyoe of variable
    img[1,4]  #the 1,4 spot in the array
    img[10:20,30:40]  #this part of the array (11-21)
"""

