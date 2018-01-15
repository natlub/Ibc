from image_func import *

snlist, filelist, instlist, filtlist = scan_data("C:/Users/user/Documents/Astro/SN/*/*/*drz.fits")  # data of sn's in directory

ralist, declist = csvscan(snlist, 'C:\Users\user\Desktop\data2.csv')  # scan matching sn position

data_table = create_table(snlist, filelist, instlist, filtlist, ralist, declist)  # create final data_table

sn_table1 = sub_table(data_table, '1999dn', 'sn')  # create specific sn (or whatever filter) data_table (or according to other title - sn/file/inst/filt/ra/dec)
sn_table2 = sub_table(data_table, '2005v', 'sn')  # create specific sn (or whatever filter) data_table (or according to other title - sn/file/inst/filt/ra/dec)
sn_mix = sn_table1 + sn_table2

unique_by_sn = table.unique(data_table, keys='sn')
WFPC2_table = sub_table(data_table, 'WFPC2', 'inst')  #the WFPC2 table

# check
print(data_table)
#print(sn_table1)
print "num of WFC3 = ", instlist.count('WFC3')
print "num of WFPC2 = ", instlist.count('WFPC2')
print "num of ACS = ", instlist.count('ACS')

plt.figure()  #plot image: table, row, col
disp_img(sn_table1, 2, 'file')

plt.figure()  #plot image: table, row, col
disp_img(sn_table2, 2, 'file')

#def disp_stack(stack_mat, sn_table):
stack1 = stacking(sn_table1, 'file', 919, 936, 100)
zmin, zmax = zscale(stack1)
plt.figure()
plt.imshow(stack1, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle(sn_table1[1]['sn'], fontsize=16, fontweight='bold')
plt.title('no of stacked images:'+str((len(sn_table1))))  # plot the sn name
plt.xlabel('Y')  # label the bars
plt.ylabel('X')
plt.show()

stack2 = stacking(sn_table2, 'file', 911, 893, 100)
zmin, zmax = zscale(stack2)
plt.figure()
plt.imshow(stack2, cmap='gray', vmin=zmin, vmax=zmax)  # print image (filters in web), maybe should be: normalize/LogNorm?
plt.colorbar()  # the color bar on the side
plt.suptitle(sn_table2[1]['sn'], fontsize=16, fontweight='bold')
plt.title('no of stacked images:'+str((len(sn_table2))))  # plot the sn name
plt.xlabel('Y')  # label the bars
plt.ylabel('X')
plt.show()

stackmix = stack1+stack2
count = len(sn_table1)+len(sn_table2)
zmin, zmax = zscale(stackmix)
plt.figure()
plt.imshow(stackmix, cmap='gray', vmin=zmin, vmax=zmax)
plt.colorbar()  # the color bar on the side
plt.title('no of stacked images:'+str(count))  # plot the sn name
plt.xlabel('Y')  # label the bars
plt.ylabel('X')
plt.show()


