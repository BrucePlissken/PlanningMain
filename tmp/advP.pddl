(define (problem pff) (:domain ad)
(:objects
    DudeAscii - player 
    farmer girl bailiff - npc
    goblin - monster
    farm town lair - location
    goblinTracks - info
    goblinhead - trophy
)

(:init
    (atLoc DudeAscii town)
    (hasTrack farm)
    (isAvailable DudeAscii)
    (canTrack DudeAscii)
    (atLoc girl lair)
    (atLoc farmer farm)
    (trackInfo goblinTracks farm lair)
    (isSecret lair)
    (isSecret goblinTracks)
    (atLoc goblin lair)
    (isSus goblin)
    (isBound girl)
    (knowInfo farmer goblinTracks)
    (haveBodyPart goblin goblinhead)
    (atLoc bailiff town)
)
(:goal 
    (and
    (atLoc Girl farm)
    (haveItem bailiff goblinhead)
    )
)
(:metric minimize (total-cost))

)
