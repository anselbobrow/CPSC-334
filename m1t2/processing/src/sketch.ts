import p5 from 'p5';

let prevPoint: p5.Vector;
let paused = false;

// parameters. play with these!
const LINE_LENGTH = 100;
const SPEED = 10;

const sketch = (p: p5) => {
    p.setup = () => {
        p.createCanvas(p.windowWidth, p.windowHeight);
        p.background('black');
        p.stroke('white');
        p.strokeWeight(3);
        p.frameRate(SPEED);
        // line starts from the middle of the screen
        prevPoint = new p5.Vector(p.windowWidth / 2, p.windowHeight / 2);
    };

    p.draw = () => {
        if (!paused) {
            let newX: number, newY: number;
            do {
                const randAngle = p.random(0, p.TWO_PI);
                newX = LINE_LENGTH * p.cos(randAngle) + prevPoint.x;
                newY = LINE_LENGTH * p.sin(randAngle) + prevPoint.y;
            } while (newX < 0 || newX > p.windowWidth || newY < 0 || newY > p.windowHeight)
            p.line(prevPoint.x, prevPoint.y, newX, newY);
            prevPoint = new p5.Vector(newX, newY);
        }
    };

    p.mouseClicked = () => {
        paused = !paused;
    }
};

new p5(sketch);
