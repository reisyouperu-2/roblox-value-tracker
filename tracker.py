import requests
import os
import json

# 設定 (GitHub Secretsから取得)
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
USER_ID = os.getenv('ROBLOX_USER_ID')
DB_FILE = "last_values.json"

def get_my_limiteds():
    """あなたの持ち物から限定アイテムのIDリストを取得"""
    # Roblox公式のインベントリAPIを使用
    url = f"https://inventory.roblox.com{USER_ID}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    # アイテムIDだけを抽出
    return [str(item['assetId']) for item in data.get('data', [])]

def get_rolimons_data():
    """Rolimonsから全アイテムの市場価値データを取得"""
    response = requests.get("https://www.rolimons.com")
    return response.json()["items"]

def main():
    my_item_ids = get_my_limiteds()
    if not my_item_ids:
        print("限定アイテムが見つからないか、インベントリが非公開です。")
        return

    roli_data = get_rolimons_data()
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            last_data = json.load(f)
    else:
        last_data = {}

    for item_id in my_item_ids:
        item = roli_data.get(item_id)
        if not item: continue
        
        name = item[0]  # アイテム名
        val = item[2]   # RolimonsのValue (0の場合はRAPを代用)
        if val == 0: val = item[3] # RAP
        
        last_val = last_data.get(item_id)
        
        if last_val and val != last_val:
            diff = val - last_val
            diff_str = f"+{diff:,}" if diff > 0 else f"{diff:,}"
            color = 0x00ff00 if diff > 0 else 0xff0000 # 上がれば緑、下がれば赤
            
            # Discordへリッチな通知を送信
            payload = {
                "embeds": [{
                    "title": f"📈 価値変動: {name}",
                    "url": f"https://www.rolimons.com{item_id}",
                    "color": color,
                    "fields": [
                        {"name": "現在の価値", "value": f"{val:,} Robux", "inline": True},
                        {"name": "前回比", "value": f"**{diff_str}**", "inline": True}
                    ],
                    "footer": {"text": "Rolimons Data Feed"}
                }]
            }
            requests.post(WEBHOOK_URL, json=payload)

        last_data[item_id] = val

    with open(DB_FILE, "w") as f:
        json.dump(last_data, f)

if __name__ == "__main__":
    main()
