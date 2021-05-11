import struct
import json


def wrt_geometry_2_OBJ(geometry, out_path, in_inches):
    '''
    @geometry: output from extract_geometry_fromGDB with flag "obj_output" set as True
    @out_path: the path to the output .obj file
    @in_inches: bool, if true output in inches, otherwise in meters
    '''
    num_layers = len(geometry)
    num_struct = [0] * num_layers
    for i in range(num_layers):
        num_struct[i] = len(geometry[i])
    fout = open(out_path, "wb")
    fout.write(struct.pack('I', num_layers))                                    # write number of layers 
    fout.write(struct.pack(str(num_layers)+'I', *num_struct))                   # write number of structures for each layer
    for i in range(num_layers):
        layer_name = geometry[i][0][0]
        fout.write(struct.pack('I', len(layer_name)))                           # write length of layer name
        fout.write(struct.pack(str(len(layer_name))+'s', layer_name.encode()))  # write layer name
        for j in range(num_struct[i]):
            pt_num = geometry[i][j][1]
            fout.write(struct.pack('I', pt_num))                                # write number of points
            if in_inches:
                coords_in_inches = np.asarray(geometry[i][j][2:])/12*0.3048
                fout.write(struct.pack(str(pt_num*2)+'f', *list(coords_in_inches))) # write point coordinates in inches
            else:
                fout.write(struct.pack(str(pt_num*2)+'f', *geometry[i][j][2:])) # write point coordinates in meters
    fout.close()
    

def read_geometry_OBJ(in_path, cvt2_meters):
    '''
    @in_path: the path to the input .obj file. format of .obj file has to follow the specifications
    @cvt2_meters: bool, if to convert to meters
    '''
    fin = open(in_path, "rb")
    num_layers = struct.unpack('I', fin.read(4))[0]                            # read number of layers
    num_struct = struct.unpack(str(num_layers)+'I', fin.read(4*num_layers))    # read number of structures for each layer as an array
    geometry_result = [None] * num_layers
    for i in range(num_layers):
        tmp_ = [None] * num_struct[i]
        geometry_result[i] = tmp_

    for i in range(num_layers):
        layer_name_length = struct.unpack('I', fin.read(4))[0]                # read length of layer name
        layer_name = struct.unpack(str(layer_name_length)+'s', fin.read(layer_name_length))[0].decode("utf-8") # read layer name
        for j in range(num_struct[i]):
            pt_num = struct.unpack('I', fin.read(4))[0]                        # read number of points for current structure
            pt_coords = struct.unpack(str(pt_num*2)+'f', fin.read(4*pt_num*2)) # read point coordinates into an array
            if cvt2_meters:
                pt_coords = np.asarray(pt_coords)/0.3048*12
            row_ = [layer_name, pt_num] + list(pt_coords)
            geometry_result[i][j] = row_
    fin.close()
    return geometry_result
    

def wrt_geometry_2_JSON(geometry, out_path, in_inches):
    '''
    @geometry: output from extract_geometry_fromGDB with flag "obj_output" set as True
    @out_path: the path to the output .json file
    @in_inches: bool, if true output in inches, otherwise in meters
    '''
    num_layers = len(geometry)
    num_struct = [0] * num_layers
    for i in range(num_layers):
        num_struct[i] = len(geometry[i])

    data = {}
    data['header'] = {'layer number': num_layers, 'structure number': num_struct}
    for i in range(num_layers):
        layer_number = "layer " + str(i)
        data[layer_number] = {'layer name': geometry[i][0][0], 'points': []}
        for j in range(num_struct[i]):
            if in_inches:
                coords_in_inches = np.asarray(geometry[i][j][2:])/12*0.3048
                data[layer_number]['points'].append({'point number': geometry[i][j][1], 'coordinates': list(coords_in_inches)}) # output in inches
            else:
                data[layer_number]['points'].append({'point number': geometry[i][j][1], 'coordinates': geometry[i][j][2:]}) # output in meters
    with open(out_path, 'w') as fout:
        json.dump(data, fout, indent=2)
            

def read_geometry_JSON(in_path, cvt2_meters):
    '''
    @in_path: the path to the input .obj file. format of .obj file has to follow the specifications
    @cvt2_meters: bool, if to convert to meters
    '''
    with open(in_path) as fin:
        data = json.load(fin)
        num_layers = data['header']['layer number']
        num_struct = data['header']['structure number']

        geometry_result = [None] * num_layers
        for i in range(num_layers):
            tmp_ = [None] * num_struct[i]
            geometry_result[i] = tmp_

        for i in range(num_layers):
            layer_number = "layer " + str(i)
            layer_name = data[layer_number]['layer name']
            for j in range(num_struct[i]):
                pt_num = data[layer_number]['points'][j]['point number']
                pt_coords = data[layer_number]['points'][j]['coordinates']
                if cvt2_meters:
                    pt_coords = np.asarray(pt_coords)/0.3048*12
                row_ = [layer_name, pt_num] + pt_coords.tolist()
                geometry_result[i][j] = row_
        return geometry_result