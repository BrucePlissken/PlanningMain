(define (domain lrrh)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions :typing :equality :negative-preconditions :conditional-effects)
(:types
    location - info
    location
    character
)
(:predicates
    (atLoc ?char - character ?loc - location)
    (isDead ?char - character)
    (isSwallowed ?vict ?mon - character)
    (unaware ?char - character ?inf - info)
    (isConnected ?loc1 ?loc2 - location)
    (cantMove ?char - character)
    (canEat ?char - character)
    (areEnemies ?char1 ?char2 - character)
    (isSaved ?char - character)
    (haveAxe ?char - character)
)
(:action move
    :parameters (?char - character ?from ?to - location)
    :precondition (and (atLoc ?char ?from) (not (isDead ?char)) (not (unaware ?char ?to)) (not (= ?from ?to)) (not (cantMove ?char)) (or (isConnected ?from ?to) (isConnected ?to ?from))
    )
    :effect (and (atLoc ?char ?to) (not (atLoc ?char ?from))
    )
)
(:action slay
    :parameters (?char - character ?mon - character ?loc - location)
    :precondition (and (atLoc ?char ?loc) (atLoc ?mon ?loc) (haveAxe ?char) (not (isDead ?char)) (not (isDead ?mon)) (not (isSwallowed ?char ?mon)) (not (= ?char ?mon))
    )
    :effect (and (isDead ?mon)
    (forall (?vict - character) (when (isSwallowed ?vict ?mon) (and (isSaved ?vict) (not (isSwallowed ?vict ?mon)) (not (isDead ?vict)) )))
    )
)
(:action askInfo
    :parameters (?char1 - character ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (unaware ?char1 ?inf) (not (unaware ?char2 ?inf)) (not (isDead ?char1)) (not (isDead ?char2)) (not (areEnemies ?char2 ?char1))
    )
    :effect (and (not (unaware ?char1 ?inf))
    )
)
(:action swallow
    :parameters (?mon - character ?vict - character ?loc - location)
    :precondition (and (atLoc ?vict ?loc) (atLoc ?mon ?loc) (canEat ?mon) (not (= ?mon ?vict)) (not (isDead ?mon))
    (forall (?char - character) (or (not (atLoc ?char ?loc)) (not (haveAxe ?char)) ))
    )
    :effect (and (isSwallowed ?vict ?mon) (cantMove ?mon) (isDead ?vict) 
    )
)
)