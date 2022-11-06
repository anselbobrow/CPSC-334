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
~positions = [-1, -0.5, 0, 0.5, 1];

// create 5 instruments, to be controlled using OSC data
~s1 = Synth(\saw, [\freq, 330 * 1, \amp, 0, \gate, 1, \pos, ~positions[0]]);
~s2 = Synth(\saw, [\freq, 330 * 2, \amp, 0, \gate, 1, \pos, ~positions[1]]);
~s3 = Synth(\saw, [\freq, 330 * 3, \amp, 0, \gate, 1, \pos, ~positions[2]]);
~s4 = Synth(\saw, [\freq, 330 * 4, \amp, 0, \gate, 1, \pos, ~positions[3]]);
~s5 = Synth(\saw, [\freq, 330 * 5, \amp, 0, \gate, 1, \pos, ~positions[4]]);

// receive OSC messages
OSCdef(\ESP, { |msg, time, addr, recvPort|
	var r1val, r2val, r3val, r4val, r5val;
	[msg, time, addr, recvPort].postln;

	r1val = msg[1];
	r2val = msg[2];
	r3val = msg[3];
	r4val = msg[4];
	r5val = msg[5];

	~s1.set(\amp, r1val.linlin(0, 4095, 0, 0.2));
	~s2.set(\amp, r2val.linlin(0, 4095, 0, 0.2));
	~s3.set(\amp, r3val.linlin(0, 4095, 0, 0.2));
	~s4.set(\amp, r4val.linlin(0, 4095, 0, 0.2));
	~s5.set(\amp, r5val.linlin(0, 4095, 0, 0.2));
}, "/esp/sensors");
)

(
~s1.free;
~s2.free;
~s3.free;
~s4.free;
~s5.free;
)


NetAddr.localAddr
ServerOptions.devices.postln
s.reboot
Server.default.options.outDevice_("Ansel’s Bose QC35 ")
Server.default.options.inDevice_("MacBook Pro Microphone")