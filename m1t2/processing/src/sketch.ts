import p5 from 'p5';
import { Line } from './customTypes';

let prevPoint: p5.Vector;
let paused = false;

// parameters, play with these!
const TAIL_LENGTH = 10;
const LINE_LENGTH = 100;
const SPEED = 10;

// screen size setup
const WIDTH = 1360;
const HEIGHT = 768;

// state
let lineQueue: Line[] = [];

const sketch = (p: p5) => {
    p.setup = () => {
        p.createCanvas(WIDTH, HEIGHT);
        p.background('black');
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
            } while (newX < 0 || newX > WIDTH || newY < 0 || newY > HEIGHT)

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
            p.background('black');
            for (let l of lineQueue) {
                console.log(l);
                p.line(l.x1, l.y1, l.x2, l.y2);
            }
        }
    };

    p.mouseClicked = () => {
        paused = !paused;
    }
};

new p5(sketch);
