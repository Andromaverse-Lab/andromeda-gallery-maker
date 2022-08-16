import os
import requests
from wand.image import Image
from stargazeutils.ipfs import IpfsClient
from .collections import AndromedaCollections

IPFS_ROOT = os.environ.get("IPFS_ROOT", default="https://stargaze.mypinata.cloud")
ipfs = IpfsClient(ipfs_root=IPFS_ROOT)

ipfs_map = {
    AndromedaCollections.ANDROMA_PUNK: {
        "ipfs": "ipfs://bafybeie7f26w3jeqcmn4nj62sfae45nvl4ivg6fmk5gfmyybapcwlicica/images",
        "logo": "./images/apunks-logo.png",
    },
    AndromedaCollections.ANDROMAVERSE: {
        "ipfs": "ipfs://bafybeifhapzqtpmkazo7567mdyhn4fxla5hxho3xpy7qtxezzoz5zd7rsi/images",
        "logo": "./images/andromaverse-logo.png",
    },
    AndromedaCollections.STARGAZE_PUNK: {
        "ipfs": "ipfs://bafybeicvvfnlxuo3ineufnwqcjvwvo64dkazv5an4lclrymb77fmnga2ze/images",
        "logo": "./images/spunks-logo.png"
    },
}

for k,v in ipfs_map.items():
    logo = Image(filename=v['logo'])
    logo.resize(300, 30)
    ipfs_map[k]['logo_img'] = logo


def get_image(collection, token_id):
    ipfs_url = f"{ipfs_map[collection]['ipfs']}/{token_id}.png"
    image_url = ipfs.ipfs_to_http(ipfs_url)
    response = requests.get(image_url)
    image = Image(blob=response.content)
    return image

def create_gallery(tokens):
    bg = Image(filename="./images/gallery-bg.png")
    frame_w, frame_h = 300, 300
    top = 380

    def add_image(token, left):
        name = token['name']
        id = token['id']
        print(f"Adding image {name} {id}")
        image = get_image(name, token['id'])
        image.resize(frame_w, frame_h)
        bg.composite_channel("all_channels", image, "dissolve", left, top)
        bg.composite_channel("all_channels", ipfs_map[name]['logo_img'], "dissolve", left, top - 55)
    
    add_image(tokens[0], 40)
    add_image(tokens[1], 427)
    add_image(tokens[2], 815)
    add_image(tokens[3], 1202)

    return bg
