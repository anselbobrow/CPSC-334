(
SynthDef(\saw, {|freq=330,gate=1,pos=0,amp=0.5|
	var saw, env, pan, out;
	saw = Saw.ar(freq, mul: amp);
	pan = Pan2.ar(saw, pos);
	env = EnvGen.kr(Env.asr(), gate);
	Out.ar(0, env * pan);
}).add;

Synth(\saw);
)

~positions = [-1, -0.5, 0, 0.5, 1];

(
OSCdef(\ESP, { |msg, time, addr, recvPort|
	"Received OSC message: ".post;
	msg[0].postln;
	msg[1].postln;
}, "/esp/sensors");
)


ServerOptions.devices.postln
s.reboot
Server.default.options.outDevice_("Ansel’s Bose QC35 ")
Server.default.options.inDevice_("MacBook Pro Microphone")