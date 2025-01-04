import math
import geomag
import exifread
from datetime import datetime
from pygeomag import GeoMag

def obtener_exif_datos(ruta_archivo):
    """
    Obtain metadata from the picture.
    Args:
        ruta_archivo: File path.
    Returns:
        Specific metadata from the picture required for subsequent functions.
    """
    with open(ruta_archivo, 'rb') as archivo:
        tags = exifread.process_file(archivo)
    # Extract latitude, longitude, and timestamp from EXIF data
    latitud = tags.get('GPS GPSLatitude')
    longitud = tags.get('GPS GPSLongitude')
    hora_fecha = tags.get('EXIF DateTimeOriginal')
    ancho = tags.get('EXIF ExifImageWidth') # in pixels
    alto = tags.get('EXIF ExifImageLength') # in pixels
    h = tags.get('GPS GPSAltitude')

    # Convert latitude, longitude, timestamp, width, height, and drone altitude into a readable and compatible format
    # for use in subsequent functions
    latitud_decimal = latitud.values[0].num / latitud.values[0].den
    longitud_decimal = longitud.values[0].num / longitud.values[0].den

    # Calculate minutes and seconds in decimal
    minutos_decimal = (latitud.values[1].num / latitud.values[1].den) / 60
    segundos_decimal = (latitud.values[2].num / latitud.values[2].den) / 3600

    # Add the decimal degrees, minutes, and seconds to get the final latitude
    latitud_final = latitud_decimal + minutos_decimal + segundos_decimal

    # Do the same for longitude
    minutos_decimal = (longitud.values[1].num / longitud.values[1].den) / 60
    segundos_decimal = (longitud.values[2].num / longitud.values[2].den) / 3600
    longitud_final = longitud_decimal + minutos_decimal + segundos_decimal
    if str(tags.get('GPS GPSLatitudeRef')) == "S":
        latitud_final *= -1
    if str(tags.get('GPS GPSLongitudeRef')) == "W":
        longitud_final *= -1

    hora_fecha = str(hora_fecha)
    formato = "%Y:%m:%d %H:%M:%S"
    hora_fecha_float = datetime.strptime(hora_fecha, formato)
    hora_fecha_ts = hora_fecha_float.timestamp() # Representation of a date and time as a single number
    anio_decimal = hora_fecha_ts / (3600 * 24 * 365.25) + 1970

    ancho_decimal = float(str(ancho))
    alto_decimal = float(str(alto))
    h_decimal = h.values[0].num / h.values[0].den

    return latitud_final, longitud_final, anio_decimal, ancho_decimal, alto_decimal, h_decimal



def calcular_nueva_posicion(px, py, ancho_decimal, alto_decimal, latitud_decimal, longitud_decimal, h_decimal, ang_declin):
    """
    Obtain coordinates given the x (px) and y (py) positions in pixels.
    Args:
        px: The position on the horizontal axis (pixels).
        py: The position on the vertical axis (pixels).
        ancho_decimal: The width in pixels of the image.
        alto_decimal: The height in pixels of the image.
        latitud_decimal: Latitude of the central location of the image, in decimal format.
        longitud_decimal: Longitude of the central location of the image, in decimal format.
        h_decimal: The drone's flight altitude.
        ang_declin: Magnetic declination in degrees.
    Returns:
        Magnetic declination in degrees.
    """
    # The pixel coordinates (px, py) are normalized
    x = px / ancho_decimal
    y = py / alto_decimal

    # Calculate geographic coordinates
    nueva_lon = longitud_decimal + (x * math.cos(math.radians(ang_declin)) / h_decimal)
    nueva_lat = latitud_decimal + (y * math.sin(math.radians(ang_declin)) / h_decimal)

    return (nueva_lat, nueva_lon)
