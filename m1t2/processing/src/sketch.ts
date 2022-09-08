import p5 from 'p5';

const sketch = (p: p5) => {
    p.setup = () => {
        p.createCanvas(p.windowWidth, p.windowHeight);
        p.background('LightSkyBlue');
        p.fill('Green');
    };

    p.draw = () => {
        if (p.mouseIsPressed) {
            p.circle(p.mouseX, p.mouseY, 100);
        }
    };
};

new p5(sketch);
