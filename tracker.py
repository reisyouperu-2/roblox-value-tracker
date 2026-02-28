import requests
import os
import json

# 設定
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
ITEMS_TO_TRACK = ["123456", "789012"]  # 監視したいアイテムIDを入れる
DB_FILE = "last_values.json"

def get_rolimons_data():
    # Rolimons APIから全アイテムデータを取得
    response = requests.get("https://www.rolimons.com")
    return response.json()["items"]

def main():
    current_data = get_rolimons_data()
    
    # 前回のデータを読み込み
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            last_data = json.load(f)
    else:
        last_data = {}

    for item_id in ITEMS_TO_TRACK:
        item = current_data.get(item_id)
        if not item: continue
        
        # Rolimonsデータ構造: [name, acro, value, rap, ...]
        name = item[0]
        val = item[2]
        
        last_val = last_data.get(item_id)
        if last_val and val != last_val:
            diff = val - last_val
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            
            # Discordへ通知
            payload = {"content": f"📢 **{name}** の価値が変動しました！\n価格: `{val}` (前回比: {diff_str})"}
            requests.post(WEBHOOK_URL, json=payload)

        last_data[item_id] = val

    # 今回のデータを保存
    with open(DB_FILE, "w") as f:
        json.dump(last_data, f)

if __name__ == "__main__":
    main()
