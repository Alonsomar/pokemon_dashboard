let sketch = function(p) {
    let waves = [];
    let numWaves = 5;
    let waveHeight = 60;
    let minWavelength = 600;
    let maxWavelength = 1200;
    let maxSpeed = 0.02*2;
    let minSpeed = 0.005*2;

    p.setup = function() {
        let canvas = p.createCanvas(p.windowWidth, p.windowHeight);
        canvas.parent('p5-container');
        p.colorMode(p.HSB, 360, 100, 100, 100);
        initializeWaves();
        p.frameRate(30);
    };

    p.draw = function() {
        p.background(210, 20, 95);
        for (let wave of waves) {
            wave.display();
            wave.move();
        }
    };

    p.windowResized = function() {
        p.resizeCanvas(p.windowWidth, p.windowHeight);
        initializeWaves();
    };

    function initializeWaves() {
        waves = [];
        let startY = p.height - p.height * 2/3;
        let gap = (p.height - startY) / numWaves;
        for (let i = 0; i < numWaves; i++) {
            let wavelength = p.random(minWavelength, maxWavelength);
            let speed = p.random(minSpeed, maxSpeed);
            let hue = p.map(i, 0, numWaves, 200, 240);
            waves.push(new Wave(p, startY + i * gap, waveHeight, wavelength, speed, hue, i));
        }
    }

    class Wave {
        constructor(p, baseY, amplitude, wavelength, speed, hue, index) {
            this.p = p;
            this.baseY = baseY;
            this.amplitude = amplitude;
            this.wavelength = wavelength;
            this.speed = speed;
            this.hue = hue;
            this.index = index;
            this.offset = 0;
        }

        move() {
            this.offset += this.speed;
        }

        display() {
            this.p.fill(this.hue, 60, 90, 10 + this.index * 2);
            this.p.noStroke();
            this.p.beginShape();
            for (let x = 0; x <= this.p.width; x += 10) {
                let y = this.baseY + this.p.sin((x / this.wavelength) * this.p.TWO_PI + this.offset) * this.amplitude;
                y += this.p.noise(x * 0.01, this.offset * 0.8) * 20;
                this.p.vertex(x, y);
            }
            this.p.vertex(this.p.width, this.p.height);
            this.p.vertex(0, this.p.height);
            this.p.endShape(this.p.CLOSE);
        }
    }
};

window.onload = function() {
    setTimeout(function() {
        console.log(document.getElementById('p5-container')); // Check if it prints the element
        new p5(sketch);
    }, 1000); // Delay for 1000 milliseconds (1 second)
};
