const canvas = document.getElementById("background");

if (canvas) {
    const ctx = canvas.getContext("2d");
    const anemiaCells = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class AnemiaCell {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 20 + 10;
            this.speed = Math.random() * 1.5 + 0.5;
            this.opacity = Math.random() * 0.3 + 0.1;
        }

        update() {
            this.y += this.speed;

            if (this.y > canvas.height + this.size) {
                this.y = -this.size;
                this.x = Math.random() * canvas.width;
            }
        }

        draw() {
            ctx.beginPath();

            ctx.fillStyle = `rgba(255, 0, 0, ${this.opacity})`;

            ctx.arc(
                this.x,
                this.y,
                this.size,
                0,
                Math.PI * 2
            );

            ctx.fill();
        }
    }

    for (let i = 0; i < 80; i++) {
        anemiaCells.push(new AnemiaCell());
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        anemiaCells.forEach(function (cell) {
            cell.update();
            cell.draw();
        });

        requestAnimationFrame(animate);
    }

    animate();
}
