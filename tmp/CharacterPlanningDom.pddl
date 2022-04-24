;Header and description
(define (domain cpd)
;remove requirements that are not needed
(:requirements :strips :typing :conditional-effects :negative-preconditions :equality :disjunctive-preconditions)
(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    character item location - omni
    agent npc - character
    consumable - item
)
; un-comment following line if constants are needed
;(:constants )
(:predicates ;todo: define predicates here
    (inventory ?char - character ?item - item)
    (whereabouts ?loc - location ?char - character)
    (atloc ?o - omni ?loc - location)
    (isdead ?char - character)
)
(:functions ;todo: define numeric functions here
)
;define actions here
(:action pick_up
    :parameters (?char - agent ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (atloc ?item ?loc))
    :effect (and (not (atloc ?item ?loc)) (inventory ?char ?item))
)
(:action move
    :parameters (?char - agent ?from ?to - location)
    :precondition (and (whereabouts ?from ?char))
    :effect (and (not (whereabouts ?from ?char)) (whereabouts ?to ?char))
)
(:action give
    :parameters (?char1 - agent ?char2 - character ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char1) (whereabouts ?loc ?char2) (inventory ?char1 ?item))
    :effect (and (not (inventory ?char1 ?item)) (inventory ?char2 ?item))
)
(:action drop
    :parameters (?char - agent ?item - item ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (inventory ?char ?item))
    :effect (and (not (inventory ?char ?item)) (atloc ?item ?loc))
)
(:action kill
    :parameters (?char - agent ?vict - character ?loc - location)
    :precondition (and (whereabouts ?loc ?char) (whereabouts ?loc ?vict))
    :effect (and (isdead ?vict))
)
)