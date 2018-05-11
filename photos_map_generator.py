import exifread
import os


def get_gps_metadata(img_file):
    f = open(img_file, 'rb')
    tags = exifread.process_file(f)
    try:
        lat_raw = tags['GPS GPSLatitude']
    except KeyError:
        return None

    lat = (lat_raw.values[0].num/lat_raw.values[0].den) + (lat_raw.values[1].num/lat_raw.values[1].den)/60\
          + (lat_raw.values[2].num/lat_raw.values[2].den)/3600
    lat_dir = str(tags['GPS GPSLatitudeRef'])
    if lat_dir == 'S':
        lat = lat * -1

    long_raw = tags['GPS GPSLongitude']
    lon = (long_raw.values[0].num / long_raw.values[0].den) + (long_raw.values[1].num / long_raw.values[1].den)/60\
          + (long_raw.values[2].num / long_raw.values[2].den)/3600
    lon_dir = str(tags['GPS GPSLongitudeRef'])
    if lon_dir == 'W':
        lon = lon * -1

    f.close()
    return {'lat': lat, 'lon': lon}


def plot_thumbs_from_dirs(dir1, dir2, dir3, dir4, dir5, dir6, map_name):
    write_html_header(map_name)
    init_map(map_name)
    count = 0
    for f in os.listdir(dir1):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir1, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir1 + '/' + f, count)
                count = count + 1

    for f in os.listdir(dir2):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir2, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir2 + '/' + f, count)
                count = count + 1

    for f in os.listdir(dir3):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir3, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir3 + '/' + f, count)
                count = count + 1

    for f in os.listdir(dir4):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir4, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir4 + '/' + f, count)
                count = count + 1

    for f in os.listdir(dir5):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir5, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir5 + '/' + f, count)
                count = count + 1

    for f in os.listdir(dir6):
        if f.endswith('.JPG'):
            gps = get_gps_metadata(os.path.join(dir6, f))
            if gps:
                create_photo_marker(map_name, gps['lat'], gps['lon'], dir6 + '/' + f, count)
                count = count + 1

    write_html_tail(map_name)

def write_html_header(map_name):
    f = open(map_name, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write('<html>\n')
    f.write('\t<head>\n')
    f.write('\t\t<meta name="viewport" content="initial-scale=1.0, user-scalable=no">\n')
    f.write('\t\t<meta charset="utf-8">\n')
    f.write('\t\t<title>Picture Map</title>\n')
    f.write('\t\t<style>\n')
    f.write('\t\t\t#map {\n')
    f.write('\t\t\t\theight: 100%;\n')
    f.write('\t\t\t}\n\n')

    f.write('\t\t\thtml, body {\n')
    f.write('\t\t\t\theight: 100%;\n')
    f.write('\t\t\t\tmargin: 0;\n')
    f.write('\t\t\t\tpadding: 0;\n')
    f.write('\t\t\t}\n\n')

    f.write('\t\t</style>\n')
    f.write('\t\t</head>\n')
    f.write('\t\t<div id=\"map\"></div>\n')
    f.write('\t\t<body>\n')
    f.write('\t\t<script>\n\n')


    f.close()


def init_map(map_name):
    f = open(map_name, 'a')

    f.write('\t\t\tfunction initMap() {\n')
    f.write('\t\t\t\tvar map = new google.maps.Map(document.getElementById(\'map\'), {\n')
    f.write('\t\t\t\t\tzoom: 10,\n')
    f.write('\t\t\t\t\tcenter: {lat: 30, lng: -80},\n')
    f.write('\t\t\t\t});\n\n')

    f.write('\t\t\tfunction load_img(img_id) {\n')
    f.write('\t\t\t\tvar imgDefer = document.getElementById(img_id);\n')
    f.write('\t\t\t\timgDefer.setAttribute(\'src\', imgDefer.getAttribute(\'data-src\'));\n')
    f.write('\t\t\t}\n\n')

    f.close()

def create_photo_marker(map_name, img_lat, img_lon, img_file, count):
    f = open(map_name, 'a')

    f.write('\t\t\tvar photo_marker%d = \'<img id=\"img%d\" src=\"data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=\"  data-src=\"' % (count, count))
    f.write(img_file)
    f.write('\" style=\"width: 600px; height: 450px; transform: rotate(180deg)\">\';\n')


    f.write('\t\t\t\tvar infowindow%d = new google.maps.InfoWindow({content: photo_marker%d});\n' % (count, count))
    f.write('\t\t\t\tvar marker%d = new google.maps.Marker({position: {lat: %f, lng: %f}, map: map});\n' % (count, img_lat, img_lon))
    f.write('\t\t\t\tmarker%d.addListener(\'click\', function () {infowindow%d.open(map, marker%d); load_img(\'img%d\')});\n' % (count, count, count, count))

    f.close()

def write_html_tail(map_name):
    f = open(map_name, 'a')


    f.write('\t\t\t}\n')
    f.write('\t\t</script>\n')
    f.write('\t\t<script async defer src=\'https://maps.googleapis.com/maps/api/js?key=AIzaSyAJZNRP8jnAPicPX0f0DTVyh8ilVjWWpXA&callback=initMap\'></script>\n')

    f.write('\t</body>\n')
    f.write('</html>\n')


    f.close()


def main():
    plot_thumbs_from_dirs('D:/Photos/2014', 'D:/Photos/2010-2013', 'D:/Photos/2013', 'D:/Photos/2015', 'D:/Photos/2016', 'D:/Photos/2017', 'map.html')


if __name__ == '__main__':
    main()


