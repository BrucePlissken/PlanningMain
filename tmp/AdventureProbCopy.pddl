(define (problem pff) (:domain adc)
(:objects
    goblinTracks grimmyIsAgoblin ladyIsVamp lordIsCreep - concept
    DudeAscii - player 
    farmer girl bailiff lord lady priest cryptkeeper grimmyTheGoblin - npc
    town castle forrest - area
    farm manor lair church keep crypt cellar - site
    dagger pole - weapon
    tonic - consumable
    goblinhead vampireHeart - trophy
    goblin creep vampire - monster
)
(:init
    (islair lady crypt)
    (islair lord cellar)
    (islair grimmythegoblin lair)
    (isunknown crypt)
    (isunknown cellar)
    (isUnknown lair)
    (inarea cellar castle)
    (inarea crypt town)
    (inarea lair forrest)
    (knowInfo priest crypt)
    (knowInfo lady cellar)
    (isunknown ladyisvamp)
    (isUnknown goblintracks)
    (inarea manor town)
    (inarea farm town)
    (inarea church town)
    (inarea keep castle)
    (isMonster grimmythegoblin goblin grimmyisagoblin)
    (isMonster lord creep lordIsCreep)
    (ismonster lady vampire ladyisvamp)
    (atloc lord keep)
    (atloc lady keep)
    (atloc farmer farm)
    (atloc grimmythegoblin lair)
    (atloc bailiff manor)
    (atloc dudeascii town)
    (atLoc priest church)
    (atloc girl farm)
    (knowinfo farmer goblintracks)
    (trackinfo goblintracks farm lair)
    (isavailable dudeascii)
    (cantrack dudeascii)
    (havething lord dagger)
    (cancut dagger)
    (onground pole farm)
    (havething grimmyTheGoblin tonic)
    (isSus grimmyTheGoblin)
    (havebodypart grimmythegoblin goblinhead)
    (havebodypart lady vampireHeart)
)
(:goal
    (isMissing girl)
  )
(:metric minimize (total-cost))
)