(define (problem pff) (:domain ad)
(:objects
    DudeAscii - player 
    farmer girl bailiff lord lady priest cryptkeeper grimmyTheGoblin - npc
    town castle forrest - area
    farm manor lair church keep - site
    goblinTracks grimmyIsAgoblin - info
    dagger pole - weapon
    tonic - consumable
    goblinhead - trophy
    goblin creep vampire - monster
)
(:init
    (inArea manor town)
    (inArea farm town)
    (inArea church town)
    (inArea lair forrest)
    (inArea keep castle)
    (isMonster grimmyTheGoblin goblin grimmyIsAgoblin)
    (havething grimmyTheGoblin tonic)
    (onGround pole farm)
    (atLoc lord keep)
    (atLoc lady lair)
    (isSus lady)
    (atloc dudeascii town)
    (hastrack farm)
    (isavailable dudeascii)
    (cantrack dudeascii)
    (atloc girl farm)
    (atloc farmer farm)
    (trackinfo goblintracks farm lair)
    (isUnknown lair)
    (isUnknown goblintracks)
    (atloc grimmyTheGoblin lair)
    (isSus grimmyTheGoblin)
    (knowinfo farmer goblintracks)
    (havebodypart grimmyTheGoblin goblinhead)
    (atloc bailiff manor)
    (havething lord dagger)
    (canCut dagger)
    (isLair grimmyTheGoblin lair)
)

(:goal 
    (and
    (isMissing girl)
    )
)

)