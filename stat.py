dt=data_table


# filter according to one of the columns and its parameters:
for n in range(0, len(dt)):
    if dt[n]['filt'] != 'F814W':
        rows.append(n)
dt.remove_rows(rows)


# add data to this table by scanning from the fits one of the header
exptimelist=[]
for n in range(0, len(dt)):
    hdu = fits.open(dt[n]['path'])
    exptimelist.append(hdu[0].header['EXPTIME'])
exptime_col = Column(name='exptime', data=exptimelist)
dt.add_column(exptime_col)

# the avg of the column
np.mean(dt['exptime'])

# count how many are from one type of parameter in the same column


# display in browser
dt.show_in_browser()

