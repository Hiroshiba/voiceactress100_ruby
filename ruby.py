from difflib import SequenceMatcher
from pathlib import Path

import spacy
from julius4seg.sp_inserter import kata2hira


def main():
    kanji_lines = Path("transcript_utf8.txt").read_text().splitlines()
    yomi_lines = Path("voiceactoress100_spaced.txt").read_text().splitlines()

    nlp = spacy.load("ja_ginza")

    html = "<html>\n"
    html += '<head><meta charset="utf-8"/></head>\n'
    html += "<body><h1>読み仮名（ルビ）つき声優統計コーパス音素バランス文</h1>\n"
    html += '<table border="1">\n'
    for kanji_line, yomi in zip(kanji_lines, yomi_lines):
        name, kanji = kanji_line.split(":")
        html += f"<tr><td style=\"padding: 1em\">{name.split('_')[1]}</td><td style=\"padding: 1em\">"

        hira_kanji = kata2hira(kanji)
        hira_yomi = kata2hira(yomi).replace(" ", "")

        i = 0
        new_hira_kanji = ""
        for token in nlp(kanji):
            s = None
            if token.pos_ == "ADP":
                if str(token) == "は":
                    s = "わ"
                elif str(token) == "へ":
                    s = "え"
            new_hira_kanji += hira_kanji[i : i + len(str(token))] if s is None else s
            i += len(str(token))

        hira_kanji = new_hira_kanji

        for tag, i1, i2, j1, j2 in SequenceMatcher(
            None, hira_kanji, hira_yomi
        ).get_opcodes():
            k = kanji[i1:i2]
            h = hira_kanji[i1:i2]
            y = hira_yomi[j1:j2]

            post = ""

            while True:
                if len(k) > 0 and k[0] == "、":
                    k = k[1:]
                    h = h[1:]
                    html += "、"
                    continue

                if len(k) > 0 and (k[-1] == "、" or k[-1] == "。"):
                    post += k[-1]
                    k = k[:-1]
                    h = h[:-1]
                    continue

                if (
                    len(k) > 0
                    and len(y) > 0
                    and (
                        (k[0] == "を" and y[0] == "お")
                        or (k[0] == "は" and y[0] == "わ")
                        or (k[0] == "へ" and y[0] == "え")
                    )
                ):
                    html += k[0]
                    k = k[1:]
                    h = h[1:]
                    y = y[1:]
                    continue

                if (
                    len(k) > 0
                    and len(y) > 0
                    and (
                        (k[-1] == "を" and y[-1] == "お")
                        or (k[-1] == "は" and y[-1] == "わ")
                        or (k[-1] == "へ" and y[-1] == "え")
                    )
                ):
                    post = k[-1] + post
                    k = k[:-1]
                    h = h[:-1]
                    y = y[:-1]
                    continue

                break

            if h == y:
                html += k
            elif y == "":
                html += k
            elif (
                (k == "を" and y == "お")
                or (k == "は" and y == "わ")
                or (k == "へ" and y == "え")
            ):
                html += k
            elif (
                h == "あ" or h == "い" or h == "う" or h == "え" or h == "お"
            ) and y == "ー":
                html += k
            else:
                ry = replace_nobashi(y)
                if ry[:2] == "おう" and (k[0] == "多" or k[0] == "大" or k[0] == "覆"):
                    ry = "おお" + ry[2:]
                html += f"<ruby>{k}<rt>{ry}</rt></ruby>"

            html += post

        html += "</td></tr>\n"

    html += "</table>\n"
    html += '<div>Made by: <a href="https://github.com/Hiroshiba">Hiroshiba</a></div>\n'
    html += "<div>License: CC-BY-SA 4.0</div>\n"
    html += (
        '<div>Link: <a href="https://voice-statistics.github.io/">声優統計コーパス</a></div>\n'
    )
    html += '<div>Link: <a href="https://sites.google.com/site/shinnosuketakamichi/publication/jsut">JSUT</a></div>\n'
    html += "</body></html>"

    Path("index.html").write_text(html)


