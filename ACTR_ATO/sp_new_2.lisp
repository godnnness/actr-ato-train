(clear-all)

(define-model SP

;(sgp :esc t :rt -2 :lf 0.4 :ans 0.5 :bll 0.5 :act nil :ncnar nil :epl t :pct t)
(sgp :seed (123456 0))
(sgp :v t :show-focus t :trace-detail high  :cursor-noise nil :incremental-mouse-moves t)
(sgp :needs-mouse "black" :process-cursor nil :include motor-command)

(chunk-type target state)
(chunk-type judge pn  property)
(chunk-type speed-diff speed)

(add-dm
   (a ISA judge pn "-"  property "down")
   (b ISA judge pn "0"  property "keep")
   (c ISA judge pn "+" property "up")

 (start isa chunk)(attend isa chunk)
 (prepare-mouse isa chunk) (move-mouse isa chunk)
 (wait-for-click isa chunk) (choose-button isa chunk) (find-button isa chunk)(recove isa chunk)
 (goal isa target state start) )

(P find-speed-diff
   =goal>
      ISA         target
      state       start

   ?visual>
     state          free
     buffer         empty

   ?visual-location>
     state          free

   ?manual>
     preparation free
     processor free
     execution free
 ==>
   +visual-location>
      isa          visual-location
      :attended nil
      kind text
      screen-x           lowest
   =goal>
      state       find-location
)

(P attend-speed-diff
   =goal>
      ISA        target
      state      find-location
   =visual-location>
   ?visual>
      state          free
      buffer         empty
==>
   +visual>
      cmd         move-attention
      screen-pos  =visual-location
   =goal>
      state       attend
)

(P encode-speed-diff
   =goal>
      ISA         target
      state       attend
   =visual>
      value       =value
   ?imaginal>
      state       free
==>
   =goal>
      state        choose-button
   +imaginal>
      isa          speed-diff
      speed     =value
)

(p choose-button
   =goal>
      isa        target
      state     choose-button

   =imaginal>
     isa       speed-diff
     speed     =value
==>
   =goal>
      state     find-button
   +retrieval>
      isa   judge
      pn   =value
   -imaginal>
    )

(p find-button
   =goal>
      isa        target
      state     find-button
   =retrieval>
      isa           judge
      pn          =value
      property    =property
  ==>
   =goal>
      state     prepare-mouse
   +visual-location>
      isa       visual-location
      :attended          nil
      screen-x           lowest
      screen-y           lowest
      kind                 oval
      value                =property
     -retrieval>
     -visual>
     )

(p move-cursor
   =goal>
      isa         target
      state      prepare-mouse
   =visual-location>
   ?visual>
      state      free
      buffer         empty
   ?manual>
     preparation free
     processor free
     execution free
  ==>
   +visual>
      isa           move-attention
      screen-pos    =visual-location
   =goal>
      state      move-mouse
   +manual>
      cmd        move-cursor
      loc        =visual-location
     )
;;;将对应的加速或减速命令调为按键动作，看到“+”按键w键0.5s,看到“-”按键s键0.5s，看到“0”按键空格0.5s
(p click-mouse
     =goal>
      isa target
      state  move-mouse
     ?manual>
      state  free
 ==>
     +goal>
       state recove
     +manual>
       cmd   click-mouse
)

(p recov_look
    =goal>
      isa target
      state  recove

    ?manual>
     state  free

   ?visual>
     state          free
     buffer         empty

   ?visual-location>
     state          free
==>
      +goal>
      state       start
      +visual>
      cmd         move-attention
      screen-y  lowest




)

(goal-focus goal)
)