def convert_HV_real_to_raw(hv_value):
    """
    convert real HV value (V) to raw value to be written to register 
    """
    offset=0
    slope=1
    raw_value=int(offset+slop*hv_value)

    return raw_value