def replace_nobashi(s: str):
    s = s.replace("あー", "ああ")
    s = s.replace("かー", "かあ")
    s = s.replace("がー", "があ")
    s = s.replace("さー", "さあ")
    s = s.replace("ざー", "ざあ")
    s = s.replace("たー", "たあ")
    s = s.replace("だー", "だあ")
    s = s.replace("なー", "なあ")
    s = s.replace("はー", "はあ")
    s = s.replace("ばー", "ばあ")
    s = s.replace("ぱー", "ぱあ")
    s = s.replace("まー", "まあ")
    s = s.replace("やー", "やあ")
    s = s.replace("らー", "らあ")
    s = s.replace("きゃー", "きゃあ")
    s = s.replace("ぎゃー", "ぎゃあ")
    s = s.replace("しゃー", "しゃあ")
    s = s.replace("じゃー", "じゃあ")
    s = s.replace("ちゃー", "ちゃあ")
    s = s.replace("ぢゃー", "ぢゃあ")
    s = s.replace("にゃー", "にゃあ")
    s = s.replace("ひゃー", "ひゃあ")
    s = s.replace("びゃー", "びゃあ")
    s = s.replace("ぴゃー", "ぴゃあ")
    s = s.replace("みゃー", "みゃあ")
    s = s.replace("りゃー", "りゃあ")

    s = s.replace("いー", "いい")
    s = s.replace("きー", "きい")
    s = s.replace("ぎー", "ぎい")
    s = s.replace("しー", "しい")
    s = s.replace("じー", "じい")
    s = s.replace("ちー", "ちい")
    s = s.replace("ぢー", "ぢい")
    s = s.replace("にー", "にい")
    s = s.replace("ひー", "ひい")
    s = s.replace("びー", "びい")
    s = s.replace("ぴー", "ぴい")
    s = s.replace("みー", "みい")
    s = s.replace("りー", "りい")

    s = s.replace("うー", "うう")
    s = s.replace("くー", "くう")
    s = s.replace("ぐー", "ぐう")
    s = s.replace("しー", "しう")
    s = s.replace("じー", "じう")
    s = s.replace("つー", "つう")
    s = s.replace("づー", "づう")
    s = s.replace("ぬー", "ぬう")
    s = s.replace("ふー", "ふう")
    s = s.replace("ぶー", "ぶう")
    s = s.replace("ぷー", "ぷう")
    s = s.replace("むー", "むう")
    s = s.replace("ゆー", "ゆう")
    s = s.replace("るー", "るう")
    s = s.replace("きゅー", "きゅう")
    s = s.replace("ぎゅー", "ぎゅう")
    s = s.replace("しゅー", "しゅう")
    s = s.replace("じゅー", "じゅう")
    s = s.replace("ちゅー", "ちゅう")
    s = s.replace("ぢゅー", "ぢゅう")
    s = s.replace("にゅー", "にゅう")
    s = s.replace("ひゅー", "ひゅう")
    s = s.replace("びゅー", "びゅう")
    s = s.replace("ぴゅー", "ぴゅう")
    s = s.replace("みゅー", "みゅう")
    s = s.replace("りゅー", "りゅう")

    s = s.replace("えー", "えい")
    s = s.replace("けー", "けい")
    s = s.replace("げー", "げい")
    s = s.replace("せー", "せい")
    s = s.replace("ぜー", "ぜい")
    s = s.replace("てー", "てい")
    s = s.replace("でー", "でい")
    s = s.replace("ねー", "ねい")
    s = s.replace("へー", "へい")
    s = s.replace("べー", "べい")
    s = s.replace("ぺー", "ぺい")
    s = s.replace("めー", "めい")
    s = s.replace("れー", "れい")

    s = s.replace("おー", "おう")
    s = s.replace("こー", "こう")
    s = s.replace("ごー", "ごう")
    s = s.replace("そー", "そう")
    s = s.replace("ぞー", "ぞう")
    s = s.replace("とー", "とう")
    s = s.replace("どー", "どう")
    s = s.replace("のー", "のう")
    s = s.replace("ほー", "ほう")
    s = s.replace("ぼー", "ぼう")
    s = s.replace("ぽー", "ぽう")
    s = s.replace("もー", "もう")
    s = s.replace("よー", "よう")
    s = s.replace("ろー", "ろう")
    s = s.replace("きょー", "きょう")
    s = s.replace("ぎょー", "ぎょう")
    s = s.replace("しょー", "しょう")
    s = s.replace("じょー", "じょう")
    s = s.replace("ちょー", "ちょう")
    s = s.replace("ぢょー", "ぢょう")
    s = s.replace("にょー", "にょう")
    s = s.replace("ひょー", "ひょう")
    s = s.replace("びょー", "びょう")
    s = s.replace("ぴょー", "ぴょう")
    s = s.replace("みょー", "みょう")
    s = s.replace("りょー", "りょう")

    return s


if __name__ == "__main__":
    main()
