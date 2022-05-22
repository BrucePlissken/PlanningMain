(define (domain adc)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions :typing :equality :negative-preconditions :conditional-effects)
(:types
    thing location character info - omni
    player npc victim vilain - character
    site area - location
    consumable weapon trophy item - thing
)

(:predicates
    (atLoc ?char - character ?loc - location)
    (onGround ?i - thing ?loc - location)
    (canTrack ?char - character)
    (havething ?char - character ?i - thing)
    (inArea ?site - location ?area - area)
    (trackInfo ?inf - info ?loc - location ?lair - location)
    (isSus ?char - character)
    (isDead ?char - character)
    (isBound ?char - character)
    (haveBodyPart ?char - character ?bp - trophy)
    (follows ?follower ?leader - character)
    (isMissing ?char - character)
    (isLair ?char - character ?loc - location)
    (isDestination ?char - character ?loc - location)
    (canCut ?thing - thing)
    (knowInfo ?char - character ?omni - omni)
    (isUnknown ?omni - omni)
    (want ?char - character ?omni - omni)
    (requested ?char1 ?char2 - character ?omni - omni)
    (isrelated ?char1 ?char2 - character)
)
(:functions
    (total-cost) - number
)
(:action move
    :parameters (?char - player ?from - location ?to - site ?area - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (inArea ?to ?area) (or (= ?from ?area) (inArea ?from ?area)) (not (isDead ?char)))
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    )
)
(:action travel
    :parameters (?char - player ?from - location ?to - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (not (isDead ?char)))
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    )
)
(:action investigatetrack
    :parameters (?char - character ?inf - info ?loc ?lair - location)
    :precondition (and (atLoc ?char ?loc) (canTrack ?char) (trackInfo ?inf ?loc ?lair) (not (isUnknown ?inf)) (not (isDead ?char)))
    :effect (and (not (isUnknown ?lair))
    )
)
(:action slay
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isSus ?char2) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)))
    :effect (and (isDead ?char2)
    (forall (?i - thing) (when (havething ?char2 ?i) (and (onGround ?i ?loc) (not (havething ?char2 ?i)))))
    )
)
(:action gowith
    :parameters (?follower - victim ?leader - character ?loc - location)
    :precondition (and (atLoc ?leader ?loc) (atLoc ?follower ?loc) (not (= ?follower ?leader)) (not (isDead ?follower)) (not (isDead ?leader))
                    (or (and (not (isSus ?follower)) (not (isBound ?follower))) (and (isSus ?follower) (isBound ?follower)))
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (follows ?follower ?leader)
    )
)
(:action pickup
    :parameters (?char - character ?i - thing ?loc - location)
    :precondition (and (onGround ?i ?loc) (atLoc ?char ?loc) (not (isDead ?char))) 
    :effect (and (havething ?char ?i) (not (onGround ?i ?loc))
    )
)
(:action untie
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isBound ?char2) (not (isDead ?char1)) (not (isDead ?char2))
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (not (isBound ?char2))
    )
)
(:action askInfo
    :parameters (?char1 - player ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)))
    :effect (and (not (isUnknown ?inf))
    )
)
(:action give
    :parameters (?char1 ?char2 - character ?i - thing ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (havething ?char1 ?i) (not (isDead ?char1)) (not (isDead ?char2)) (not (isSus ?char1)) (not (= ?char1 ?char2))) 
    :effect (and (havething ?char2 ?i) (not (havething ?char1 ?i))
    )
)
(:action deliver
    :parameters (?char1 ?char2 - character ?i - thing ?loc - location)
    :precondition (and (requested ?char2 ?char1 ?i) (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (havething ?char1 ?i) (not (isDead ?char1)) (not (isDead ?char2)) (not (isSus ?char1)) (not (= ?char1 ?char2))) 
    :effect (and (havething ?char2 ?i) (not (havething ?char1 ?i)) (not (requested ?char2 ?char1 ?i))
    )
)
(:action dismember
    :parameters (?char1 - player ?char2 - character ?bp - trophy ?loc - location ?blad - thing)
    :precondition (and (atLoc ?char1 ?loc) (havething ?char1 ?blad) (canCut ?blad) (atLoc ?char2 ?loc) (not (isDead ?char1)) (isDead ?char2) (haveBodyPart ?char2 ?bp))
    :effect (and (onGround ?bp ?loc) (not (haveBodyPart ?char2 ?bp))
    )
)
(:action endscort
    :parameters (?char1 ?char2 - character ?loc - location)
    :precondition (and (isDestination ?char2 ?loc) (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (follows ?char2 ?char1) (not (= ?char1 ?char2)) (not (isDead ?char1)))
    :effect (and (not (isMissing ?char2)) (not (follows ?char2 ?char1)) (not (isDestination ?char2 ?loc))
    (forall (?char - character) (when (and (atLoc ?char ?loc) (requested ?char ?char1 ?char2)) (not (requested ?char ?char1 ?char2)) )  )
    )
)
(:action kidnap
    :parameters (?mon - vilain ?vict - victim ?from ?to - location)
    :precondition (and (not (isMissing ?vict)) (not (isDead ?mon)) (atLoc ?vict ?from) (isLair ?mon ?to) (not (= ?mon ?vict)))
    :effect (and (atLoc ?vict ?to) (isMissing ?vict) (isDestination ?vict ?from) (isBound ?vict) (not (atLoc ?vict ?from))
    (forall (?char - character) (when (or (isrelated ?char ?vict) (isrelated ?vict ?char)) (want ?char ?vict)))
    )
)
(:action request
    :parameters (?char1 - character ?char2 - player ?loc - location ?target - omni)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (not  (isDead ?char1)) (not (isDead ?char2)) (want ?char1 ?target) )
    :effect (and (requested ?char1 ?char2 ?target) (not (want ?char1 ?target)))       
    )
)   