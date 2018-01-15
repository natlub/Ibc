from c0m_func import *

pathlist, snlist, folderlist, filelist, instlist, filtlist, datelist = scan_data("/Users/natalie/Documents/sn/*/*/*c0m.fits")  # data of sn's in directory - also checks **CORR commends, does not count Omit because it means it is not required

ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, explist = csvscan(snlist, "/Users/natalie/Documents/c0mdata.csv")  # scan matching sn position and explosion date

ra_dec_table = Table([snlist, ra_h, ra_m, ra_s, dec_d, dec_m, dec_s], names=('sn', 'ra_h', 'ra_m', 'ra_s', 'dec_d', 'dec_m', 'dec_s'))  # create ra sec sn's table
#ra_dec_table.show_in_browser()

ra_deg = ra2deg(ra_dec_table)  # convert ra dec to deg
dec_deg = dec2deg(ra_dec_table)

data_table = Table([snlist, pathlist, folderlist, filelist, instlist, filtlist, ra_deg, dec_deg, datelist, explist], names=('sn', 'path', 'folder', 'file', 'inst', 'filt', 'ra_deg', 'dec_deg', 'imgdate', 'expdate'))
# data_table.show_in_browser()  # create the general table

# taking only img pre exp- try and put it in a func, not urgent
rows = []
for n in range(0, len(data_table)):
    imgd = dt.strptime(data_table[n]['imgdate'], "%Y-%m-%d")
    expd = dt.strptime(data_table[n]['expdate'], "%m/%d/%Y")
    if imgd > expd:
        rows.append(n)
data_table.remove_rows(rows)

# taking only WFPC2 cam
rows = []
for n in range(0, len(data_table)):
    if data_table[n]['inst'] != 'WFPC2':
        rows.append(n)
data_table.remove_rows(rows)

# finding the best det, and the px of the ra dec, that are with distance of buffer from the edges - if not found within buffer - 0 is listed. tried 80 - only 2 zeroes
det, x_px, y_px = find_det_and_px(data_table, 5)

# adding the lists above to the data_table
det_col = Column(name='det', data=det)
data_table.add_column(det_col)
x_px_col = Column(name='x_px', data=x_px)
data_table.add_column(x_px_col)
y_px_col = Column(name='y_px', data=y_px)
data_table.add_column(y_px_col)

dt=data_table.to_pandas()
dt.to_pickle('data.pickle')

## UP TO HERE LOAD FULL TABLE



# displaying specific SN's and specific det's images
row_list = []
for n in range(0, len(data_table)):
    if data_table[n]['sn'] == '2003jg' and data_table[n]['det'] == 3:
        row_list.append(n)
        # print(data_table[n]['path'])
        plt.figure()
        disp_img(data_table, n)

# stacking - move to function later
stack = []
for n in range(0, len(row_list)):
    stack.append(fits.getdata(data_table[row_list[n]]['path']))  #gets the array from first headr with array - this case img. could have choosen header
'''for n in range(0, len(stack)):
    stack[n] = stack[n][(data_table[row_list[n]]['y_px'])-100:(data_table[row_list[n]]['y_px'])+100, (data_table[row_list[n]]['x_px'])-100:(data_table[row_list[n]]['x_px'])+100]'''
stack_image = np.zeros_like(stack[0])  #np.zeros(shape=stack[0])
for n in range(0, len(stack)):
    stack_image += stack[n]

