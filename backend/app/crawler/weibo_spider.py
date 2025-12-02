import requests
import logging
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import random
import time

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
]

# Placeholder for Proxy Pool
PROXIES = [
    # "http://user:pass@ip:port",
]

def _sanitize_cookie(cookie: str) -> str:
    if not cookie:
        return ""
    c = cookie.replace("\r", "").replace("\n", "")
    return c.strip()

def get_random_headers(uid=None, cookie=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
    }
    if cookie:
        headers["Cookie"] = _sanitize_cookie(cookie)
        headers["Referer"] = f"https://weibo.com/u/{uid}" if uid else "https://weibo.com/"
    else:
        headers["MWeibo-Pwa"] = "1"
        headers["Referer"] = f"https://m.weibo.cn/u/{uid}" if uid else "https://m.weibo.cn/"
        
    return headers

def get_proxy(proxies=None):
    pool = proxies if proxies else PROXIES
    if not pool:
        return None
    choice = random.choice(pool)
    return {"http": choice, "https": choice}

def parse_pc_weibo_date(date_str: str) -> datetime:
    try:
        dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
        return dt.astimezone(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)
    except Exception:
        return datetime.now(ZoneInfo('Asia/Shanghai')).replace(tzinfo=None)

def _extract_xsrf(cookie: str):
    if not cookie:
        return None
    parts = cookie.split(";")
    for p in parts:
        p = p.strip()
        if p.startswith("XSRF-TOKEN="):
            return p.split("=", 1)[1]
    return None

def fetch_weibo_updates(uid: str, cookie: str = None, proxies: list = None):
    """
    Fetch the latest weibo update time for a given UID.
    Dispatches to PC or Mobile API based on cookie availability.
    """
    if cookie:
        try:
            return fetch_weibo_updates_pc(uid, cookie, proxies)
        except Exception as e:
            logger.error(f"PC API failed for {uid}, falling back to mobile: {e}")
            # Fallback to mobile
    
    return fetch_weibo_updates_mobile(uid, proxies)

def fetch_weibo_updates_pc(uid: str, cookie: str, proxies: list = None):
    # PC API: https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0
    base_url = "https://weibo.com/ajax/statuses/mymblog"
    params = {
        "uid": uid,
        "page": 1,
        "feature": 0
    }
    
    time.sleep(random.uniform(1, 3))
    headers = get_random_headers(uid, cookie)
    xsrf = _extract_xsrf(cookie)
    if xsrf:
        headers["X-XSRF-TOKEN"] = xsrf
        headers["x-xsrf-token"] = xsrf
    headers.update({
        "client-version": "v2.47.138",
        "server-version": "v2025.11.25.2",
    })
    response = requests.get(
        base_url,
        params=params,
        headers=headers,
        proxies=get_proxy(proxies),
        timeout=15
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}")
        
    data = response.json()
    if not data.get("data", {}).get("list"):
         # Try alternative: /ajax/profile/info?uid={uid} -> statuses
         return None, "No posts found in PC API"
         
    posts = data.get("data", {}).get("list", [])
    if not posts:
        return None, "No posts list in response"

    latest_created_at = None
    for p in posts:
        if p.get("isTop") == 1:
            continue
        created_at_str = p.get("created_at")
        latest_created_at = parse_pc_weibo_date(created_at_str) if created_at_str else None
        if latest_created_at:
            break
    return latest_created_at, None

def fetch_weibo_updates_mobile(uid: str, proxies: list = None):
    # 1. Get container ID for weibo posts
    base_url = "https://m.weibo.cn/api/container/getIndex"
    
    container_id = None
    
    # Try to get container ID from profile tabs
    try:
        params_profile = {
            "type": "uid",
            "value": uid,
        }
        time.sleep(random.uniform(1, 2))
        resp_profile = requests.get(
            base_url,
            params=params_profile,
            headers=get_random_headers(uid),
            proxies=get_proxy(proxies),
            timeout=10
        )
        if resp_profile.status_code == 200:
            data_profile = resp_profile.json()
            tabs = data_profile.get("data", {}).get("tabsInfo", {}).get("tabs", [])
            for tab in tabs:
                if tab.get("tab_type") == "weibo":
                    container_id = tab.get("containerid")
                    break
        else:
            logger.warning(f"Profile fetch failed for {uid}: {resp_profile.status_code}, trying fallback")
            
    except Exception as e:
        logger.warning(f"Exception fetching profile for {uid}: {e}, trying fallback")

    if not container_id:
         # Fallback to standard ID construction if not found in tabs
        container_id = f"107603{uid}"

    # 2. Get Posts
    params_posts = {
        "type": "uid",
        "value": uid,
        "containerid": container_id
    }
    
    try:
        time.sleep(random.uniform(1, 2))
        response = requests.get(
            base_url, 
            params=params_posts, 
            headers=get_random_headers(uid), 
            proxies=get_proxy(proxies),
            timeout=10
        )
        
        if response.status_code != 200:
             logger.error(f"Error fetching posts: {response.status_code} - {response.text[:200]}")
             return None, f"HTTP Error {response.status_code}"

        data = response.json()
        
        if data.get("ok") != 1:
            logger.error(f"Failed to fetch data for UID {uid}: {data}")
            # If 432 or other error happens here, we can't do much without proxies
            return None, f"API returned error: {data.get('msg', 'unknown')}"

        cards = data.get("data", {}).get("cards", [])
        latest_created_at = None
        
        for card in cards:
            if card.get("card_type") == 9: # Type 9 is a Weibo post
                mblog = card.get("mblog", {})
                created_at_str = mblog.get("created_at")
                latest_created_at = parse_weibo_date(created_at_str)
                # We only need the latest one
                if latest_created_at:
                    return latest_created_at, None
        
        return None, "No posts found"

    except Exception as e:
        logger.error(f"Exception fetching posts for {uid}: {e}")
        return None, str(e)

def parse_weibo_date(date_str: str) -> datetime:
    """
    Parse Weibo date string to datetime object.
    """
    if not date_str:
        return None
        
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    
    if "刚刚" in date_str:
        return now.replace(tzinfo=None)
    
    if "分钟前" in date_str:
        minutes = int(date_str.replace("分钟前", ""))
        target = now - timedelta(minutes=minutes)
        return target.replace(tzinfo=None)
    
    if "小时前" in date_str:
        hours = int(date_str.replace("小时前", ""))
        target = now - timedelta(hours=hours)
        return target.replace(tzinfo=None)
        
    if "昨天" in date_str:
        time_str = date_str.replace("昨天", "").strip()
        try:
            t = datetime.strptime(time_str, "%H:%M")
            y = now - timedelta(days=1)
            return y.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0).replace(tzinfo=None)
        except:
            return now.replace(tzinfo=None)
            
    if "-" in date_str:
        parts = date_str.split("-")
        if len(parts) == 2: # MM-DD
            try:
                return datetime.strptime(f"{now.year}-{date_str}", "%Y-%m-%d")
            except:
                pass
        elif len(parts) == 3: # YYYY-MM-DD
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                pass
                
    return now.replace(tzinfo=None)
