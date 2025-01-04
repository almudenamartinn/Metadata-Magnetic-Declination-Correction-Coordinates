File path of the picture
ruta_archivo = "/Users/.../IMG.jpg"


# Obtain EXIF data
latitud_final, longitud_final, anio_decimal, ancho_decimal, alto_decimal, h_decimal = obtener_exif_datos(ruta_archivo)

# Calculate magnetic declination
geo_mag = GeoMag()
# Altitude is set to 0
# h_decimal is the altitude relative to sea level
# https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml does not take altitude into account for declination calculation
# That is the reference used
# print(h_decimal)
ang_declin_i = geo_mag.calculate(glat=latitud_final, glon=longitud_final, alt=0, time=anio_decimal)
# print(float(ang_declin_i.d))
ang_declin = float(ang_declin_i.d)

# Calculate corrected coordinates given a pixel position "x" and a pixel position "y"
# -> example: pixel no. 234 on the x-axis, pixel no. 583 on the y-axis
coordenadas_gps = calcular_nueva_posicion(234, 583, ancho_decimal, alto_decimal, latitud_final, longitud_final, h_decimal, ang_declin)

# Print the corrected coordinates of that point
print("GPS Coordinates of the pixel:", coordenadas_gps)


