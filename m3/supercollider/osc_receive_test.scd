~positions = [-1, -0.5, 0, 0.5, 1];
~networkAddress = NetAddr("127.0.0.1", 57120);

(
SynthDef(\saw, {|freq=330,gate=1,pos=0,amp=0.5|
	var saw, env, pan, out;
	saw = Saw.ar(freq, mul: amp);
	pan = Pan2.ar(saw, pos);
	env = EnvGen.kr(Env.asr(), gate);
	Out.ar(0, env * pan);
}).add;
)

(
OSCdef(\ESP, { |msg, time, addr, recvPort|
	"Received OSC message: ".post;
	msg[0].postln;
	msg[1].postln;
}, "/esp/sensors", ~networkAddress);
)

(
// create 5 instruments, to be controlled using OSC data
~s1 = Synth(\saw, [\freq, 330 * 1, \amp, 0.2, \gate, 0]);
~s2 = Synth(\saw, [\freq, 330 * 2, \amp, 0.2, \gate, 0]);
~s3 = Synth(\saw, [\freq, 330 * 3, \amp, 0.2, \gate, 0]);
~s4 = Synth(\saw, [\freq, 330 * 4, \amp, 0.2, \gate, 0]);
~s5 = Synth(\saw, [\freq, 330 * 5, \amp, 0.2, \gate, 0]);
)

NetAddr.langPort

ServerOptions.devices.postln
s.reboot
Server.default.options.outDevice_("Ansel’s Bose QC35 ")
Server.default.options.inDevice_("MacBook Pro Microphone")