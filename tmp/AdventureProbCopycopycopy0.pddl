(define (problem pff) (:domain adc)
(:objects
    goblinTracks grimmyIsAgoblin ladyIsVamp lordIsCreep - info
    DudeAscii - player
    farmer bailiff lord lady priest cryptkeeper - npc
    girl - victim
    grimmyTheGoblin - vilain
    town castle forrest - area
    farm manor lair church keep crypt cellar - site
    dagger pole - weapon
    tonic - consumable
    goblinhead vampireHeart - trophy
)
(:init
    (want bailiff goblinhead)
    (islair lady crypt)
    (islair lord cellar)
    (islair grimmythegoblin lair)
    (isunknown crypt)
    (isunknown cellar)
    (isunknown lair)
    (inarea cellar castle)
    (inarea crypt town)
    (inarea lair forrest)
    (knowinfo priest crypt)
    (knowinfo lady cellar)
    (isunknown ladyisvamp)
    (isunknown goblintracks)
    (inarea manor town)
    (inarea farm town)
    (inarea church town)
    (inarea keep castle)
    (atloc lord keep)
    (atloc lady keep)
    (atloc farmer farm)
    (atloc grimmythegoblin lair)
    (atloc bailiff manor)
    (atloc dudeascii town)
    (atloc priest church)
    (atloc girl farm)
    (knowinfo farmer goblintracks)
    (trackinfo goblintracks farm lair)
    (cantrack dudeascii)
    (havething lord dagger)
    (cancut dagger)
    (onground pole farm)
    (havething grimmythegoblin tonic)
    (issus grimmythegoblin)
    (havebodypart grimmythegoblin goblinhead)
    (havebodypart lady vampireheart)
)
(:goal
    (and (atloc priest crypt)
)
  )
)