use_synth :sine
live_loop :foo do
  use_real_time
  a = sync "/osc*/freq"
  play a[0], attack: 0, release: 0, sustain: 0.5
end