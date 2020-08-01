# load OBJ mesh file into MantaFlow in real coordinates
# and convert it from real to logical coordinates [0-1],[0-1],[0-1]
# and return offset and scale to convert the result back to real coordinates
# scale0 defines size of calculation space in units of the mesh logical space [0-1],[0-1],[0-1]
def mesh2manta(mesh, gs, filename, scale0=[1,1,1]):
    from manta import vec3
    import pywavefront
    import numpy as np

    # === load mesh, and turn into SDF ===
    mesh.load( filename )
    # load mesh coordinates
    _mesh = pywavefront.Wavefront(filename)
    _mesh = np.asarray(_mesh.vertices)
    (_xmin,_xmax) = _mesh[:,0].min(),_mesh[:,0].max()
    (_ymin,_ymax) = _mesh[:,1].min(),_mesh[:,1].max()
    (_zmin,_zmax) = _mesh[:,2].min(),_mesh[:,2].max()
    print ("mesh real coordinates:",_xmin,_xmax, _ymin,_ymax, _zmin,_zmax)
    #print ("gs", gs.x, gs.y, gs.z)
    scale = [scale0[0]*(_xmax-_xmin)/gs.x, scale0[1]*(_ymax-_ymin)/gs.y, scale0[2]*(_zmax-_zmin)/gs.z]
    offset = [_xmin,_ymin,_zmin]
    # move
    mesh.offset(vec3(-_xmin,-_ymin,-_zmin))
    mesh.scale( gs*vec3(1./(_xmax-_xmin)/scale0[0], 1./(_ymax-_ymin)/scale0[1], 1./(_zmax-_zmin)/scale0[2]) )
    # scale and offset required to save output results in the mesh coordinates
    return (mesh, scale, offset)
