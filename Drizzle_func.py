import drizzlepac
from drizzlepac import tweakreg
import os
from astropy import table
import fnmatch

def tweak_run(path, n_up, threshold_ini, threshold_gap, conv_width_ini, conv_width_gap, roundlo_val_ini, roundlo_gap, roundhi_val_ini, roundhi_gap, peakmax_val_ini, peakmax_gap):
    
    os.chdir(path)
    shift_file = []
    file_name = []
    x_rms = []
    y_rms = []
    threshold = []
    conv_width = []
    roundlo = []
    roundhi = []
    peakmax = []

    for n in range(1, n_up, 1):
        outshifts_val = (repr(n)+'shift.txt')
        threshold_val = threshold_ini+(n-1)*threshold_gap
        conv_width_val = conv_width_ini+(n-1)*conv_width_gap
        roundlo_val = roundlo_val_ini+(n-1)*roundlo_gap
        roundhi_val = roundhi_val_ini+(n-1)*roundhi_gap
        peakmax_val = peakmax_val_ini+(n-1)*peakmax_gap
        tweakreg.TweakReg('*c0m.fits', exclusions='WFPC2_exclude.txt', updatehdr=False, shiftfile=True, outshifts=outshifts_val, residplot='No plot', see2dplot=None, use_sharp_round='Yes', threshold=threshold_val, conv_width=conv_width_val, roundlo=roundlo_val, roundhi=roundhi_val, peakmax=peakmax_val)

        shift = open(outshifts_val,"r")
        list = []
        for line in shift:
            list.append(line)
        shift.close()

        for m in range(4, len(list), 1):
            words = list[m].split()
            print words[1]
            
            if fnmatch.fnmatch(words[1],'*n*'):
                shift_file.append(outshifts_val)
                file_name.append(words[0])
                x_rms.append('failed')
                y_rms.append('failed')
                threshold.append(threshold_val)
                conv_width.append(conv_width_val)
                roundlo.append(roundlo_val)
                roundhi.append(roundhi_val)
                peakmax.append(peakmax_val)

            else: 
                shift_file.append(outshifts_val)
                file_name.append(words[0])
                x_rms.append(words[5])
                y_rms.append(words[6])
                threshold.append(threshold_val)
                conv_width.append(conv_width_val)
                roundlo.append(roundlo_val)
                roundhi.append(roundhi_val)
                peakmax.append(peakmax_val)
                
    results = table.Table([shift_file, file_name, x_rms, y_rms, threshold, conv_width, roundlo, roundhi, peakmax], names=['shift', 'file', 'x_rms', 'y_rms', 'threshold', 'conv_width', 'roundlo', 'roundhi', 'peakmax'])

    return results


def astrodrizzle_run(path, det_val, n_up, combine_type_val, driz_sep_kernel_val, driz_cr_snr_val, final_kernel_val, final_pixfrac_ini, final_pix_frac_gap, final_fillval_ini, final_fillval_gap):
    
    os.chdir(path)
    output_file = []
    det = []
    combine_type_ = []
    driz_sep_kernel_ = []
    driz_cr_snr_ = []
    final_kernel_ = []
    final_pixfrac = []
    final_fillval = []
        
    for n in range(1, n_up, 1):
        output_val = (repr(n)+'_drz.fits')
        final_pixfrac_val = final_pixfrac_ini+(n-1)*final_pix_frac_gap
        final_fillval_val = final_fillval_ini+(n-1)*final_fillval_gap
        astrodrizzle.AstroDrizzle(input='*c0m.fits', output=output_val, group=det_val, combine_type=combine_type_val, driz_sep_kernel=driz_sep_kernel_val, driz_cr_snr=driz_cr_snr_val, final_kernel=final_kernel_val, final_pixfrac=final_pixfrac_val, final_fillval=final_fillval_val)
      
        output_file.append(output_val)
        det.append(det_val)
        combine_type_.append(combine_type_val)
        driz_sep_kernel_.append(driz_sep_kernel_val)
        driz_cr_snr_.append(driz_cr_snr_val)
        final_kernel_.append(final_kernel_val)
        final_pixfrac.append(final_pixfrac_val)
        final_fillval.append(final_fillval_val)
                
    results = table.Table([output_file, det, combine_type_, driz_sep_kernel_, driz_cr_snr_, final_kernel_, final_pixfrac, final_fillval], names=['output', 'det', 'combine_type', 'driz_sep_kernel', 'driz_cr_snr', 'final_kernel', 'pixfrac', 'fillval'])

    return results
