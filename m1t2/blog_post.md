# Animated Line Art - Ansel Bobrow

Author: Ansel Bobrow

## Task 1

Our team’s documentation for task one and figuring out the mapping of the projector can be found in the README of the GitHub repo we used: [cpsc334.a1](https://github.com/evankirkiles/cs334.a1/tree/c48cd395e35f983f753d9b3f08724d82dae7a28a)

## Task 2

This piece was inspired by the layout of the projectors at the CCAM, similar to a strip of film rotated 90º. I thought it’d be interesting to play an animation like a film, cycling a frame over all the projectors at various speeds, to both take advantage of the medium and expose the underlying visual effect.

![https://png2png.com/wp-content/uploads/2021/05/filmstrip-png-21905-1536x293.png](https://png2png.com/wp-content/uploads/2021/05/filmstrip-png-21905-1536x293.png)

I first wrote a processing script to simply animate a line over the screen. It looks something like this.

![Screen Recording 2022-09-20 at 21.12.26.gif](blog_content/Screen_Recording_2022-09-20_at_21.12.26.gif)

I’m using p5.js to write the code, and the script works by picking a random direction to draw a new line segment on every iteration. The reason it’s happening so slowly is because I’ve adjusted the p5 `frameRate()` function to reduce the number of time `draw()` is called per second.

The slower frame rate makes it easier to see what’s going, while also alluding to imperfect and slower frame rates in actual film, which fits nicely with the style of the piece.

I then drew a few border frames in charcoal to make each slide look a little more like a roll of film, and cleaned them up and inverted them in Photoshop.

![border_1.jpg](blog_content/border_1.jpg)

I wanted to delay each subsequent slide (projector) by a frame, again to sort of simulate visualizing a film reel running through a projector, but since I initially was only using animating one slide in processing, I tried to offload the work of duplicating that slide with a time delay per projector to Isadora. After messing around on Isadora for a while I came up with this patch.

TODO: get screenshot of patch off CCAM computer

As you can see, the extensive video delay modules each stored the delayed frames in a buffer, contributing to huge buffer overload that used around 2-300% of the available RAM. (Aside: the video input was routed in Isadora from a Google Chrome window running my p5 app in real time). The only somewhat useful thing to come of this patch was that I discovered how to easily make 6 individual scenes that map to the 6 projectors out of the 2 displays, they can also be assigned to any scene number in case the HDMI cables were plugged in wrong, fixing any incorrect ordering problems.

I realized I’d have to code the delay into the processing application, so I set about duplicating the slide to create 6 copies that could then run on the CCAM computer directly from the web, no Isadora. This inspired me to do something more interesting than just a simple delay, so I coded up a frame delay that varies over time according to a sin function, meaning that the individual slides start out of sync, then slowly fade into sync, then fall back out again, etc. Both the period and max delay time of this effect are defined as macros in terms of frames at the beginning of the code and can be played around with. This is easier to visualize in the video demonstration below. Here is the line that calculates the new delay time each frame.

```jsx
delay = Math.round(p.sin(p.frameCount * p.PI / DELAY_PERIOD) * MAX_DELAY_DEPTH / 2 + MAX_DELAY_DEPTH / 2);
```

The way the delay is implemented is by storing a history (similar to an undo history) of each set of lines that have been displayed in the past several frames. Then based on the depth, each slide shows a snapshot of some point in that history. This is the best way I could come up with to allow easily creating a variable delay depth, but it’s not super clean. If you look at the last slide (far right) with the most variation in delay (from 0 to MAX_DELAY_DEPTH * 5 frames), it jumps around a lot in the history as a result of whiplash. Sometimes it glitches back in time to slow down and sometimes it jumps ahead 5 line segments at a time, but when the speed is set fast enough it’s a little less noticeable. To mitigate the back-in-time glitch when delay time is being increased, I suppose I could just have the slide wait a few frames and then continue to move instead of replaying the last 5 or so frames, but I wasn’t sure of a good way to have it grow faster to catch up when the delay speed is being reduced, so I decided not to fix it. Here is the code that determines which set of lines to display on each slide based on the current delay length.

```jsx
// display all lines
for (let slide = 0; slide < 6; slide++) {
    // determine where to query in the history for each slide
    let history_index = slide * delay;
    // make sure that there is enough history to query from
    if (history_index < lineHistory.length) {
	// grab the set of lines from that index
        let lineSet = lineHistory[history_index];
	// make sure we're drawing on the correct slide with this x offset
        let xoffset = WIDTH * i;
	// draw each line from the set
        lineSet.forEach(line => {
            p.line(line.x1 + xoffset, line.y1, line.x2 + xoffset, line.y2);
        })
    }
}
```

The other feature I added is that the length of the line grows over time, adding a new segment to the chain every 10 frames so that it gets visually more interesting and complex over time.

In order to display the webapp properly at the CCAM, I experimented with multiple methods of getting a browser to go fullscreen across 2 displays. Ultimately, what worked for me was this [open source chrome extension](https://github.com/nomomo/multidesktop-fullscreen-for-chrome-remote-desktop). I hosted the app from my laptop and used my laptop’s ip to connect to the webapp from the CCAM desktop. The final iteration of the project is however hosted [here](https://anselbobrow.com/line-art/). You can click anywhere to restart the animation.

Here’s a video of the final result.

[https://www.youtube.com/watch?v=GC2ikWnkc18](https://www.youtube.com/watch?v=GC2ikWnkc18)