# display stacked image
zmin, zmax = zscale(stack_image)
plt.figure()
plt.imshow(stack_image, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle(data_table[row_list[0]]['sn'], fontsize=16, fontweight='bold') # plot the sn name
plt.title('no of stacked images:'+str((len(row_list))))
plt.xlabel('X')  # label the bars
plt.ylabel('Y')
plt.scatter(data_table[row_list[0]]['x_px'], data_table[row_list[0]]['y_px'], s=10, c='red', marker='o')
plt.show()

# check for post exp images

# for the c0f image from article

buff = 5
hdu = fits.open('C:/Users/user/Documents/Astro/2000ew - anonymous67106 postexp\u6ea5403m_c0m.fits') # C:/Users/user/Documents/Astro/SN\2001ai\anonymous67133\u65r2701r_c0m.fits
for n in range(1, hdu[0].header['NEXTEND']): #0 not needed - up to no' of detectors
    w = WCS(hdu[n].header)
    xpx, ypx = w.all_world2pix(175.243833333, 11.4655, 1, maxiter=30)  #1 stands for the origin of the corner of image - needs 1 for fits
    if 0+buff <= xpx <= hdu[n].shape[1]-buff and 0+buff <= ypx <= hdu[n].shape[0]-buff:
        det = hdu[n].header['DETECTOR']
        x_px = xpx
        y_px = ypx
        break
print det
print x_px,y_px

img = hdu[3].data  # define image data as hdulist[1] # alternitvely:  img=hdulist['sci'].data
zmin, zmax = zscale(img)  # # displaying in Z scale
plt.imshow(img, cmap='gray', vmin=zmin, vmax=zmax, origin='lower')  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle(hdu[0].header['FILENAME'], fontsize=16, fontweight='bold')
plt.title((hdu[0].header['INSTRUME'], hdu[0].header['FILTNAM1'], det))  # plot the sn name
plt.xlabel('X')  # label the bars
plt.ylabel('Y')
plt.plot(x_px, y_px, 'ro')
plt.show()

# for the c0f image from article

buff = 5
hdu = fits.open('C:/Users/user/Documents/Astro/2000ew - anonymous67106 postexp\u6ea5403m_drz.fits') # C:/Users/user/Documents/Astro/SN\2001ai\anonymous67133\u65r2701r_c0m.fits
for n in range(1, hdu[0].header['NEXTEND']): #0 not needed - up to no' of detectors
    w = WCS(hdu[n].header)
    xpx, ypx = w.all_world2pix(175.243833333, 11.4655, 1, maxiter=30)  #1 stands for the origin of the corner of image - needs 1 for fits
    if 0+buff <= xpx <= hdu[n].shape[1]-buff and 0+buff <= ypx <= hdu[n].shape[0]-buff:
        det = hdu[n].header['DETECTOR']
        x_px = xpx
        y_px = ypx
        break
print det
print x_px,y_px

img = hdu[1].data  # define image data as hdulist[1] # alternitvely:  img=hdulist['sci'].data
zmin, zmax = zscale(img)  # # displaying in Z scale
plt.figure()
plt.imshow(img, cmap='gray', vmin=zmin, vmax=zmax, origin='lower')  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle(hdu[0].header['FILENAME'], fontsize=16, fontweight='bold')
plt.title((hdu[0].header['INSTRUME'], hdu[0].header['FILTNAM1'], det))  # plot the sn name
plt.xlabel('X')  # label the bars
plt.ylabel('Y')
plt.plot(x_px, y_px, 'ro')
plt.show()


"""
# crop the image, not required qith tick
delta = 30
cropped = img[y_px-delta:y_px+delta, x_px-delta:x_px+delta]
plt.figure()
zmin, zmax = zscale(img)  # # displaying in Z scale
plt.imshow(cropped, cmap='gray', vmin=zmin, vmax=zmax, origin='lower')  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle('cropped', fontsize=16, fontweight='bold')
plt.title((hdu[0].header['INSTRUME'], hdu[0].header['FILTNAM1'], det))  # plot the sn name
plt.xlabel('Y')  # label the bars
plt.ylabel('X')
plt.show()
hdulist.close()  # close on
"""

"""
print some parameter from the header of all images

for n in range(1, len(data_table)):
    hdu = fits.open(data_table[n]['path'])
    print data_table[n]['sn'], hdu[0].header['ATODGAIN']
"""