(define (problem pff) (:domain ad)
(:objects
    DudeAscii - player 
    farmer girl bailiff lord lady priest cryptkeeper - npc
    goblin - monster
    farm town manor lair castle kingdom - location
    goblinTracks - info
    dagger pole - weapon
    tonic - consumable
    goblinhead - trophy
)
(:init
    (haveItem goblin tonic)
    (onGround pole farm)
    (atLoc lord castle)
    (atLoc lady lair)
    (isSus lady)
    (atloc dudeascii town)
    (hastrack farm)
    (isavailable dudeascii)
    (cantrack dudeascii)
    (atloc girl lair)
    (atloc farmer farm)
    (trackinfo goblintracks farm lair)
    (isUnknown lair)
    (isUnknown goblintracks)
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
    )
)
(:metric minimize (total-cost))

)