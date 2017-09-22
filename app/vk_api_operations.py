from app.cnf import  vk_token
import requests as r

template_url = "https://api.vk.com/method/{}?{}&access_token={}&v=5.68"

def is_user_liked_post( object_url:str, liker_url:str, is_group=False):
    if is_group:
        user_id = _get_owner_id_from_post_url(object_url, True)
        user_id = -1 * int(user_id)
    else:
        user_id = _get_owner_id_from_post_url(object_url)
    liker_id = _get_user_id_by_url(liker_url)
    post_id = _get_post_id_from_url(object_url)
    params = "user_id={}&owner_id={}&item_id={}&type=post".format(liker_id,user_id,post_id)
    return r.get(template_url.format("likes.isLiked", params, vk_token)).json()["response"]['liked'] > 0


def is_user_liked_photo( object_url: str, liker_url: str, is_group=False):
    if is_group:
        user_id = _get_owner_id_from_photo_url(object_url, True)
        user_id = -1 * int(user_id)
    else:
        user_id = _get_owner_id_from_photo_url(object_url)
    liker_id = _get_user_id_by_url(liker_url)
    photo_id = _get_photo_id_from_url(object_url)
    params = "user_id={}&owner_id={}&item_id={}&type=photo".format(liker_id,user_id,photo_id)
    return r.get(template_url.format("likes.isLiked",params,vk_token)).json()["response"]['liked'] > 0

def is_user_comment_post( object_url:str, commenter_id:str, is_group=False):
    commenter_id = _get_user_id_by_url(commenter_id)
    if is_group:
        user_id = _get_owner_id_from_post_url(object_url, True)
        user_id = -1 * int(user_id)
    else:
        user_id = _get_owner_id_from_post_url(object_url)
    post_id = _get_post_id_from_url(object_url)
    params = "count=100&sort=desc&owner_id={}&post_id={}".format(user_id,post_id)
    response = r.get(template_url.format("wall.getComments",params,vk_token)).json()["response"]
    items = response.get("items", None)
    if len(items) == 0:
        return False
    from_ids = [d["from_id"] for d in items]
    return commenter_id in from_ids

def is_user_comment_photo( object_url:str,commenter_id:str, is_group=False):
    commenter_id = _get_user_id_by_url(commenter_id)

    if is_group:
        user_id = _get_owner_id_from_photo_url(object_url, True)
        user_id = -1 * int(user_id)
    else:
        user_id = _get_owner_id_from_photo_url(object_url)

    photo_id = _get_photo_id_from_url(object_url)
    params = "count=100&sort=desc&owner_id={}&photo_id={}".format(user_id,photo_id)
    response = r.get(template_url.format("photos.getComments", params, vk_token)).json()["response"]
    items = response.get("items", None)
    if len(items) == 0:
        return False
    from_ids = [d["from_id"] for d in items]
    return commenter_id in from_ids


def _get_user_id_by_url(url:str):
    id = url.split("/")[-1]
    params = "user_ids={}".format(id)
    json = r.get(template_url.format("users.get",params, vk_token)).json()
    return json['response'][0]['id']

def _get_post_id_from_url(url:str):
    return int(url.split("_")[-1])

def _get_photo_id_from_url(url:str):
    s = url.find("photo") + len("photo")
    e = url.find("%")
    phot_str_id = url[s:e]
    params= "photos={}".format(phot_str_id)
    return r.get(template_url.format("photos.getById",params,vk_token)).json()["response"][0]["id"]


def _get_group_id_from_url(group_url:str):
    group_id = group_url.split("/")[-1]
    params = "group_id={}".format(group_id)
    return r.get(template_url.format("groups.getById",params, vk_token)).json()["response"][0]["id"]


def _get_owner_id_from_photo_url(url:str, isGroup= False):
    token = "photo"
    if isGroup:
        token = token + "-"
    s = url.find(token) + len(token)
    e = url.find("%")
    phot_str_id = url[s:e]
    return phot_str_id.split('_')[0]

def _get_owner_id_from_post_url(url: str, isGroup= False):
    token = "wall"
    if isGroup:
        token = token + "-"
    s = url.find(token) + len(token)
    phot_str_id = url[s:]
    return phot_str_id.split('_')[0]
