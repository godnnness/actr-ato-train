
(clear-all)

(defvar *show-trace* t)

(defun show-trace () (setf *show-trace* t) (sgp :v t))
(defun hide-trace () (setf *show-trace* nil) (sgp :v nil))

(define-model SF-player

  ;;; tell it where the game server is
  (sgp-fct (list :sf-host *server-name*))
  #+sfapi (sgp-fct (list :sf-server-type *server-type*))
  (sgp :p-count t)
  (sgp-fct (list :v *show-trace*))

  (sgp :er t :esc t :egs .0001 :ol t :lf .1  :ans .01 :rt -1 :pct nil :trace-detail low)
  ;; Temporal module's noise
  (eval `(sgp :sf-data-hook ,*data-hook*))
  (sgp :do-not-harvest game-state)


  (specify-compilation-buffer-type game-state perceptual)

;; Temporal module's noise
  (sgp :TIME-NOISE .005)

 ;; Motor setup, timing, and randomization
  (sgp :randomize-time 3)
  (sgp :dual-execution-stages t)
  (sgp :MOTOR-FEATURE-PREP-TIME 0.020)
  (sgp :MOTOR-INITIATION-TIME .020)
  (sgp :hold-until-timing .025)

  ;; visual configuration
  (sgp :test-feats nil :visual-movement-tolerance 2 :do-not-harvest visual)

  (chunk-type gamestate x y orientation vx vy ship-alive status game  ;common
               offaim  moving-angle current-angle future-angle r1 r2 ship-speed   ;spacetrack
                time-to-outer thrust-angle vulnerability FORTRESS-ANGLE fortress-alive outward prop-to-big speed)   ;space fortess
  (chunk-type goal step state nextstep target aim game thrust-time;common
              rectangle  offaim  press-point stop-angle ship-speed ;spacetrack
              time-to-outer time-thresh dist-thresh vulnerability last-action outward prop-to-big speed) ;space fortess
  (chunk-type operator pre action arg1 result post  fail success)
  (chunk-type tracker rectangle death bad-aim good-aim
              hit miss badspeed goodspeed bighexdeath shelldeath smallhexdeath)
  (chunk-type mapping function key)

(default-chunks '(yes no speed adjust offaim turn-to-point test-dimension pressing-d pressing-key pressing-left down target-angle
                      THRUST-TO-TURNTAP-THRUST death rectangle press-point stop-angle tapthrust TAPPING-KEY pressing-a
                      CALCULATE-TURN-ANGLE maketurn2 test-speed  start done connected play start-playing-again do-step game-over
                      start-playing current-angle future-angle pressing-thrust tap-key thrust-to-turn ship-speed
                      NOFORTRESS FORTRESS-ALIVE TESTOBJECT DELAY? CHECK-DELAY ANGLE fortress-angle  double-space-bar
                             thrust thrust-angle increment-angle decrement-angle TIME-TO-OUTER space-bar shooting vulnerability? thrusting
                             double-spacebar state-changed reset hit time-thresh bighexdeath spacebar test-object prop-to-big
                             kill  shelldeath smallhexdeath thrust-time miss badspeed goodspeed))

(add-dm


(w isa mapping function thrust key w)
(a isa mapping function counterclockwise key a)
(d isa mapping function clockwise key d)
)
(eval (cons 'add-dm *instructions*))


(sgp :ul t  :epl t :egs .05 :alpha .2 :iu 9  )


(eval `(sgp :alpha ,*alpha*))
(eval `(sgp :initial-temp ,*factor*))

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; General productions for playing a SF-style game

    ;;; This production continues play at the very beginning


  (p get-started
     "Make sure game is running"
     ?game>
       game-state connected
     ?goal>
       buffer empty
     ?imaginal>
       state free
     ?game-state>
       state free
     ==>
     +goal>
         isa goal
         state start-playing
     +imaginal>
        isa tracker
     +game-state>
        isa gamestate)

   ;;; This production continues play for another game.
(p get-started-again
     "Make sure game is running"
     ?game>
       game-state connected
    =game-state>
       ship-alive yes
       game =game
     =goal>
       state game-over
       game =game
==>
    =game-state>
      status nil
     =goal>
       state start-playing-again
       rectangle nil)

(p get-started-new-game
     "Make sure game is running"
     ?game>
       game-state connected
    =game-state>
       ship-alive yes
       game =game
     =goal>
       state game-over
      - game =game
     ==>
     =goal>
         isa goal
         state start-playing
     +imaginal>
        isa tracker
     +game-state>
        isa gamestate)


;initiates for first game of space track
(p start-playing-spacetrack
     "once the ship is visible get going"
     =goal>
       isa goal
       state start-playing
     -  game spacetrack
    =game-state>
        game spacetrack
==>
     +tracker>
         control-slot aim
         good-slot rectangle
         bad-slot death
         min 3
         max 20.0
         bad-weight -1
     +tracker>
         control-slot ship-speed
         good-slot rectangle
         bad-slot death
         min 1.0
         max 4.0
         bad-weight -1
     +tracker>
         control-slot press-point
         good-slot rectangle
         bad-slot death
         min -25.0
         max 50.0
         bad-weight -1
     +tracker>
         control-slot stop-angle
         good-slot rectangle
         bad-slot death
         min 5.0
         max 40.0
         bad-weight -1
     +tracker>
         control-slot thrust-time
         good-slot rectangle
         bad-slot death
         min 0.067
         max 0.167
         bad-weight -1
    =goal>
        state play
        offaim 25
        game spacetrack
     ;  thrust-time .09
     )
