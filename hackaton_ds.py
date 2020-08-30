import googlemaps  # from https://github.com/googlemaps/google-maps-services-python, installed using "pip install -U googlemaps"
import cv2
import numpy as np
import math
import json
import requests

zoom = 20
tileSize = 256
initialResolution = 2 * math.pi * 6378137 / tileSize
originShift = 2 * math.pi * 6378137 / 2.0
earthc = 6378137 * 2 * math.pi
factor = math.pow(2, zoom)
map_width = 256 * (2 ** zoom)


def grays(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


def white_image(im):
    return cv2.bitwise_not(np.zeros(im.shape, np.uint8))


def pixels_per_mm(lat, length):
    return length / math.cos(lat * math.pi / 180) * earthc * 1000 / map_width


def sharp(gray):
    blur = cv2.bilateralFilter(gray, 5, sigmaColor=7, sigmaSpace=5)
    kernel_sharp = np.array((
        [-2, -2, -2],
        [-2, 17, -2],
        [-2, -2, -2]), dtype='int')
    return cv2.filter2D(blur, -1, kernel_sharp)


def rotation(center_x, center_y, points, ang):
    angle = ang * math.pi / 180
    rotated_points = []
    for p in points:
        x, y = p
        x, y = x - center_x, y - center_y
        x, y = (x * math.cos(angle) - y * math.sin(angle), x * math.sin(angle) + y * math.cos(angle))
        x, y = x + center_x, y + center_y
        rotated_points.append((x, y))
    return rotated_points


def calc_area(lat, lng):
    gurl = "https://maps.googleapis.com/maps/api/staticmap?"
    MapImgageURL = "{gurl}maptype=satellite&center={lat},{lng}&scale={scale}&zoom={zoom}&size={sizex}x{sizey}&key=AIzaSyDks1m0UBovbzm4QR8Ja7axR-S6DpiK-ig&sensor=false".format(
        gurl=gurl, lat=lat, lng=lng, scale=1, zoom=20, sizex=300, sizey=300)

    ImgRequest = requests.get(MapImgageURL)

    if ImgRequest.status_code == requests.codes.ok:
        img = open("test.jpg", "wb")
        img.write(ImgRequest.content)
        img.close()
        pl, pw, l, w, solar_angle = 4, 1, 8, 5, 30
        image = cv2.imread("test.jpg")
        img = cv2.pyrDown(image)
        n_white_pix = np.sum(img == 255)
        high_reso_orig = cv2.pyrUp(image)
        canny_contours = white_image(image)
        image_contours = white_image(image)
        image_polygons = grays(canny_contours)
        canny_polygons = grays(canny_contours)
        grayscale = grays(image)
        sharp_image = sharp(grayscale)
        edged = cv2.Canny(sharp_image, 180, 240)
        edge_image = sharp_image
        thresh = cv2.threshold(sharp_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        new_image = white_image(image)
        ret, thresh2 = cv2.threshold(edge_image, 198, 255, cv2.THRESH_BINARY)
        n_white_pix = np.sum(thresh2 == 255)
        metersPerPx = 0.0075
        area_roof = n_white_pix * metersPerPx
        return area_roof


def find_roof_json(lat, lng, address):

        gmaps = googlemaps.Client(key='AIzaSyDks1m0UBovbzm4QR8Ja7axR-S6DpiK-ig')
        #ReverseGeocodeResult = gmaps.reverse_geocode((lat, lng))
        AddressString = address #ReverseGeocodeResult[0]['formatted_address']

        # if address is not already in dataframe AND LocationType is a rooftop,
        # get the new address coordinates and populate the dataframe
        GeocodeResult = gmaps.geocode(AddressString)
        PlaceID = GeocodeResult[0]['place_id']

        # We only want rooftops (no parks or other structures), so only add to the
        # database if the 'location_type' == 'ROOFTOP'
        LocationType = GeocodeResult[0]['geometry']['location_type']

        if LocationType == 'ROOFTOP':
            try:
                ad_id = str(round(float(lat), 6)) + '-' + str(round(float(lng), 6))
                sqrd_meter = calc_area(lat, lng)
                return (ad_id, lat, lng, AddressString, sqrd_meter)

            except:
                return 'An error occurs when retrieving the user info'
        else:
            return 'This is not a rooftop'

