import json

txt = """
{
  "タイトル": "今日の活動報告です！",
  "本文": "プロデューサーさん、こんにちは！櫻木真乃です。

今日の午前中の活動について報告します。

朝9時からのダンスレッスンでは、新曲の振り付けを集中して練習しました。少し難しい部分もありましたが、何度も繰り返し練習して少しずつ上達できたと思います。

その後、11時からはボイストレーニングがありました。発声練習や新曲の歌唱練習を行いました。高音部分で少し苦戦しましたが、先生からアドバイスをいただいて改善点が分かりました。

これからの午後は、楽曲のレコーディングと衣装合わせがあります。全力で頑張りますので、応援よろしくお願いします！

何か気になる点がありましたら、ご指導ください。
これからも精一杯頑張ります！

櫻木真乃"
}
"""

json_data = json.loads(txt, strict=False)
print("title: ", json_data["タイトル"])
print("txt: ", json_data["本文"])