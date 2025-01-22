import random
import os

# 画面クリア関数
def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass  # エラーが出ても続行

# 初期ステータスリセット関数
def reset_player():
    return {
        "名前": "",
        "HP": 10,
        "階層": 0,
        "称号": "初心者",
        "ゴールド": 0,
        "チャレンジ回数": 1  # チャレンジ回数を1からスタート
    }

player = reset_player()
履歴 = []

# 称号設定
RANKS = {
    10: "冒険初心者",
    20: "冒険熟練者",
    30: "冒険達人",
    40: "冒険英雄",
    50: "伝説の冒険者"
}

# HPの色設定
def get_hp_color():
    if player["HP"] <= 2:
        return "\033[91m"  # 赤色
    elif player["HP"] <= 5:
        return "\033[93m"  # 黄色
    else:
        return "\033[0m"   # 通常色

# 称号更新
def update_rank():
    for floor, rank in RANKS.items():
        if player["階層"] >= floor and player["称号"] != rank:
            player["称号"] = rank
            履歴.append(f"B{player['階層']} 到達！称号: {rank} を獲得！")

# 探索イベント
def explore():
    global 履歴
    player["階層"] += 1
    update_rank()

    event = random.choice(["敵", "宝箱", "罠", "回復"])
    if event == "敵":
        damage = random.randint(1, 3)
        player["HP"] -= damage
        履歴.append(f"B{player['階層']} 敵に遭遇！HP {color_text(f'-{damage}', 'red')}")
    elif event == "宝箱":
        gold = random.randint(1, 5)
        player["ゴールド"] += gold
        履歴.append(f"B{player['階層']} 宝箱を発見！+{gold} ゴールド")
    elif event == "罠":
        damage = random.randint(1, 2)
        player["HP"] -= damage
        履歴.append(f"B{player['階層']} 罠にかかった！HP {color_text(f'-{damage}', 'red')}")
    elif event == "回復":
        heal = random.randint(1, 2)
        player["HP"] += heal
        if player["HP"] > 10:
            player["HP"] = 10
        履歴.append(f"B{player['階層']} 回復の泉！HP {color_text(f'+{heal}', 'green')}")

    if len(履歴) > 3:
        履歴.pop(0)

# 色付きテキスト
def color_text(text, color):
    if color == "red":
        return f"\033[91m{text}\033[0m"  # 赤色
    elif color == "green":
        return f"\033[92m{text}\033[0m"  # 緑色
    elif color == "yellow":
        return f"\033[93m{text}\033[0m"  # 黄色
    else:
        return text

# ステータス表示
def show_status():
    hp_color = get_hp_color()
    print(f"【{player['名前']}のステータス】")
    print(f"称号: {player['称号']}")
    print(f"{hp_color}HP: {player['HP']}\033[0m")
    print(f"ゴールド: {player['ゴールド']}")
    print(f"階層: B{player['階層']}")
    print(f"チャレンジ回数: {player['チャレンジ回数']} / 10")
    print("\n【探索履歴】")
    for log in 履歴:
        print(log)

# ゲーム終了
def end_game():
    global player, 履歴
    print("\nゲーム終了！結果はこちら:")
    print(f"到達階層: B{player['階層']}")
    print(f"獲得ゴールド: {player['ゴールド']}")
    input("\nEnterキーを押してゲームを終了します...")
    exit()

# ダンジョンから戻る処理
def return_to_town():
    global player, 履歴
    print(f"\n{player['名前']}はダンジョンから戻った！")
    player["階層"] = 0  # 階層リセット
    player["HP"] = 10  # HPリセット
    player["チャレンジ回数"] += 1  # チャレンジ回数を増加
    if player["チャレンジ回数"] > 10:  # 10回を超えたら終了
        print("\nチャレンジ回数が10回に達しました。ゲーム終了です！")
        end_game()
    else:
        print("HPが全回復しました。再び挑戦できます。")
        input("\nEnterキーを押して次の冒険を始めてください...")
        履歴 = []  # 履歴リセット

# ゲーム開始
def start_game():
    global player
    clear_screen()
    player["名前"] = input("冒険者の名前を入力してください: ")
    while True:
        clear_screen()
        show_status()
        if player["HP"] <= 0:
            print("\nHPが尽きた...ゲームオーバー！")
            end_game()

        print("\n1: もぐる / 2: 戻る")
        action = input("> ")
        if action == "1":
            explore()
        elif action == "2":
            return_to_town()
        else:
            print("無効な選択です。1または2を入力してください。")

# ゲーム開始
start_game()