;Header and description
(define (domain cpd)
;remove requirements that are not needed
(:requirements :strips :typing :conditional-effects :negative-preconditions :equality :disjunctive-preconditions :universal-preconditions)
(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    character item location - omni
    agent - character
    consumable weapon - item
)
; un-comment following line if constants are needed
;(:constants )
(:predicates ;todo: define predicates here
    (inventory ?item - item ?char - character)
    (whereabouts ?loc - location ?char - character)
    (atloc ?o - omni ?loc - location)
    (isdead ?char - character)
    (isasleep ?char - character)
)
(:functions ;todo: define numeric functions here
)
;define actions here
(:action pick_up
    :parameters (?char - agent ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (atloc ?item ?loc))
    :effect (and (not (atloc ?item ?loc)) (inventory ?item ?char))
)
(:action move
    :parameters (?char - agent ?from ?to - location)
    :precondition (and (whereabouts ?from ?char))
    :effect (and (not (whereabouts ?from ?char)) (whereabouts ?to ?char))
)
(:action give
    :parameters (?char1 - agent ?char2 - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (inventory ?item ?char1))
    :effect (and (not (inventory ?item ?char1)) (inventory ?item ?char2))
)
(:action drop
    :parameters (?char - agent ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (inventory ?item ?char))
    :effect (and (not (inventory ?item ?char)) (atloc ?item ?loc))
)
(:action kill
    :parameters (?char - agent ?vict - character ?wep - weapon ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (whereabouts ?loc ?vict) (inventory ?wep ?char))
    :effect (and (isdead ?vict))
)
(:action take
    :parameters (?char1 - agent ?char2 - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (inventory ?item ?char2) (or (isdead ?char2) (isasleep ?char2)))
    :effect (and (not (inventory ?item ?char2)) (inventory ?item ?char1))
)
(:action wt_for_sleep
    :parameters (?char1 - agent ?char2 - character ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (not (whereabouts ?loc ?char2)))
    :effect (and (isasleep ?char2))
)
)