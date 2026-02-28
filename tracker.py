def get_my_limiteds():
    """あなたの持ち物から限定アイテムのIDリストを取得（プロキシ経由）"""
    # inventory.roblox.com を inventory.roproxy.com に変更しました
    url = f"https://inventory.roproxy.com{3301498488}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100"
    try:
        response = requests.get(url)
        response.raise_for_status() # エラーがあればここで止める
        data = response.json()
        return [str(item['assetId']) for item in data.get('data', [])]
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []
