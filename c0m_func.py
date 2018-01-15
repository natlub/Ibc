from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.wcs import WCS
import glob
import os
from astropy.table import Column
from astropy.visualization import ZScaleInterval
from astropy.table import Table
import csv
from datetime import datetime
import math

# scanning the files from directory
def scan_data(c0m_search_path):
    pathlist = glob.glob(c0m_search_path)  # "C:/Users/user/Documents/Astro/SN/*/*/*c0m.fits"
    listlen = len(pathlist)
    print "num of tot c0m.fits files =", listlen
    snlist = []
    folderlist = []
    filelist = []
    instlist = []
    filtlist = []
    datelist = []
    explist = []
    MASKCORR = []  # check which processes were done on the image
    ATODCORR = []
    WF4TCORR = []
    BLEVCORR = []
    BIASCORR = []
    DARKCORR = []
    FLATCORR = []
    SHADCORR = []
    DOSATMAP = []
    DOPHOTOM = []
    DOHISTOS = []
    DRIZCORR = []
    OUTDTYPE = []
    for n in range(0, listlen):
        path = pathlist[n].split(os.sep)  #split the path (temp for current path)
        snlist.append(path[5])   #create a list of sn (by folder)
        folderlist.append(path[6])  #create a list of folder name
        filelist.append(path[7])  #create a list of file name
        hdulist = fits.open(pathlist[n])
        datelist.append(hdulist[0].header['DATE-OBS'])  # check for which processes were made in the image
        MASKCORR.append(hdulist[0].header['MASKCORR'])
        ATODCORR.append(hdulist[0].header['ATODCORR'])
        WF4TCORR.append(hdulist[0].header['WF4TCORR'])
        BLEVCORR.append(hdulist[0].header['BLEVCORR'])
        BIASCORR.append(hdulist[0].header['BIASCORR'])
        DARKCORR.append(hdulist[0].header['DARKCORR'])
        FLATCORR.append(hdulist[0].header['FLATCORR'])
        SHADCORR.append(hdulist[0].header['SHADCORR'])
        DOSATMAP.append(hdulist[0].header['DOSATMAP'])
        DOPHOTOM.append(hdulist[0].header['DOPHOTOM'])
        DOHISTOS.append(hdulist[0].header['DOHISTOS'])
        DRIZCORR.append(hdulist[0].header['DRIZCORR'])
        OUTDTYPE.append(hdulist[0].header['OUTDTYPE'])
        instlist.append(hdulist[0].header['INSTRUME'])
        if instlist[n] == 'WFC3':
            filtlist.append(hdulist[0].header['FILTER'])
            explist.append(hdulist[0].header['EXPTIME'])
        elif instlist[n] == 'WFPC2':
            filtlist.append(hdulist[0].header['FILTNAM1'])
            explist.append(hdulist[0].header['EXPTIME'])
        else:
            filtlist.append(hdulist[0].header['FILTER1'])
            explist.append(hdulist[0].header['EXPTIME'])
        hdulist.close()
    '''print "num of PERFORM in MASKCORR = ", MASKCORR.count('PERFORM')  # print which process are yet to perform
    print "num of PERFORM in ATODCORR = ", ATODCORR.count('PERFORM')
    print "num of PERFORM in WF4TCORR = ", WF4TCORR.count('PERFORM')
    print "num of PERFORM in BLEVCORR = ", BLEVCORR.count('PERFORM')
    print "num of PERFORM in BIASCORR = ", BIASCORR.count('PERFORM')
    print "num of PERFORM in DARKCORR = ", DARKCORR.count('PERFORM')
    print "num of PERFORM in FLATCORR = ", FLATCORR.count('PERFORM')
    print "num of PERFORM in SHADCORR = ", SHADCORR.count('PERFORM')
    print "num of PERFORM in DOSATMAP = ", DOSATMAP.count('PERFORM')
    print "num of PERFORM in DOPHOTOM = ", DOPHOTOM.count('PERFORM')
    print "num of PERFORM in DOHISTOS = ", DOHISTOS.count('PERFORM')
    print "num of PERFORM in DRIZCORR = ", DRIZCORR.count('PERFORM')
    print "num of PERFORM in OUTDTYPE = ", OUTDTYPE.count('PERFORM')'''
    return pathlist, snlist, folderlist, filelist, instlist, filtlist, datelist, explist


# scanning their data from csv
def csvscan(snlist, csv_path):
    csvlist = []
    ra_h = []
    ra_m = []
    ra_s = []
    dec_d = []
    dec_m = []
    dec_s = []
    explist = []
    reader = csv.reader(open(csv_path, "rb"))
    for row in reader:
        csvlist += row
    for n in range(0, len(snlist)):
        ind = csvlist.index(snlist[n])  # finding the index of row matching current sn
        ra_h.append(csvlist[ind+1])  # the ind+n is for the correct col
        ra_m.append(csvlist[ind+2])
        ra_s.append(csvlist[ind+3])
        dec_d.append(csvlist[ind+4])
        dec_m.append(csvlist[ind+5])
        dec_s.append(csvlist[ind+6])
        explist.append(csvlist[ind+7])
    return ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, explist


