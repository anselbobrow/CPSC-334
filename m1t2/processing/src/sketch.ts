import p5 from 'p5';
import { Line } from './customTypes';

let prevPoint: p5.Vector;
let paused = false;
let border_imgs: p5.Image[] = [];

// parameters, play with these!
let TAIL_LENGTH = 10;
const LINE_LENGTH = 100;
const SPEED = 25;
const LINE_HISTORY = 50;

// screen size setup
const WIDTH = 1360;
const HEIGHT = 768;
const INSET = 25;

// state
let lineQueue: Line[] = [];
let background_number = 0;

const sketch = (p: p5) => {
    p.preload = () => {
        const urls: URL[] = [];

        urls.push(new URL(
            'img/border_1.jpg', // must be a string literal
            import.meta.url
        ));

        urls.push(new URL(
            'img/border_2.jpg',
            import.meta.url
        ))

        urls.push(new URL(
            'img/border_3.jpg',
            import.meta.url
        ))

        for (let url of urls) {
            border_imgs.push(p.loadImage(url.toString()));
        }
    }

    p.setup = () => {
        p.createCanvas(WIDTH * 6, HEIGHT);
        p.stroke('white');
        p.strokeWeight(5);
        p.frameRate(SPEED);

        // line starts from the middle of the screen
        prevPoint = new p5.Vector(WIDTH / 2, HEIGHT / 2);
    };

    p.draw = () => {
        if (!paused) {
            // generate a new random angle for a line to be created at
            let newX: number, newY: number;
            do {
                const randAngle = p.random(0, p.TWO_PI);
                newX = LINE_LENGTH * p.cos(randAngle) + prevPoint.x;
                newY = LINE_LENGTH * p.sin(randAngle) + prevPoint.y;
            } while (newX < 0 + INSET || newX > WIDTH - INSET || newY < 0 + INSET || newY > HEIGHT - INSET)

            // display border images
            for (let i = 0; i < 6; i++) {
                p.image(border_imgs[background_number], WIDTH * i, 0);
            }
            background_number = (background_number + 1) % 3;

            // display all lines
            for (let i = 0; i < 6; i++) {
                lineQueue.forEach((l, idx) => {
                    let xoffset = WIDTH * i;
                    if (lineQueue.length - idx > i && idx > 5 - i) {
                        p.line(l.x1 + xoffset, l.y1, l.x2 + xoffset, l.y2);
                    }
                });
            }

            // create new line based on above random direction, add it to the queue
            const line = new Line(prevPoint.x, prevPoint.y, newX, newY);
            lineQueue.push(line);
            // trim lines off the end to keep tail length under control
            if (lineQueue.length > TAIL_LENGTH) {
                lineQueue.shift();
            }

            // increase tail length as time goes on
            if (p.frameCount % 10 == 0) {
                TAIL_LENGTH += 1;
            }

            prevPoint = new p5.Vector(newX, newY);
        }
    };

    const pause = () => {
        paused = !paused;
    }

    // reset on click
    p.mouseClicked = () => {
        TAIL_LENGTH = 10;
        lineQueue = [];
        p.setup();
    }

    // pause on space
    p.keyTyped = (e: KeyboardEvent) => {
        if (e.key == " ") {
            pause();
        }
    }
};

new p5(sketch);
