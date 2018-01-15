from astropy.io import fits

imglist=['u29r1r01t_c0m.fits','u29r1r02t_c0m.fits']
for root in imglist:
	cut=fits.open(root,mode='update')
	cut[1].data[0:799,0:50] = cut[1].data[0:62,0:799] = 0.0
	cut[2].data[0:799,0:50] = cut[2].data[0:30,0:799] = 0.0
	cut[3].data[0:799,0:37] = cut[3].data[0:52,0:799] = 0.0
	cut[4].data[0:799,0:48] = cut[4].data[0:50,0:799] = 0.0
cut.close()
