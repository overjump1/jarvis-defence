"""This module contains functions to generate maps and alerts for Jarvis Defence System"""
import textwrap
import staticmaps
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import s2sphere



def get_tile_provider():
    """returns a tile provider object"""
    return staticmaps.TileProvider(
            "carto-darknolabels",
            url_pattern="https://api.mapbox.com/styles/v1/overjump/cloajx0co011o01qm8cb4875v/tiles/256/$z/$x/$y@2x?access_token=sk.eyJ1Ijoib3Zlcmp1bXAiLCJhIjoiY2xvYWtibzFnMGk4cjJxbm5vZ3lvaDlzdCJ9.WdKUjQ5ieHrofIenxtvycw",
            attribution="Alert designed by Freepik, Powered by Geoapify © OpenStreetMap contributors",
            max_zoom=20,
        )
    return staticmaps.TileProvider(
        "carto-darknolabels",
        url_pattern="https://maps.geoapify.com/v1/tile/dark-matter-brown/$z/$x/$y.png",
        api_key="14f3673238834226abd424ada440953a",
        attribution="Alert designed by Freepik, Powered by Geoapify © OpenStreetMap contributors",
        max_zoom=20,
    )
    

def add_polygons_to_context(context:staticmaps.context, polygons):
    """adds polygons to a context object"""
    for polygon in polygons:
        context.add_object(
            staticmaps.Area(
                [staticmaps.create_latlng(lat, lng) for lat, lng in polygon],
                fill_color=staticmaps.parse_color("#FF00003F"),
                width=2,
                color=staticmaps.RED,
            )
        )
    pos = staticmaps.create_latlng(32.811, 34.980)
    marker = staticmaps.ImageMarker(pos, "icons/tomer.png", origin_x=27, origin_y=35)
    context.add_object(marker)

def add_longitude_to_height(context:staticmaps.context, longitude):
    # Get the latitude and longitude intervals from the LatLngRect object.
    rect = context.object_bounds()
    lat_interval = rect.lat()
    lng_interval = rect.lng()

    # Add the given longitude to the height of the latitude interval.
    new_lat_interval = s2sphere.LineInterval(lat_interval.lo(), lat_interval.hi() + longitude)
    new_rect = s2sphere.LatLngRect(new_lat_interval, lng_interval)
    context.add_bounds(new_rect)


def render_image(context:staticmaps.context, width, height):
    """renders an image from a context object"""
    image = context.render_pillow(width, height)
    #enhancer = ImageEnhance.Brightness(image)
    #image = enhancer.enhance(1)
    return image.resize(size=(1500, 1500))

def create_map(my_polygons):
    """generates a map from list of polygons of attack area"""
    tile = get_tile_provider()
    context = staticmaps.Context()
    context.set_tile_provider(tile)
    add_polygons_to_context(context, my_polygons)
    #add_longitude_to_height(context, 0.3)
    image = render_image(context, 1500, 1500)
    return image



def create_warning(title: str, msg: str, icon_path: str):
    """makes an image alert from title, msg and icon path"""
    title = title.upper()
    CAPS_FONT = "fonts/BebasNeue-Regular.ttf"
    EASY_FONT = "fonts/Roboto-Regular.ttf"

    img = Image.open('icons/alert_msg.png')
    icon = Image.open(icon_path)
    icon = icon.resize(size=(80, 80))
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(CAPS_FONT, 40)
    msg_font = ImageFont.truetype(EASY_FONT, 22)

    draw.text((46, 155), title, (255, 10, 80), font=title_font)
    wrap = textwrap.wrap(msg, width=50)
    draw.text((46, 200), "\n".join(wrap), (255, 255, 255), font=msg_font)
    img.paste(icon, (12, 31), icon)
    # img.save('image.png')

    return img


def combine_images(alert):
    """combines the map and the alert image to create the final image"""
    map_img = create_map(alert["polygons"])
    warning = create_warning(alert["title"], ', '.join(
        alert['english_cities']), get_icon_path(alert["cat"]))
    warning = ImageOps.contain(warning, (700, 700), method=Image.LANCZOS)
    warning = warning.convert("RGBA")
    map_img.paste(warning, (0, 5), warning)

    return map_img


def get_icon_path(category_id: int):
    """returns the category name of a given category id"""
    category_id = int(category_id)
    categories = {
        1: "missile",
        2: "general",
        3: "earthquake",
        4: "radioactive",
        5: "tsunami",
        6: "aircraft",
        7: "radioactive",
        10: "general",
        13: "terrorist",
        101: "missile",
        102: "general",
        103: "earthquake",
        104: "radioactive",
        105: "tsunami",
        106: "aircraft",
        107: "radioactive",
        110: "general",
        113: "terrorist"
    }

    return "icons/"+categories[category_id]+".png"
