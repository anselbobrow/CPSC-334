import p5 from 'p5';
import { Line } from './customTypes';

let prevPoint: p5.Vector;
let paused = false;
const border_urls = ['../img/border_1.jpg', '../img/border_2.jpg', '../img/border_3.jpg'];
let border_imgs: p5.Image[] = [];

// parameters, play with these!
const TAIL_LENGTH = 10;
const LINE_LENGTH = 100;
const SPEED = 10;

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
            'img/border_1.jpg',
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
        p.createCanvas(WIDTH, HEIGHT);
        p.stroke('white');
        p.strokeWeight(3);
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

            // create new line based on above random direction, add it to the queue
            const line = new Line(prevPoint.x, prevPoint.y, newX, newY);
            lineQueue.push(line);
            // trim lines off the end to keep tail length under control
            if (lineQueue.length > TAIL_LENGTH) {
                lineQueue.shift();
            }

            prevPoint = new p5.Vector(newX, newY);

            // display all lines
            // TODO: custom backgrounds
            p.background(border_imgs[background_number]);
            background_number = (background_number + 1) % 3;

            for (let l of lineQueue) {
                p.line(l.x1, l.y1, l.x2, l.y2);
            }
        }
    };

    const pause = () => {
        paused = !paused;
    }

    p.mouseClicked = () => {
        pause();
    }

    p.keyTyped = (e: KeyboardEvent) => {
        if (e.key == " ") {
            pause();
        }
    }
};

new p5(sketch);
