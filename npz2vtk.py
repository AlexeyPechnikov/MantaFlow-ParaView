import numpy as np
import xarray as xr

### Save scalar to VTK (version 1) files
def da2vtk1(da, filename):
    vals = da.transpose('z','y','x').values
    header = """# vtk DataFile Version 1.0
vtk output
BINARY
DATASET STRUCTURED_POINTS
DIMENSIONS %d %d %d
ASPECT_RATIO %f %f %f
ORIGIN %f %f %f
POINT_DATA %d
SCALARS %s float
LOOKUP_TABLE default
""" % (da.x.shape[0],da.y.shape[0],da.z.shape[0],
                (np.nanmax(da.x.values)-np.nanmin(da.x.values))/(da.x.shape[0]-1),
                (np.nanmax(da.y.values)-np.nanmin(da.y.values))/(da.y.shape[0]-1),
                (np.nanmax(da.z.values)-np.nanmin(da.z.values))/(da.z.shape[0]-1),
                np.nanmin(da.x.values),
                np.nanmin(da.y.values),
                np.nanmin(da.z.values),
                da.x.shape[0]*da.y.shape[0]*da.z.shape[0],
                da.name)

    with open(filename, 'wb') as f:
        f.write(bytes(header,'utf-8'))
        np.array(vals, dtype=np.float32).byteswap().tofile(f)

### Save vector with components (i,j,k) to VTK (version 4.2) binary files
# ds2vtk3(ds, 'velocity', fname + '.vtk')
def ds2vtk3(ds, name, filename):
    da = ds.transpose('z','y','x')
    header = """# vtk DataFile Version 4.2
vtk output
BINARY
DATASET STRUCTURED_POINTS
DIMENSIONS %d %d %d
SPACING %f %f %f
ORIGIN %f %f %f
POINT_DATA %d
VECTORS %s float
""" % (da.x.shape[0],da.y.shape[0],da.z.shape[0],
                (np.nanmax(da.x.values)-np.nanmin(da.x.values))/(da.x.shape[0]-1),
                (np.nanmax(da.y.values)-np.nanmin(da.y.values))/(da.y.shape[0]-1),
                (np.nanmax(da.z.values)-np.nanmin(da.z.values))/(da.z.shape[0]-1),
                np.nanmin(da.x.values),
                np.nanmin(da.y.values),
                np.nanmin(da.z.values),
                da.x.shape[0]*da.y.shape[0]*da.z.shape[0],
                name)

    with open(filename, 'wb') as f:
        f.write(bytes(header,'utf-8'))
        arr = np.stack([da.i.values, da.j.values, da.k.values],axis=-1)
        np.array(arr, dtype=np.float32).byteswap().tofile(f)

# npz2vtk(output_vel_npz % t, output_vel_vtk % t, 'velocity')
def npz2vtk(npzfile, vtkfile, name, scale=[1,1,1], offset=[0,0,0]):
    data = np.load(npzfile)
    #print ('files', data.files)
    arr_name = data.files[0]
    arr = data[arr_name]
    #print ('arr dims', arr.ndim, arr.shape)
    if arr.ndim == 4 and arr.shape[3]==1:
#        arr = arr.squeeze()
        arr = arr[:,:,:,0]
    if arr.ndim == 4:
        ds = xr.Dataset()
        coords = {'z':range(arr.shape[0]),'y':range(arr.shape[1]),'x':range(arr.shape[2])}
        dims = ['z','y','x']
        ds['i'] = xr.DataArray(offset[0]+scale[0]*arr[:,:,:,0], dims=dims, coords=coords)
        ds['j'] = xr.DataArray(offset[1]+scale[1]*arr[:,:,:,1], dims=dims, coords=coords)
        ds['k'] = xr.DataArray(offset[2]+scale[2]*arr[:,:,:,2], dims=dims, coords=coords)
        # ParaView Calculator: (100*coordsX+604000)*iHat + (100*coordsY+9085000)*jHat + (100*coordsZ)*kHat
        ds2vtk3(ds, name, vtkfile)
    elif arr.ndim == 3:
        da = xr.DataArray(arr, dims=['z','y','x'],
                          coords={
                            'z':offset[2]+scale[2]*np.arange(arr.shape[0]),
                            'y':offset[1]+scale[1]*np.arange(arr.shape[1]),
                            'x':offset[0]+scale[0]*np.arange(arr.shape[2])},
                          name=name)
        # ParaView Calculator: (100*coordsX+604000)*iHat + (100*coordsY+9085000)*jHat + (100*coordsZ)*kHat
        da2vtk1(da, vtkfile)
    else:
        print ('Dimensions not supported: ',arr.ndim)
