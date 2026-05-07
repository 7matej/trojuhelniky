from rule import Rule
from pravidla import promene

#nesmí zde být použita pravidla vedoucí k rozvětvení!

ban = Rule(promene)

@ban.rule("r", "r", 1)
def kruz_opsana(r):
    return r
@ban.rule("S", "S", 1)
def obsah(S):
    return S


ban.ban("uhel", 0, "uhel", 1, "uhel", 2)
ban.ban("r", 0, "strana", 0, "uhel", 0)
ban.ban("h", 0, "strana", 1, "uhel", 2)
ban.ban("h", 0, "S", 0, "strana", 0)