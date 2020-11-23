import re
from difflib import SequenceMatcher
from pathlib import Path

import spacy
from julius4seg.sp_inserter import kata2hira


def main():
    html = Path("index.html").read_text()

    kanji_lines = Path("transcript_utf8.txt").read_text().splitlines()
    yomi_lines = Path("voiceactoress100_spaced.txt").read_text().splitlines()

    for i, m in enumerate(
        re.compile(r"<td.*?>.*?</td><td.*?>(.*?)</td>").finditer(html)
    ):
        name, kanji = kanji_lines[i].split(":")
        yomi = kata2hira(yomi_lines[i]).replace(" ", "")

        one_html = m.group(1)

        text = re.compile(r"<ruby>(.*?)<rt>.*?</rt></ruby>").sub(r"\1", one_html)
        assert text == kanji

        text = (
            replace_nobashi(
                re.compile(r"<ruby>.*?<rt>(.*?)</rt></ruby>").sub(r"\1", one_html)
            )
            .replace("おお", "おー")
            .replace("とお", "とー")
            .replace("、", "")
            .replace("。", "")
        )
        text = kata2hira(text)

        old_text = text
        text = ""
        for tag, i1, i2, j1, j2 in SequenceMatcher(None, old_text, yomi).get_opcodes():
            t = old_text[i1:i2]
            y = yomi[j1:j2]
            if t == y:
                text += t
            elif t == "は" and y == "わ":
                text += y
            elif t == "へ" and y == "え":
                text += y
            elif t == "を" and y == "お":
                text += y
            elif t == "づ" and y == "ず":
                text += y
            elif t == "いう" and y == "ゆー":
                text += y
            elif (t == "ー" and (y == "あ" or y == "い" or y == "う")) or (
                (t == "あ" or t == "い" or t == "う") and y == "ー"
            ):
                print("true?")
                print("　" * i1 + "・")
                print(old_text)
                print(yomi)
                text += y
            else:
                raise ValueError

        assert text == yomi


def replace_nobashi(s: str):
    s = s.replace("ああ", "あー")
    s = s.replace("かあ", "かー")
    s = s.replace("があ", "がー")
    s = s.replace("さあ", "さー")
    s = s.replace("ざあ", "ざー")
    s = s.replace("たあ", "たー")
    s = s.replace("だあ", "だー")
    s = s.replace("なあ", "なー")
    s = s.replace("はあ", "はー")
    s = s.replace("ばあ", "ばー")
    s = s.replace("ぱあ", "ぱー")
    s = s.replace("まあ", "まー")
    s = s.replace("やあ", "やー")
    s = s.replace("らあ", "らー")
    s = s.replace("きゃあ", "きゃー")
    s = s.replace("ぎゃあ", "ぎゃー")
    s = s.replace("しゃあ", "しゃー")
    s = s.replace("じゃあ", "じゃー")
    s = s.replace("ちゃあ", "ちゃー")
    s = s.replace("ぢゃあ", "ぢゃー")
    s = s.replace("にゃあ", "にゃー")
    s = s.replace("ひゃあ", "ひゃー")
    s = s.replace("びゃあ", "びゃー")
    s = s.replace("ぴゃあ", "ぴゃー")
    s = s.replace("みゃあ", "みゃー")
    s = s.replace("りゃあ", "りゃー")

    s = s.replace("いい", "いー")
    s = s.replace("きい", "きー")
    s = s.replace("ぎい", "ぎー")
    s = s.replace("しい", "しー")
    s = s.replace("じい", "じー")
    s = s.replace("ちい", "ちー")
    s = s.replace("ぢい", "ぢー")
    s = s.replace("にい", "にー")
    s = s.replace("ひい", "ひー")
    s = s.replace("びい", "びー")
    s = s.replace("ぴい", "ぴー")
    s = s.replace("みい", "みー")
    s = s.replace("りい", "りー")

    s = s.replace("うう", "うー")
    s = s.replace("くう", "くー")
    s = s.replace("ぐう", "ぐー")
    s = s.replace("しう", "しー")
    s = s.replace("じう", "じー")
    s = s.replace("つう", "つー")
    s = s.replace("づう", "づー")
    s = s.replace("ぬう", "ぬー")
    s = s.replace("ふう", "ふー")
    s = s.replace("ぶう", "ぶー")
    s = s.replace("ぷう", "ぷー")
    s = s.replace("むう", "むー")
    s = s.replace("ゆう", "ゆー")
    s = s.replace("るう", "るー")
    s = s.replace("きゅう", "きゅー")
    s = s.replace("ぎゅう", "ぎゅー")
    s = s.replace("しゅう", "しゅー")
    s = s.replace("じゅう", "じゅー")
    s = s.replace("ちゅう", "ちゅー")
    s = s.replace("ぢゅう", "ぢゅー")
    s = s.replace("にゅう", "にゅー")
    s = s.replace("ひゅう", "ひゅー")
    s = s.replace("びゅう", "びゅー")
    s = s.replace("ぴゅう", "ぴゅー")
    s = s.replace("みゅう", "みゅー")
    s = s.replace("りゅう", "りゅー")

    s = s.replace("えい", "えー")
    s = s.replace("けい", "けー")
    s = s.replace("げい", "げー")
    s = s.replace("せい", "せー")
    s = s.replace("ぜい", "ぜー")
    s = s.replace("てい", "てー")
    s = s.replace("でい", "でー")
    s = s.replace("ねい", "ねー")
    s = s.replace("へい", "へー")
    s = s.replace("べい", "べー")
    s = s.replace("ぺい", "ぺー")
    s = s.replace("めい", "めー")
    s = s.replace("れい", "れー")

    s = s.replace("おう", "おー")
    s = s.replace("こう", "こー")
    s = s.replace("ごう", "ごー")
    s = s.replace("そう", "そー")
    s = s.replace("ぞう", "ぞー")
    s = s.replace("とう", "とー")
    s = s.replace("どう", "どー")
    s = s.replace("のう", "のー")
    s = s.replace("ほう", "ほー")
    s = s.replace("ぼう", "ぼー")
    s = s.replace("ぽう", "ぽー")
    s = s.replace("もう", "もー")
    s = s.replace("よう", "よー")
    s = s.replace("ろう", "ろー")
    s = s.replace("きょう", "きょー")
    s = s.replace("ぎょう", "ぎょー")
    s = s.replace("しょう", "しょー")
    s = s.replace("じょう", "じょー")
    s = s.replace("ちょう", "ちょー")
    s = s.replace("ぢょう", "ぢょー")
    s = s.replace("にょう", "にょー")
    s = s.replace("ひょう", "ひょー")
    s = s.replace("びょう", "びょー")
    s = s.replace("ぴょう", "ぴょー")
    s = s.replace("みょう", "みょー")
    s = s.replace("りょう", "りょー")

    return s


if __name__ == "__main__":
    main()