# turning ra to deg
def ra2deg(ra_dec_table):
    ra_deg = []
    for n in range(0, len(ra_dec_table)):
        ra_deg.append(float(ra_dec_table[n]['ra_h'])*15.00 + float(ra_dec_table[n]['ra_m'])*0.25 + float(ra_dec_table[n]['ra_s'])*float(1/240.00))
    return ra_deg


# turning dec to deg
def dec2deg(ra_dec_table):
    dec_deg = []
    for n in range(0, len(ra_dec_table)):
        dec_deg.append(float(ra_dec_table[n]['dec_d']) + float(ra_dec_table[n]['dec_m'])/60.00 + float(ra_dec_table[n]['dec_s'])/3600.00)
    return dec_deg


#  need to add another if and delete the break so that i get the most centered detector
#  turning ra dec position to px according to current pic (check with ds9)
def find_det_and_px(data_table, buff):
    det = [0] * (len(data_table))
    x_px = [0] * (len(data_table))
    y_px = [0] * (len(data_table))
    for m in range(0, len(data_table)):
        dis = 0
        hdu = fits.open(data_table[m]['path'])
        for n in range(1, hdu[0].header['NEXTEND']+1):
            w = WCS(hdu[n].header)
            temp_xpx, temp_ypx = w.all_world2pix(data_table[m]['ra_deg'], data_table[m]['dec_deg'], 1, tolerance=1.0e-8, maxiter=80) #1 stands for the origin of the corner of image - needs 1 for fits, tolerance - the change to achieve between to steps, maxiter - max steps allowed
            if 0+buff <= temp_xpx <= hdu[n].shape[1]-buff and 0+buff <= temp_ypx <= hdu[n].shape[0]-buff:
                temp_det = hdu[n].header['DETECTOR']
                x_dis = min(temp_xpx, hdu[n].shape[1]-temp_xpx)
                y_dis = min(temp_ypx, hdu[n].shape[0]-temp_ypx)
                temp_dis = math.sqrt(x_dis**2+y_dis**2)
                if temp_dis > dis:
                    dis = temp_dis
                    det[m] = temp_det
                    x_px[m] = temp_xpx
                    y_px[m] = temp_ypx
    return det, x_px, y_px


# displaying image
def disp_img(data_table, row):
    hdulist = fits.open(data_table[row]['path'])  # 'C:\Users\user\Desktop\drz\u2e63801t_drz.fits'
    img = hdulist[data_table[row]['det']].data  # define image data as hdulist[the correct detector]
    zmin, zmax = ZScaleInterval(img)  # displaying in Z scale
    plt.imshow(img, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
    plt.colorbar()  # the color bar on the side
    plt.suptitle(data_table[row]['sn'], fontsize=16, fontweight='bold')
    plt.title((data_table[row]['inst'], data_table[row]['filt'], data_table[row]['x_px'], data_table[row]['y_px']))  # plot the sn name
    plt.xlabel('X')  # label the bars
    plt.ylabel('Y')
    plt.scatter(data_table[row]['x_px'], data_table[row]['y_px'], s=10, c='red', marker='o')
    plt.show()
    hdulist.close()  # close only when done, otherwise doesn't work


# need to crop image here around source

# stacking image
def stacking(data_table, row_list, delta):
    stack = []
    for n in range(0, len(row_list)):
        stack.append(fits.getdata(data_table[row_list[n]]['path']))  #gets the array from first headr with array - this case img. could have choosen header
    '''for n in range(0, len(stack)):
        stack[n] = stack[n][ypx-delta:ypx+delta, xpx-delta:xpx+delta]''' # needed for cropping - do later
    stack_image = np.zeros_like(stack[0])  #np.zeros(shape=stack[0])
    for n in range(0, len(stack)):
        stack_image += stack[n]
        return stack_image

'''
# the image displayed is upside down - maybe straight to corner
disp image
img = hdu[1].data  # define image data as hdulist[1] # alternitvely:  img=hdulist['sci'].data
zmin, zmax = ZScaleInterval(img)  # # displaying in Z scale
plt.imshow(img, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
'''


'''
#  create only pre exp table
def date_table(data_table):
    rows = []
    for n in range(0, len(data_table)):
        imgd = dt.strptime(data_table[n]['imgdate'], "%Y-%m-%d")
        expd = dt.strptime(data_table[n]['expdate'], "%m/%d/%Y")
        if imgd > expd:
            rows.append(n)
    data_table.remove_rows(rows)
    return data_table


#  create only WFPC2 table
def WFPC2_table(data_table):
    rows = []
    for n in range(0, len(data_table)):
        if data_table[n]['inst'] != 'WFPC2':
            rows.append(n)
    data_table.remove_rows(rows)
    return data_table


# remember table[col][row]
table[row]
table[0:2] rows [0-2]
table['sn'] - col sn
'''