~positions = [-1, -0.5, 0, 0.5, 1];

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
// create 5 instruments, to be controlled using OSC data
~s1 = Synth(\saw, [\freq, 330 * 1, \amp, 0.2, \gate, 0]);
~s2 = Synth(\saw, [\freq, 330 * 2, \amp, 0.2, \gate, 0]);
~s3 = Synth(\saw, [\freq, 330 * 3, \amp, 0.2, \gate, 0]);
~s4 = Synth(\saw, [\freq, 330 * 4, \amp, 0.2, \gate, 0]);
~s5 = Synth(\saw, [\freq, 330 * 5, \amp, 0.2, \gate, 0]);

// receive OSC messages
OSCdef(\ESP, { |msg, time, addr, recvPort|
	var r1val, r2val, r3val, r4val;
	// [msg, time, addr, recvPort].postln;

	r1val = msg[1];
	r2val = msg[2];
	r3val = msg[3];
	r4val = msg[4];

	~s1.set(\gate, r1val.linlin(0, 4095, -1, 1));
	~s2.set(\gate, r2val.linlin(0, 4095, -1, 1));
	~s3.set(\gate, r3val.linlin(0, 4095, -1, 1));
	~s4.set(\gate, r4val.linlin(0, 4095, -1, 1));
}, "/esp/sensors");
)


ServerOptions.devices.postln
s.reboot
Server.default.options.outDevice_("Ansel’s Bose QC35 ")
Server.default.options.inDevice_("MacBook Pro Microphone")