import matplotlib as mpl
mpl.use("QT4agg")
import sunpy.map
import sys
import pdb
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
import matplotlib.image as mpimg
#from sunpy.coordinates import frames, sun
#from astropy.coordinates import SkyCoord
#from astropy import units as u
#from astropy.io import fits

def plot_single_fits(filename):
    try:
        m = sunpy.map.Map(filename)
        m.plot()
        plt.show()
        plt.close('all')
    except ValueError:
        print("No file with the chosen name found\n")


def save_fits(filename, index):
    m = sunpy.map.Map(filename)
    m.plot()

    filename_tail = os.path.basename(filename)
    pltname = filename_tail.split("-")
    end_string = pltname[2].split(".")

    pltname = pltname[1] + "-" + end_string[0]
    plt.savefig(pltname)
    fig = plt.gcf()
    plt.close(fig)
    
    print(filename + "\n")

def produce_video(images):
    frames = []

    #fig = plt.figure()
    #for i in xrange(len(images)):
    #    img = mpimg.imread(images[i])
    #    frames.append([plt.imshow(img, cmap=cm.Greys_r, animated=True)])
    print(str(images[0]) + "\n")

    #ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True, repeat_delay=1000)

    #ani.save('movie.mp4')
    #plt.show()

# coordinate transformation function
def icrs_to_helio(file):
    x=0
#    hdu = fits.open(file)
#    header = hdu[0].header
#    data = np.squeeze(hdu[0].data)
#    obstime = header['date-obs'] # observational time
#    freq = header['crval3']*u.Hz # frequency of observation

    # reference coordinate from FITS file
#    reference_coord = SkyCoord(header['crval1']*u.deg, header['crval2']*u.deg,
#                           frame='gcrs',
#                           obstime=obstime,
#                           distance=sun.earth_distance(obstime),
#                           equinox='J2000',
#                           observer = 'earth')
#
#    reference_coord_arcsec = reference_coord.transform_to(frames.Helioprojective)

    # cdelt in arcsec rather than degrees
#    cdelt1 = (np.abs(header['cdelt1'])*u.deg).to(u.arcsec)
#    cdelt2 = (np.abs(header['cdelt2'])*u.deg).to(u.arcsec)

#    P1 = sun.P(obstime)
    #print(header['crpix1'])
    #header_test = sunpy.map.make_fitswcs_header(data, reference_coord_arcsec,
    #                                    reference_pixel=u.Quantity([header['crpix1'], header['crpix2']]*u.pixel),
#                                            scale=u.Quantity([cdelt1, cdelt2]*u.arcsec/u.pix),
#                                            rotation_angle=-P1,
#                                            wavelength=freq.to(u.MHz),
#                                            observatory='LOFAR')
    '''
    # There is currently a bug in the make_fitswcs_header in that the lat and lon are given in backwards to crval1,
    # crval2 in the header - so we just need to switch these
    header_test2 = header_test.copy()
    header_test2['crval1'] = header_test['crval2']
    header_test2['crval2'] = header_test['crval1']
    '''
    #lofar_map = sunpy.map.Map(data, header_test)

    #rotate_map = lofar_map.rotate()

    #return rotate_map

