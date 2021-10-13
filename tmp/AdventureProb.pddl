(define (problem pff) (:domain ad)
(:objects
    DudeAscii - player 
    farmer girl bailiff lord lady priest cryptkeeper - npc
    goblin - monster
    farm town manor lair castle kingdom - location
    goblinTracks - info
    goblinhead - trophy
    dagger - weapon
)
(:init
    (isSus lord)
    (atLoc lord castle)
    (atLoc lady castle)
    (atloc dudeascii town)
    (hastrack farm)
    (isavailable dudeascii)
    (cantrack dudeascii)
    (atloc girl lair)
    (atloc farmer farm)
    (trackinfo goblintracks farm lair)
    (issecret lair)
    (issecret goblintracks)
    (atloc goblin lair)
    (isbound girl)
    (isSus goblin)
    (knowinfo farmer goblintracks)
    (havebodypart goblin goblinhead)
    (atloc bailiff manor)
    (haveItem lord dagger)
    (canCut dagger)
)

 (:goal 
    (and
    (atLoc girl farm)
    (haveItem bailiff goblinhead)
    )
)
(:metric minimize (total-cost))

)