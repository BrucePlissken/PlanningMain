(define (domain lrrh)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions :typing :equality :negative-preconditions)
(:types
    location - info
    location
    hero victim antagonist - character
)
(:predicates
    (atLoc ?char - character ?loc - location)
    (isDead ?char - character)
    (isSwallowed ?vict ?mon - character)
    (knowInfo ?char - character ?inf - info)
    (isConnected ?loc1 ?loc2 - location)
    (cantMove ?char - character)
    (canEat ?char - antagonist)
    (areEnemies ?char1 ?char2 - character)
)
(:action move
    :parameters (?char - character ?from ?to - location)
    :precondition (and (atLoc ?char ?from) (knowInfo ?char ?to) (or (isConnected ?from ?to) (isConnected ?to ?from)) (not (= ?from ?to)) (not (cantMove ?char))
    )
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    )
)
(:action slay
    :parameters (?char - hero ?mon - antagonist ?loc - location)
    :precondition (and (atLoc ?char ?loc) (atLoc ?mon ?loc) (not (isDead ?char)) (not (isSwallowed ?char ?mon)) (not (= ?char ?mon))
    )
    :effect (and (isDead ?mon)
    (forall (?vict - character) (when (isSwallowed ?vict ?mon) (not (isSwallowed ?vict ?mon))))
    )
)
(:action askInfo
    :parameters (?char1 ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)) (not (areEnemies ?char2 ?char1))
    )
    :effect (and (knowInfo ?char1 ?inf)
    )
)
(:action swallow
    :parameters (?vict - victim ?mon - antagonist ?loc - location)
    :precondition (and (atloc ?vict ?loc) (atLoc ?mon ?loc) (canEat ?mon)
    )
    :effect (and (isSwallowed ?vict ?mon) (cantMove ?mon)
    )
)
)