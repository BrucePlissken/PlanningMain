;Header and description
(define (domain fairy_tale_dom_ex)
;remove requirements that are not needed
(:requirements :typing :conditional-effects :negative-preconditions :strips :disjunctive-preconditions :equality :action-costs)
(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    character item location - omni
    consumable weapon - item
    monster - character
)
; un-comment following line if constants are needed
(:predicates ;todo: define predicates here
    (inventory ?item - item ?char - character)
    (whereabouts ?loc - location ?char - character)
    (hate ?char1 - character ?char2 - character)
    (inside ?vict - character ?mon - monster)
    (oblivious ?o - omni ?char - character)
    (atloc ?o - omni ?loc - location)
    (isdead ?char - character)
    (isasleep ?char - character)
    (cangobble ?mon - character)
    (imobile ?char - character)
    (issaved ?vict - character)
)
(:functions ;todo: define numeric functions here
    (total-cost)
)
;define actions here
(:action move
    :parameters (?char - character ?from ?to ?by - location)
    :precondition (and (whereabouts ?from ?char) (not (imobile ?char)) (not (isdead ?char)) (not (isasleep ?char)) (not (oblivious ?to ?char)) (or (and (= ?to ?by) (atloc ?from ?to)) (and (= ?from ?by) (atloc ?to ?from))))
    :effect (and (not (whereabouts ?from ?char)) (whereabouts ?to ?char)
    (increase (total-cost) 1)
    )
)
(:action pick_up
    :parameters (?char - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (atloc ?item ?loc) (not (isdead ?char)) (not (isasleep ?char)))
    :effect (and (not (atloc ?item ?loc)) (inventory ?item ?char)
    (increase (total-cost) 1)
    )
)
(:action drop
    :parameters (?char - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (inventory ?item ?char))
    :effect (and (not (inventory ?item ?char)) (atloc ?item ?loc)
    (increase (total-cost) 1)
    )
)
(:action give
    :parameters (?char1 - character ?char2 - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (inventory ?item ?char1) (not (isdead ?char1)) (not (isasleep ?char1)) (not (hate ?char1 ?char2)))
    :effect (and (not (inventory ?item ?char1)) (inventory ?item ?char2)
    (increase (total-cost) 1)
    )
)
(:action kill
    :parameters (?char - character ?vict - character ?wep - weapon ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (whereabouts ?loc ?vict) (inventory ?wep ?char) (not (isdead ?char)) (not (isasleep ?char)))
    :effect (and (isdead ?vict)
    (increase (total-cost) 1)
    )
)
(:action take
    :parameters (?char1 - character ?char2 - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (inventory ?item ?char2) (not (isdead ?char1)) (not (isasleep ?char1)) (or (isdead ?char2) (isasleep ?char2)))
    :effect (and (not (inventory ?item ?char2)) (inventory ?item ?char1)
    (increase (total-cost) 1)
    )
)
(:action gotosleep
    :parameters (?char - character ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (not (isasleep ?char)) (not (isdead ?char))
    (forall (?char1 - character) (or (not (whereabouts ?loc ?char1)) (not (hate ?char ?char1))) )
    )
    :effect (and (isasleep ?char)
    (increase (total-cost) 1)
    )
)
(:action askInfo
    :parameters (?char1 - character ?char2 - character ?loc - location ?inf - omni)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (oblivious ?inf ?char1) (not (oblivious ?inf ?char2)) (not (isDead ?char1)) (not (isDead ?char2)) (not (hate ?char1 ?char2))
    (not (isasleep ?char1)) (not (isasleep ?char2))
    )
    :effect (and (not (oblivious ?inf ?char1))
    (increase (total-cost) 1)
    )
)
(:action swallow
    :parameters (?mon - monster ?vict - character ?loc - location)
    :precondition (and (whereabouts ?loc ?vict) (whereabouts ?loc ?mon) (cangobble ?mon) (not (= ?mon ?vict)) (not (hate ?mon ?vict)) (not (isDead ?mon)) (not (isasleep ?mon)) (not (inside ?vict ?mon)) (not (issaved ?vict))
    (forall (?char - character)  (or (not (whereabouts ?loc ?char)) (not (hate ?mon ?char))) )
    )
    :effect (and (inside ?vict ?mon) (imobile ?mon) (isasleep ?vict)
    (increase (total-cost) 1)
    )
)
(:action cesarean
    :parameters (?char - character ?mon - monster ?bab - character ?cut - weapon ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (whereabouts ?loc ?mon) (inventory ?cut ?char) (inside ?bab ?mon) (not (= ?char ?mon)) (not (isasleep ?char)) (not (isdead ?char)) (isasleep ?mon))
    :effect (and (not (inside ?bab ?mon)) (issaved ?bab)
    (increase (total-cost) 1)
    )
)
)